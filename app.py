import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np
import numpy_financial as npf
import base64
from io import BytesIO

# Configuração inicial da página
st.set_page_config(page_title="Controle Financeiro", layout="centered")

# Estilos personalizados
st.markdown("""
    <style>
    .stTab {
        font-size: 18px;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)

def calculadora_50_30_20():
    st.header("📊 Calculadora 50-30-20")
    st.write("Calcule a distribuição ideal do seu orçamento seguindo a regra 50-30-20")

    renda = st.number_input("Digite sua renda mensal:", min_value=0.0, format="%.2f")

    if renda > 0:
        necessidades = renda * 0.5
        desejos = renda * 0.3
        investimentos = renda * 0.2

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Necessidades (50%)", f"R$ {necessidades:.2f}")
            st.write("- Aluguel/Moradia")
            st.write("- Alimentação")
            st.write("- Contas básicas")
            st.write("- Transporte")

        with col2:
            st.metric("Desejos (30%)", f"R$ {desejos:.2f}")
            st.write("- Lazer")
            st.write("- Streaming")
            st.write("- Restaurantes")
            st.write("- Compras")

        with col3:
            st.metric("Investimentos (20%)", f"R$ {investimentos:.2f}")
            st.write("- Poupança")
            st.write("- Investimentos")
            st.write("- Reserva de emergência")

        fig = px.pie(
            values=[necessidades, desejos, investimentos],
            names=['Necessidades', 'Desejos', 'Investimentos'],
            title='Distribuição 50-30-20'
        )
        st.plotly_chart(fig)

def simulador_investimentos():
    st.header("💰 Simulador de Investimentos")

    col1, col2 = st.columns(2)

    with col1:
        valor_inicial = st.number_input("Valor inicial:", min_value=0.0, format="%.2f")
        aporte_mensal = st.number_input("Aporte mensal:", min_value=0.0, format="%.2f")
        taxa_juros = st.number_input("Taxa de juros anual (%):", min_value=0.0, format="%.2f")
        periodo_anos = st.number_input("Período (anos):", min_value=1, max_value=50)

    if st.button("Calcular"):
        taxa_mensal = (1 + taxa_juros/100)**(1/12) - 1
        periodos = periodo_anos * 12

        valores_acumulados = []
        valor_atual = valor_inicial

        for i in range(periodos):
            valor_atual = valor_atual * (1 + taxa_mensal) + aporte_mensal
            valores_acumulados.append(valor_atual)

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=list(range(periodos)),
            y=valores_acumulados,
            name='Valor Acumulado'
        ))

        fig.update_layout(
            title='Evolução do Investimento',
            xaxis_title='Meses',
            yaxis_title='Valor (R$)'
        )

        st.plotly_chart(fig)

        st.metric("Valor Final", f"R$ {valores_acumulados[-1]:,.2f}")
        st.metric("Total Investido", 
                 f"R$ {(valor_inicial + aporte_mensal * periodos):,.2f}")
        st.metric("Juros Acumulados", 
                 f"R$ {(valores_acumulados[-1] - valor_inicial - aporte_mensal * periodos):,.2f}")

def calculadora_dividas():
    st.header("💳 Calculadora de Dívidas")

    if 'dividas' not in st.session_state:
        st.session_state.dividas = []

    with st.form("nova_divida"):
        st.subheader("Adicionar Nova Dívida")
        nome = st.text_input("Nome da dívida")
        valor = st.number_input("Valor total", min_value=0.0)
        juros = st.number_input("Taxa de juros mensal (%)", min_value=0.0)

        if st.form_submit_button("Adicionar"):
            st.session_state.dividas.append({
                "nome": nome,
                "valor": valor,
                "juros": juros
            })

    if st.session_state.dividas:
        st.subheader("Suas Dívidas")
        df = pd.DataFrame(st.session_state.dividas)
        total = df['valor'].sum()
        df_ordenado = df.sort_values('juros', ascending=False)

        st.write("Método Avalanche (ordenado por taxa de juros):")
        st.table(df_ordenado)
        st.metric("Total de Dívidas", f"R$ {total:,.2f}")

        fig = px.pie(df, values='valor', names='nome', title='Composição das Dívidas')
        st.plotly_chart(fig)

    if st.button("Limpar todas as dívidas"):
        st.session_state.dividas = []
        st.experimental_rerun()

def gestor_orcamento():
    st.header("📝 Gestor de Orçamento")

    if 'orcamento' not in st.session_state:
        st.session_state.orcamento = {
            'receitas': [],
            'despesas': []
        }

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Receitas")
        with st.form("nova_receita"):
            desc_receita = st.text_input("Descrição da receita")
            valor_receita = st.number_input("Valor da receita", min_value=0.0)

            if st.form_submit_button("Adicionar Receita"):
                st.session_state.orcamento['receitas'].append({
                    'descricao': desc_receita,
                    'valor': valor_receita
                })

    with col2:
        st.subheader("Despesas")
        with st.form("nova_despesa"):
            desc_despesa = st.text_input("Descrição da despesa")
            valor_despesa = st.number_input("Valor da despesa", min_value=0.0)
            categoria = st.selectbox("Categoria", 
                                   ["Moradia", "Alimentação", "Transporte", 
                                    "Saúde", "Educação", "Lazer", "Outros"])

            if st.form_submit_button("Adicionar Despesa"):
                st.session_state.orcamento['despesas'].append({
                    'descricao': desc_despesa,
                    'valor': valor_despesa,
                    'categoria': categoria
                })

    if st.session_state.orcamento['receitas'] or st.session_state.orcamento['despesas']:
        st.subheader("Resumo do Orçamento")

        total_receitas = sum(item['valor'] for item in st.session_state.orcamento['receitas'])
        total_despesas = sum(item['valor'] for item in st.session_state.orcamento['despesas'])
        saldo = total_receitas - total_despesas

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Receitas", f"R$ {total_receitas:,.2f}")
        col2.metric("Total Despesas", f"R$ {total_despesas:,.2f}")
        col3.metric("Saldo", f"R$ {saldo:,.2f}")

        if st.session_state.orcamento['despesas']:
            df_despesas = pd.DataFrame(st.session_state.orcamento['despesas'])
            fig = px.pie(df_despesas, values='valor', names='categoria', 
                        title='Despesas por Categoria')
            st.plotly_chart(fig)

    if st.button("Limpar Orçamento"):
        st.session_state.orcamento = {'receitas': [], 'despesas': []}
        st.experimental_rerun()

def planejador_metas():
    st.header("🎯 Planejador de Metas Financeiras")

    if 'metas' not in st.session_state:
        st.session_state.metas = []

    with st.form("nova_meta"):
        st.subheader("Adicionar Nova Meta")
        descricao = st.text_input("Descrição da meta")
        valor_meta = st.number_input("Valor necessário", min_value=0.0)
        valor_atual = st.number_input("Valor já guardado", min_value=0.0)
        prazo_meses = st.number_input("Prazo (meses)", min_value=1, step=1)

        if st.form_submit_button("Adicionar Meta"):
            valor_mensal = (valor_meta - valor_atual) / prazo_meses
            progresso = (valor_atual / valor_meta) * 100

            st.session_state.metas.append({
                "descricao": descricao,
                "valor_meta": valor_meta,
                "valor_atual": valor_atual,
                "prazo_meses": prazo_meses,
                "valor_mensal": valor_mensal,
                "progresso": progresso
            })

    if st.session_state.metas:
        st.subheader("Suas Metas")

        for idx, meta in enumerate(st.session_state.metas):
            col1, col2, col3 = st.columns([2,1,1])

            with col1:
                st.write(f"**{meta['descricao']}**")
                st.progress(meta['progresso'] / 100)

            with col2:
                st.metric("Valor necessário", f"R$ {meta['valor_meta']:,.2f}")
                st.metric("Guardado", f"R$ {meta['valor_atual']:,.2f}")

            with col3:
                st.metric("Falta", f"R$ {meta['valor_meta'] - meta['valor_atual']:,.2f}")
                st.metric("Guardar por mês", f"R$ {meta['valor_mensal']:,.2f}")

            st.write("---")

    if st.button("Limpar todas as metas"):
        st.session_state.metas = []
        st.experimental_rerun()

def main():
    st.title("🎯 Assistente de Controle Financeiro")

    # Navegação usando tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Calculadora 50-30-20",
        "Simulador de Investimentos",
        "Calculadora de Dívidas",
        "Gestor de Orçamento",
        "Planejador de Metas"
    ])

    with tab1:
        calculadora_50_30_20()

    with tab2:
        simulador_investimentos()

    with tab3:
        calculadora_dividas()

    with tab4:
        gestor_orcamento()

    with tab5:
        planejador_metas()

if __name__ == "__main__":
    main()