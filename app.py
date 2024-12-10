import streamlit as st  
import pandas as pd  
import plotly.express as px  
import plotly.graph_objects as go  
import numpy as np  
import numpy_financial as npf  

# Configuração inicial da página  
st.set_page_config(page_title="Controle Financeiro", page_icon="📊", layout="centered")  

# Estilo personalizado  
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

def main():  
    st.title("📊 Assistente de Controle Financeiro")  

    tab1, tab2, tab3, tab4, tab5 = st.tabs([  
        "Calculadora 50-30-20",  
        "Simulador de Investimentos",  
        "Calculadora de Empréstimo",  
        "Gestor de Orçamento",  
        "Meta por Idade"  
    ])  

    with tab1:  
        calculadora_50_30_20()  

    with tab2:  
        simulador_investimentos()  

    with tab3:  
        calculadora_emprestimo()  

    with tab4:  
        gestor_orcamento()  

    with tab5:  
        meta_idade() 

def calculadora_50_30_20():  
    st.header("📊 Calculadora 50-30-20")  
    st.write("Calcule a distribuição ideal do seu orçamento seguindo a regra 50-30-20")  

    renda = st.number_input("Digite sua renda mensal:", min_value=0.0, format="%.2f", key="renda_50_30_20")  

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
        valor_inicial = st.number_input("Valor inicial:", min_value=0.0, format="%.2f", key="valor_inicial_inv")  
        aporte_mensal = st.number_input("Aporte mensal:", min_value=0.0, format="%.2f", key="aporte_mensal_inv")  
        taxa_juros = st.number_input("Taxa de juros anual (%):", min_value=0.0, format="%.2f", key="taxa_juros_inv")  
        periodo_anos = st.number_input("Período (anos):", min_value=1, max_value=50, key="periodo_anos_inv")  

    if st.button("Calcular Investimento", key="calc_investimento"):  
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
        st.metric("Total Investido", f"R$ {(valor_inicial + aporte_mensal * periodos):,.2f}")  
        st.metric("Juros Acumulados", f"R$ {(valores_acumulados[-1] - valor_inicial - aporte_mensal * periodos):,.2f}")  

def calculadora_emprestimo():  
    st.header("💳 Calculadora de Empréstimo")  

    tipo_taxa = st.radio(  
        "Selecione o tipo de taxa de juros:",  
        ["Anual", "Mensal"],  
        key="tipo_taxa_emp"  
    )  

    col1, col2 = st.columns(2)  

    with col1:  
        valor_emprestimo = st.number_input("Valor do empréstimo:", min_value=0.0, format="%.2f", key="valor_emp")  

        if tipo_taxa == "Anual":  
            taxa_juros = st.number_input("Taxa de juros anual (%):", min_value=0.0, format="%.2f", key="taxa_juros_emp")  
        else:  
            taxa_juros = st.number_input("Taxa de juros mensal (%):", min_value=0.0, format="%.2f", key="taxa_juros_emp_mensal")  

    with col2:  
        tipo_prazo = st.radio(  
            "Selecione o tipo de prazo:",  
            ["Anos", "Meses"],  
            key="tipo_prazo_emp"  
        )  

        if tipo_prazo == "Anos":  
            prazo = st.number_input("Prazo (anos):", min_value=1, max_value=30, key="prazo_emp")  
            prazo_meses = prazo * 12  
        else:  
            prazo = st.number_input("Prazo (meses):", min_value=1, max_value=360, key="prazo_meses_emp")  
            prazo_meses = prazo  

    if st.button("Calcular Empréstimo", key="calc_emprestimo"):  
        if tipo_taxa == "Anual":  
            taxa_mensal = (1 + taxa_juros/100)**(1/12) - 1  
        else:  
            taxa_mensal = taxa_juros/100  

        prestacao = npf.pmt(taxa_mensal, prazo_meses, -valor_emprestimo)  

        saldo_devedor = valor_emprestimo  
        amortizacoes = []  
        juros_pagos = []  
        saldos = []  
        prestacoes = []  

        for i in range(int(prazo_meses)):  
            juros = saldo_devedor * taxa_mensal  
            amortizacao = prestacao - juros  
            saldo_devedor -= amortizacao  

            amortizacoes.append(amortizacao)  
            juros_pagos.append(juros)  
            saldos.append(saldo_devedor)  
            prestacoes.append(prestacao)  

        total_pago = prestacao * prazo_meses  
        total_juros = total_pago - valor_emprestimo  

        st.subheader("Resumo do Financiamento")  
        col1, col2, col3 = st.columns(3)  

        col1.metric("Prestação Mensal", f"R$ {prestacao:,.2f}")  
        col2.metric("Total a Pagar", f"R$ {total_pago:,.2f}")  
        col3.metric("Total de Juros", f"R$ {total_juros:,.2f}")  

        taxa_efetiva_anual = (1 + taxa_mensal)**12 - 1  
        st.metric("Taxa Efetiva Anual", f"{taxa_efetiva_anual*100:.2f}%")  

        fig = go.Figure()  
        fig.add_trace(go.Scatter(  
            x=list(range(len(saldos))),  
            y=saldos,  
            name='Saldo Devedor',  
            line=dict(color='blue')  
        ))  

        pagamentos_acumulados = [prestacao * (i+1) for i in range(len(saldos))]  
        fig.add_trace(go.Scatter(  
            x=list(range(len(pagamentos_acumulados))),  
            y=pagamentos_acumulados,  
            name='Total Pago',  
            line=dict(color='green')  
        ))  

        fig.update_layout(  
            title='Evolução do Financiamento',  
            xaxis_title='Meses',  
            yaxis_title='Valor (R$)',  
            hovermode='x unified'  
        )  

        st.plotly_chart(fig)  

        df_amortizacao = pd.DataFrame({  
            'Parcela': range(1, len(amortizacoes) + 1),  
            'Prestação': prestacoes,  
            'Amortização': amortizacoes,  
            'Juros': juros_pagos,  
            'Saldo Devedor': saldos  
        })  

        st.subheader("Tabela de Amortização")  
        st.dataframe(  
            df_amortizacao.style.format({  
                'Prestação': 'R$ {:.2f}',  
                'Amortização': 'R$ {:.2f}',  
                'Juros': 'R$ {:.2f}',  
                'Saldo Devedor': 'R$ {:.2f}'  
            })  
        )  

