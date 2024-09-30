
import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

# Título del Dashboard
st.title("Dashboard de Análisis Financiero")

st.markdown(""" Este tablero presenta información financiera de varias empresas, permitiendo un análisis claro de su situación económica. Con estos datos, podrás entender cómo se gestionan las finanzas de cada una y compararlas fácilmente. Ideal para tomar decisiones informadas y evaluar el rendimiento de las organizaciones.""")

# File Upload Widget
#uploaded_file = st.file_uploader("Upload your financial data CSV file", type=['csv'])
#if uploaded_file is not None:
    # Load the data from the uploaded file
    #df = pd.read_csv(uploaded_file)

# Carga y Visualización de Datos
#st.header("Cargar Dataset")

# Cargar el archivo CSV
#uploaded_file = st.file_uploader("Sube tu archivo CSV", type=["csv"])

#if uploaded_file is not None:
    # Cargar los datos
   # df = pd.read_csv(uploaded_file)
  
# Cargar los datos desde GitHub
@st.cache_data
def load_data():
    url = 'https://github.com/Danielaht03/Proyecto-solvencia/raw/main/Datos_proyecto_limpio.csv'
    return pd.read_csv(url)

df = load_data()
  
st.dataframe(df.head(10))

# Calcular los ratios financieros
df['Current_Ratio2'] = df['Current_Assets'] / df['Current_Liabilities']
df['Debt_to_Equity_Ratio2'] = (df['Short_Term_Debt'] + df['Long_Term_Debt']) / df['Equity']
df['Interest_Coverage_Ratio2'] = df['Total_Revenue'] / df['Financial_Expenses']


# Sidebar - Filtros
st.sidebar.title('Filtros')
selected_industry = st.sidebar.selectbox('Seleccionar Industry', df['Industry'].unique())
selected_country = st.sidebar.selectbox('Seleccionar Country', df['Country'].unique())
selected_company_size = st.sidebar.selectbox('Seleccionar Company Size', df['Company_Size'].unique())

# Filtrar los datos
filtered_data = df[
    (df['Industry'] == selected_industry) &
    (df['Country'] == selected_country) &
    (df['Company_Size'] == selected_company_size)
]

# Gráfico de líneas - Promedio de ratios por Industry, Country y Company Size
st.title('Promedio de Ratios Financieros')
avg_ratios = filtered_data.groupby(['Industry', 'Country', 'Company_Size'])[['Current_Ratio', 'Debt_to_Equity_Ratio', 'Interest_Coverage_Ratio']].mean().reset_index()

# Crear gráfico
fig, ax = plt.subplots()
ax.plot(avg_ratios['Industry'], avg_ratios['Current_Ratio'], label='Current Ratio', marker='o')
ax.plot(avg_ratios['Industry'], avg_ratios['Debt_to_Equity_Ratio'], label='Debt to Equity Ratio', marker='o')
ax.plot(avg_ratios['Industry'], avg_ratios['Interest_Coverage_Ratio'], label='Interest Coverage Ratio', marker='o')

ax.set_title('Promedio de Ratios Financieros por Industry, Country y Company Size')
ax.set_xlabel('Industry')
ax.set_ylabel('Promedio')
ax.legend()

st.pyplot(fig)

# Tabla de top 5 compañías por Total Revenue
st.title('Top 5 Compañías con Mayor Total Revenue')
top_5_companies = filtered_data[['Company', 'Total_Revenue']].sort_values(by='Total_Revenue', ascending=False).head(5)
st.table(top_5_companies)

# Mostrar datos filtrados
st.title('Datos Filtrados')
st.write(filtered_data)
  
# Gráfico de Ratio de Liquidez
current_ratio_fig = px.bar(filtered_df, x='Company_ID', y='Current_Ratio2', title='Ratio de Liquidez')
st.plotly_chart(current_ratio_fig)

# Gráfico de Ratio de Deuda a Patrimonio
debt_to_equity_fig = px.bar(filtered_df, x='Company_ID', y='Debt_to_Equity_Ratio2', title='Ratio de Deuda a Patrimonio')
st.plotly_chart(debt_to_equity_fig)

# Gráfico de Cobertura de Gastos Financieros
interest_coverage_fig = px.bar(filtered_df, x='Company_ID', y='Interest_Coverage_Ratio2', title='Cobertura de Gastos Financieros')
st.plotly_chart(interest_coverage_fig)
