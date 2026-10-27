import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title="Portfolio Personal", page_icon="📊", layout="wide")

st.title("📊 Control de Cartera Personal")
st.caption("Prototipo interactivo · Datos extraídos de tu archivo Numbers")

# Sidebar
st.sidebar.header("Navegación")
pagina = st.sidebar.radio(
    "Ir a:",
    ["Dashboard", "Cartera (Diario)", "Cash Flow & Gastos", "Deudas & Préstamos"]
)

# ====================== DATOS (basados en tu archivo) ======================
# Resumen
resumen = pd.DataFrame({
    "Categoría": ["Crypto", "Stocks", "Cash"],
    "Invertido (€)": [1861619, 548720, -242911],
    "Valor Actual (€)": [3711338, 1039324, -242911],
    "Variación (€)": [1850694, 490605, 0],
    "% Variación": [99.36, 89.41, 0],
    "% Portfolio": [82.33, 23.06, -5.39]
})

# Crypto holdings
crypto = pd.DataFrame({
    "Activo": ["BITCOIN", "SOLANA", "ETHEREUM", "CARDANO", "LINK", "AAVE"],
    "Símbolo": ["BTC", "SOL", "ETH", "ADA", "LINK", "AAVE"],
    "Cantidad": [47.05, 4021.46, 0, 0.14, 12.76, 0.06],
    "Precio Medio (€)": [33579, 67.33, 0, 14722, 546, 14217],
    "Precio Actual (€)": [71470, 89.52, 2072, 0.18, 10.19, 118.17],
    "Invertido (€)": [1580009, 270767, 0, 2001, 6967, 1475],
    "Valor Actual (€)": [3362044, 349293, 0, 0, 0, 0]
})
crypto["Variación (€)"] = crypto["Valor Actual (€)"] - crypto["Invertido (€)"]
crypto["% Variación"] = (crypto["Variación (€)"] / crypto["Invertido (€)"].replace(0, 1)) * 100

# Stocks
stocks = pd.DataFrame({
    "Activo": ["TESLA", "MICROSTRATEGY"],
    "Símbolo": ["TSLA", "MSTR"],
    "Cantidad": [2365, 1672],
    "Precio Medio": [206, 61.5],
    "Precio Actual": [391.62, 139.82],
    "Invertido (€)": [455096, 93624],
    "Valor Actual (€)": [829858, 209466]
})
stocks["Variación (€)"] = stocks["Valor Actual (€)"] - stocks["Invertido (€)"]
stocks["% Variación"] = (stocks["Variación (€)"] / stocks["Invertido (€)"]) * 100

# Cash / Debt
cash = pd.DataFrame({
    "Cuenta": ["R4", "Sabadell", "CaixaBank", "Kraken", "Revolut"],
    "Saldo (€)": [-254345, 395, 9889, 1150, 0]
})

# Gastos / Cash Flow (ejemplo basado en la estructura)
gastos = pd.DataFrame({
    "Categoría": ["Vivienda", "Alimentación", "Transporte", "Ocio", "Otros", "Cuotas Deuda"],
    "Presupuesto (€)": [2500, 1200, 400, 600, 800, 5000],
    "Real (€)": [2450, 1180, 380, 720, 650, 5000]
})
gastos["Diferencia"] = gastos["Presupuesto (€)"] - gastos["Real (€)"]

# Préstamos
prestamos = pd.DataFrame({
    "Préstamo": ["Póliza Crédito R4", "Otro"],
    "Saldo Pendiente (€)": [60000, 0],
    "Cuota Mensual (€)": [5000, 0],
    "Tipo Interés (%)": [2.50, 0],
    "Colateral": ["Cartera Crypto/Stocks", "-"]
})

# ====================== PÁGINAS ======================
if pagina == "Dashboard":
    st.header("Visión General")
    
    total_actual = resumen["Valor Actual (€)"].sum()
    total_invertido = resumen[resumen["Categoría"] != "Cash"]["Invertido (€)"].sum()
    variacion_total = total_actual - total_invertido
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Valor Total Cartera", f"{total_actual:,.0f} €", f"{variacion_total:,.0f} €")
    col2.metric("Crypto", f"{resumen.loc[0, 'Valor Actual (€)']:,.0f} €")
    col3.metric("Stocks", f"{resumen.loc[1, 'Valor Actual (€)']:,.0f} €")
    col4.metric("Cash / Deuda neta", f"{resumen.loc[2, 'Valor Actual (€)']:,.0f} €")
    
    st.subheader("Distribución de la Cartera")
    fig = px.pie(resumen[resumen["Categoría"] != "Cash"], values="Valor Actual (€)", names="Categoría",
                 hole=0.4, color_discrete_sequence=px.colors.sequential.Blues_r)
    st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("Rentabilidad por categoría")
    fig2 = px.bar(resumen[resumen["Categoría"] != "Cash"], x="Categoría", y="% Variación",
                  text="% Variación", color="% Variación", color_continuous_scale="RdYlGn")
    fig2.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    st.plotly_chart(fig2, use_container_width=True)