def gestor_orcamento():  
    st.header("📝 Gestor de Orçamento")  

    # Inicializar dados de orçamento na session_state  
    if 'orcamento' not in st.session_state:  
        st.session_state.orcamento = {  
            'receitas': [],  
            'despesas': []  
        }  

    col1, col2 = st.columns(2)  

    with col1:  
        st.subheader("Adicionar Receita")  
        desc_receita = st.text_input("Descrição da receita")  
        valor_receita = st.number_input("Valor da receita", min_value=0.0)  

        if st.button("Adicionar Receita"):  
            st.session_state.orcamento['receitas'].append({  
                'descricao': desc_receita,  
                'valor': valor_receita  
            })  

    with col2:  
        st.subheader("Adicionar Despesa")  
        desc_despesa = st.text_input("Descrição da despesa")  
        valor_despesa = st.number_input("Valor da despesa", min_value=0.0)  

        if st.button("Adicionar Despesa"):  
            st.session_state.orcamento['despesas'].append({  
                'descricao': desc_despesa,  
                'valor': valor_despesa  
            })  

    # Exibir resumo  
    if st.session_state.orcamento['receitas'] or st.session_state.orcamento['despesas']:  
        st.subheader("Resumo do Orçamento")  

        total_receitas = sum(item['valor'] for item in st.session_state.orcamento['receitas'])  
        total_despesas = sum(item['valor'] for item in st.session_state.orcamento['despesas'])  
        saldo = total_receitas - total_despesas  

        col1, col2, col3 = st.columns(3)  
        col1.metric("Total Receitas", f"R$ {total_receitas:,.2f}")  
        col2.metric("Total Despesas", f"R$ {total_despesas:,.2f}")  
        col3.metric("Saldo", f"R$ {saldo:,.2f}")  

        # Gráfico de despesas por categoria  
        if st.session_state.orcamento['despesas']:  
            df_despesas = pd.DataFrame(st.session_state.orcamento['despesas'])  
            fig = px.pie(df_despesas, values='valor', names='descricao', title='Despesas por Categoria')  
            st.plotly_chart(fig)  

    if st.button("Limpar Orçamento"):  
        st.session_state.orcamento = {'receitas': [], 'despesas': []}  
        st.experimental_rerun()  

