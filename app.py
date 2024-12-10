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
    st.title("🎯 Assistente de Controle Financeiro")  

    # Navegação usando tabs  
    tab1, tab2, tab3 = st.tabs([  
        "Calculadora 50-30-20",  
        "Simulador de Investimentos",  
        "Calculadora de Empréstimo"  
    ])  

    with tab1:  
        calculadora_50_30_20()  

    with tab2:  
        simulador_investimentos()  

    with tab3:  
        calculadora_emprestimo()  

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

        # Gráfico de pizza  
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

        # Gráfico de evolução  
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

def calculadora_emprestimo():  
    st.header("💳 Calculadora de Empréstimo")  

    col1, col2 = st.columns(2)  

    with col1:  
        valor_emprestimo = st.number_input("Valor do empréstimo:", min_value=0.0, format="%.2f")  
        taxa_juros_anual = st.number_input("Taxa de juros anual (%):", min_value=0.0, format="%.2f")  
        prazo_anos = st.number_input("Prazo (anos):", min_value=1, max_value=30)  

    if st.button("Calcular Empréstimo"):  
        # Converter taxa anual para mensal  
        taxa_mensal = (1 + taxa_juros_anual/100)**(1/12) - 1  
        prazo_meses = prazo_anos * 12  

        # Calcular prestação mensal  
        prestacao = npf.pmt(taxa_mensal, prazo_meses, -valor_emprestimo)  

        # Calcular amortização e juros mês a mês  
        saldo_devedor = valor_emprestimo  
        amortizacoes = []  
        juros_pagos = []  
        saldos = []  

        for _ in range(int(prazo_meses)):  
            juros = saldo_devedor * taxa_mensal  
            amortizacao = prestacao - juros  
            saldo_devedor -= amortizacao  

            amortizacoes.append(amortizacao)  
            juros_pagos.append(juros)  
            saldos.append(saldo_devedor)  

        # Métricas principais  
        total_pago = prestacao * prazo_meses  
        total_juros = total_pago - valor_emprestimo  

        col1, col2, col3 = st.columns(3)  
        col1.metric("Prestação Mensal", f"R$ {prestacao:,.2f}")  
        col2.metric("Total a Pagar", f"R$ {total_pago:,.2f}")  
        col3.metric("Total de Juros", f"R$ {total_juros:,.2f}")  

        # Gráfico de evolução do saldo devedor  
        fig = go.Figure()  
        fig.add_trace(go.Scatter(  
            x=list(range(len(saldos))),  
            y=saldos,  
            name='Saldo Devedor'  
        ))  

        fig.update_layout(  
            title='Evolução do Saldo Devedor',  
            xaxis_title='Meses',  
            yaxis_title='Valor (R$)'  
        )  

        st.plotly_chart(fig)  

        # Tabela de amortização  
        df_amortizacao = pd.DataFrame({  
            'Prestação': [prestacao] * len(amortizacoes),  
            'Amortização': amortizacoes,  
            'Juros': juros_pagos,  
            'Saldo Devedor': saldos  
        })  

        st.subheader("Tabela de Amortização")  
        st.dataframe(df_amortizacao.style.format("{:.2f}"))  

if __name__ == "__main__":  
    main()  