elif pagina == "Cartera (Diario)":
    st.header("Cartera de Activos")
    
    tab1, tab2 = st.tabs(["Crypto", "Stocks"])
    
    with tab1:
        st.subheader("Holdings Crypto")
        st.dataframe(crypto.style.format({
            "Precio Medio (€)": "{:,.0f}",
            "Precio Actual (€)": "{:,.2f}",
            "Invertido (€)": "{:,.0f}",
            "Valor Actual (€)": "{:,.0f}",
            "Variación (€)": "{:,.0f}",
            "% Variación": "{:.1f}%"
        }), use_container_width=True, hide_index=True)
        
        fig = px.bar(crypto[crypto["Valor Actual (€)"] > 0], x="Activo", y="Valor Actual (€)",
                     color="% Variación", title="Valor Actual Crypto")
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("Holdings Stocks")
        st.dataframe(stocks.style.format({
            "Precio Medio": "{:,.2f}",
            "Precio Actual": "{:,.2f}",
            "Invertido (€)": "{:,.0f}",
            "Valor Actual (€)": "{:,.0f}",
            "Variación (€)": "{:,.0f}",
            "% Variación": "{:.1f}%"
        }), use_container_width=True, hide_index=True)
        
        fig = px.bar(stocks, x="Activo", y=["Invertido (€)", "Valor Actual (€)"],
                     barmode="group", title="Invertido vs Actual (Stocks)")
        st.plotly_chart(fig, use_container_width=True)

elif pagina == "Cash Flow & Gastos":
    st.header("Cash Flow y Control de Gastos (Mensual)")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Presupuesto Total", f"{gastos['Presupuesto (€)'].sum():,.0f} €")
    with col2:
        st.metric("Gasto Real", f"{gastos['Real (€)'].sum():,.0f} €",
                  f"{gastos['Diferencia'].sum():,.0f} €")
    
    st.subheader("Presupuesto vs Real")
    fig = go.Figure()
    fig.add_trace(go.Bar(name="Presupuesto", x=gastos["Categoría"], y=gastos["Presupuesto (€)"]))
    fig.add_trace(go.Bar(name="Real", x=gastos["Categoría"], y=gastos["Real (€)"]))
    fig.update_layout(barmode="group", title="Gastos por Categoría")
    st.plotly_chart(fig, use_container_width=True)
    
    st.dataframe(gastos.style.format({
        "Presupuesto (€)": "{:,.0f}",
        "Real (€)": "{:,.0f}",
        "Diferencia": "{:,.0f}"
    }), use_container_width=True, hide_index=True)
    
    st.info("En la versión final podrás editar el presupuesto y registrar gastos reales directamente.")

elif pagina == "Deudas & Préstamos":
    st.header("Deudas y Préstamos")
    
    total_deuda = prestamos["Saldo Pendiente (€)"].sum()
    total_cuota = prestamos["Cuota Mensual (€)"].sum()
    
    col1, col2 = st.columns(2)
    col1.metric("Saldo Total Deuda", f"{total_deuda:,.0f} €")
    col2.metric("Cuota Mensual Total", f"{total_cuota:,.0f} €")
    
    st.subheader("Detalle de Préstamos")
    st.dataframe(prestamos, use_container_width=True, hide_index=True)
    
    st.subheader("Saldos Bancarios / Efectivo")
    st.dataframe(cash.style.format({"Saldo (€)": "{:,.0f}"}), use_container_width=True, hide_index=True)
    
    st.warning("Los activos de la cartera actúan como colateral de las pólizas de crédito (según tu archivo).")

st.sidebar.markdown("---")
st.sidebar.caption("Prototipo basado en PORFOLIO-PERSONAL-2.numbers")
st.sidebar.caption(f"Última actualización: {datetime.now().strftime('%d/%m/%Y')}")