def meta_idade():  
    st.header("🎯 Simulador de Meta por Idade")  
    st.write("Calcule seu patrimônio ideal por idade e meta para liberdade financeira")  

    # Criação de tabs para diferentes simulações  
    tab1, tab2 = st.tabs(["Patrimônio Ideal por Idade", "Meta Liberdade Financeira"])  

    with tab1:  
        st.subheader("Calculadora de Patrimônio Ideal por Idade")  

        col1, col2 = st.columns(2)  

        with col1:  
            custo_mensal = st.number_input(  
                "Custo mensal de vida (R$):",   
                min_value=0.0,   
                format="%.2f",  
                key="custo_mensal_idade"  
            )  

            idade = st.number_input(  
                "Idade atual:",   
                min_value=18,   
                max_value=70,   
                value=30,  
                key="idade_atual"  
            )  

        with col2:  
            capacidade_poupanca = st.slider(  
                "Capacidade de poupança (%):",   
                min_value=10.0,   
                max_value=15.0,   
                value=10.0,   
                step=0.5,  
                key="cap_poupanca"  
            )  

        if st.button("Calcular Patrimônio Ideal", key="calc_pat_ideal"):  
            # Fórmula: Patrimônio Ideal = Custo Mensal * 12 * Idade * Capacidade de Poupança  
            patrimonio_ideal = custo_mensal * 12 * idade * (capacidade_poupanca/100)  

            st.metric(  
                "Patrimônio Ideal para sua idade",   
                f"R$ {patrimonio_ideal:,.2f}"  
            )  

            st.info(  
                f"Com {idade} anos e um custo mensal de R$ {custo_mensal:,.2f}, "  
                f"poupando {capacidade_poupanca}% da sua renda, "  
                f"você deveria ter R$ {patrimonio_ideal:,.2f} acumulados."  
            )  

    with tab2:  
        st.subheader("Calculadora de Meta para Liberdade Financeira")  

        col1, col2 = st.columns(2)  

        with col1:  
            custo_mensal_lf = st.number_input(  
                "Custo mensal desejado (R$):",   
                min_value=0.0,   
                format="%.2f",  
                key="custo_mensal_lf"  
            )  

        with col2:  
            rentabilidade_anual = st.number_input(  
                "Rentabilidade anual esperada (%):",   
                min_value=0.0,   
                max_value=20.0,   
                value=8.0,  
                format="%.2f",  
                key="rent_anual"  
            )  

        if st.button("Calcular Meta de Liberdade Financeira", key="calc_lf"):  
            # Fórmula: Patrimônio LF = (Custo Mensal * 12) / (Rentabilidade Anual)  
            patrimonio_lf = (custo_mensal_lf * 12) / (rentabilidade_anual/100)  

            st.metric(  
                "Patrimônio Necessário para Liberdade Financeira",   
                f"R$ {patrimonio_lf:,.2f}"  
            )  

            # Calculando em quantos anos atingirá a meta  
            if custo_mensal_lf > 0 and capacidade_poupanca > 0:  
                poupanca_anual = custo_mensal_lf * 12 * (capacidade_poupanca/100)  
                anos_para_lf = patrimonio_lf / (poupanca_anual)  

                st.info(  
                    f"Com uma poupança de {capacidade_poupanca}% do seu custo mensal "  
                    f"e uma rentabilidade de {rentabilidade_anual}% ao ano, "  
                    f"você atingirá sua liberdade financeira em aproximadamente "  
                    f"{anos_para_lf:.1f} anos."  
                )  

        # Adicionar explicação sobre os cálculos  
        with st.expander("ℹ️ Como os cálculos são feitos?"):  
            st.write("""  
            **Patrimônio Ideal por Idade:**  
            - Fórmula: Custo Mensal × 12 × Idade × Capacidade de Poupança  
            - Este cálculo indica quanto você deveria ter acumulado na sua idade atual  

            **Meta para Liberdade Financeira:**  
            - Fórmula: (Custo Mensal × 12) ÷ Rentabilidade Anual  
            - Este valor representa quanto você precisa ter investido para viver dos rendimentos  
            - A rentabilidade considerada deve ser real (descontada a inflação)  
            """)  

if __name__ == "__main__":  
    main()  