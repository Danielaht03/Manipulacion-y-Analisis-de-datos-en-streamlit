import streamlit as st
import pandas as pd
import plotly.express as px

# Título del Dashboard
st.title("Dashboard de Análisis Financiero")

st.markdown(""" Este tablero presenta información financiera de varias empresas, permitiendo un análisis claro de su situación económica. Con estos datos, podrás entender cómo se gestionan las finanzas de cada una y compararlas fácilmente. Ideal para tomar decisiones informadas y evaluar el rendimiento de las organizaciones.""")

# File Upload Widget
#uploaded_file = st.file_uploader("Upload your financial data CSV file", type=['csv'])
#if uploaded_file is not None:
    # Load the data from the uploaded file
    #df = pd.read_csv(uploaded_file)

# Carga y Visualización de Datos
st.header("Cargar Dataset")

# Instrucciones para cargar el archivo CSV
uploaded_file = st.file_uploader("Sube tu archivo CSV", type=["csv"])

if uploaded_file is not None:
    # Cargar los datos
    df = pd.read_csv(uploaded_file)
  
#df = pd.read_csv('https://raw.githubusercontent.com/Danielaht03/Proyecto-solvencia/main/Datos_proyecto_limpio.csv')
  
st.dataframe(df.head(10))

# Calcular los ratios financieros
df['Current_Ratio2'] = df['Current_Assets'] / df['Current_Liabilities']
df['Debt_to_Equity_Ratio2'] = (df['Short_Term_Debt'] + df['Long_Term_Debt']) / df['Equity']
df['Interest_Coverage_Ratio2'] = df['Total_Revenue'] / df['Financial_Expenses']

# Filtros para la industria y país
industries = df['Industry'].unique()
selected_industry = st.multiselect('Selecciona una industria:', industries)

countries = df['Country'].unique()
selected_country = st.multiselect('Selecciona un país:', countries)

# Filtrar el DataFrame según las selecciones
filtered_df = df
if selected_industry:
    filtered_df = filtered_df[filtered_df['Industry'].isin(selected_industry)]
  
if selected_country:
    filtered_df = filtered_df[filtered_df['Country'].isin(selected_country)]
  
# Gráfico de Ratio de Liquidez
current_ratio_fig = px.bar(filtered_df, x='Company_ID', y='Current_Ratio2', title='Ratio de Liquidez')
st.plotly_chart(current_ratio_fig)

# Gráfico de Ratio de Deuda a Patrimonio
debt_to_equity_fig = px.bar(filtered_df, x='Company_ID', y='Debt_to_Equity_Ratio2', title='Ratio de Deuda a Patrimonio')
st.plotly_chart(debt_to_equity_fig)

# Gráfico de Cobertura de Gastos Financieros
interest_coverage_fig = px.bar(filtered_df, x='Company_ID', y='Interest_Coverage_Ratio2', title='Cobertura de Gastos Financieros')
st.plotly_chart(interest_coverage_fig)
