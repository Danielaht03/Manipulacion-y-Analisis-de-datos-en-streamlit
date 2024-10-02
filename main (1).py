
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Título del Dashboard
st.title("Dashboard de Análisis Financiero")

st.markdown(""" Este tablero presenta información financiera de varias empresas, permitiendo un análisis claro de su situación económica. Con estos datos, podrás entender cómo se gestionan las finanzas de cada una y compararlas fácilmente. Ideal para tomar decisiones informadas y evaluar el rendimiento de las organizaciones.""")

# Cargar los datos desde GitHub
@st.cache_data
def load_data():
    url = 'https://github.com/Danielaht03/Proyecto-solvencia/raw/main/Datos_proyecto_limpio.csv'
    return pd.read_csv(url, encoding='ISO-8859-1')  

df = load_data()

st.dataframe(df.head(10))

# Cálculo de los indicadores
df['Liquidity_Ratio'] = df['Current_Assets'] / df['Current_Liabilities']
df['Debt_to_Equity_Ratio'] = df['Long_Term_Debt'] / df['Equity']
df['Interest_Coverage_Ratio'] = df['Total_Revenue'] / df['Financial_Expenses']

# Título del tablero
st.title('Tablero de Solvencia')

# Definir una paleta de colores para gráficas de pastel (colores fríos)
cold_palette = sns.color_palette("Blues_r", n_colors=8)  # Paleta de colores fríos

# Gráfica de pastel por industria (ordenada por ingresos totales)
st.subheader('Distribución de Ingresos Totales por País')
industry_revenue = df.groupby('Country')['Total_Revenue'].sum().sort_values(ascending=False)
fig, ax = plt.subplots()
industry_revenue.plot(kind='pie', autopct='%1.1f%%', ax=ax, colors=cold_palette)
ax.set_ylabel('')
st.pyplot(fig)

# Gráfica de pastel por industria (ordenada por ingresos totales)
st.subheader('Distribución de Ingresos Totales por Industria')
industry_revenue = df.groupby('Industry')['Total_Revenue'].sum().sort_values(ascending=False)
fig, ax = plt.subplots()
industry_revenue.plot(kind='pie', autopct='%1.1f%%', ax=ax, colors=cold_palette)
ax.set_ylabel('')
st.pyplot(fig)

# Gráfica de pastel por tamaño de compañía (ordenada por ingresos totales)
st.subheader('Distribución de Ingresos Totales por Tamaño de Compañía')
company_size_revenue = df.groupby('Company_Size')['Total_Revenue'].sum().sort_values(ascending=False)
fig, ax = plt.subplots()
company_size_revenue.plot(kind='pie', autopct='%1.1f%%', ax=ax, colors=cold_palette)
ax.set_ylabel('')
st.pyplot(fig)

# Gráfico de barras horizontales: Top 10 empresas por ingresos totales (ordenado de mayor a menor)
st.subheader('Top 10 Empresas con Mayor Ingreso Total')
top_10_revenue = df.nlargest(10, 'Total_Revenue').sort_values(by='Total_Revenue', ascending=False)
fig, ax = plt.subplots()
sns.barplot(data=top_10_revenue, y='Company_ID', x='Total_Revenue', ax=ax, orient='h',
            palette=sns.color_palette("Purples_r", n_colors=len(top_10_revenue)))  # Degradado inverso
plt.xticks(rotation=90)
st.pyplot(fig)

# Opciones para los filtros, incluyendo 'Todas'
industry_options = ['Todas'] + list(df['Industry'].unique())
country_options = ['Todas'] + list(df['Country'].unique())
company_size_options = ['Todas'] + list(df['Company_Size'].unique())

# Filtros
industry = st.selectbox('Selecciona una industria', options=industry_options)
country = st.selectbox('Selecciona un país', options=country_options)
company_size = st.selectbox('Selecciona el tamaño de la compañía', options=company_size_options)

# Filtrar datos según los filtros seleccionados (se ignoran si se selecciona 'Todas')
filtered_data = df.copy()
if industry != 'Todas':
    filtered_data = filtered_data[filtered_data['Industry'] == industry]
if country != 'Todas':
    filtered_data = filtered_data[filtered_data['Country'] == country]
if company_size != 'Todas':
    filtered_data = filtered_data[filtered_data['Company_Size'] == company_size]

# Ordenar los datos de mayor a menor para las gráficas
filtered_data = filtered_data.sort_values(by=['Liquidity_Ratio', 'Debt_to_Equity_Ratio', 'Interest_Coverage_Ratio'], ascending=False)

# Sección de visualizaciones
st.header('Indicadores Financieros')

# Gráfico de barras: Ratio de Liquidez (ordenado de mayor a menor)
st.subheader('Ratio de Liquidez (Current Assets / Current Liabilities)')
fig, ax = plt.subplots()
sns.barplot(data=filtered_data, x='Company_ID', y='Liquidity_Ratio', ax=ax,
            order=filtered_data.sort_values('Liquidity_Ratio', ascending=False)['Company_ID'],
            palette=sns.color_palette("Purples_r", n_colors=len(filtered_data)))  # Degradado inverso
plt.xticks(rotation=90)
st.pyplot(fig)

# Gráfico de barras: Ratio de Deuda a Patrimonio (ordenado de mayor a menor)
st.subheader('Ratio de Deuda a Patrimonio (Long Term Debt / Equity)')
fig, ax = plt.subplots()
sns.barplot(data=filtered_data, x='Company_ID', y='Debt_to_Equity_Ratio', ax=ax,
            order=filtered_data.sort_values('Debt_to_Equity_Ratio', ascending=False)['Company_ID'],
            palette=sns.color_palette("Purples_r", n_colors=len(filtered_data)))  # Degradado inverso
plt.xticks(rotation=90)
st.pyplot(fig)

# Gráfico de barras: Cobertura de Gastos Financieros (ordenado de mayor a menor)
st.subheader('Cobertura de Gastos Financieros (Total Revenue / Financial Expenses)')
fig, ax = plt.subplots()
sns.barplot(data=filtered_data, x='Company_ID', y='Interest_Coverage_Ratio', ax=ax,
            order=filtered_data.sort_values('Interest_Coverage_Ratio', ascending=False)['Company_ID'],
            palette=sns.color_palette("Purples_r", n_colors=len(filtered_data)))  # Degradado inverso
plt.xticks(rotation=90)
st.pyplot(fig)

# Gráfico de dispersión: Ratio de Deuda a Patrimonio por País e Industria
st.subheader('Relación entre Ratio de Deuda a Patrimonio, País e Industria')
fig, ax = plt.subplots()
sns.scatterplot(data=filtered_data, x='Country', y='Debt_to_Equity_Ratio', hue='Industry',
                palette='viridis', style='Industry', s=100, ax=ax)
plt.xticks(rotation=90)
ax.set_title('Ratio de Deuda a Patrimonio por País e Industria')
st.pyplot(fig)

# Gráfico de dispersión: Ratio de Liquidez por País e Industria
st.subheader('Relación entre Ratio de Liquidez, País e Industria')
fig, ax = plt.subplots()
sns.scatterplot(data=filtered_data, x='Country', y='Liquidity_Ratio', hue='Industry',
                palette='viridis', style='Industry', s=100, ax=ax)
plt.xticks(rotation=90)
ax.set_title('Ratio de Liquidez por País e Industria')
st.pyplot(fig)

# Tabla con el top 5 de compañías con mayor Total_Revenue
st.subheader('Top 5 Compañías con Mayor Total_Revenue')
top_5_companies = filtered_data.nlargest(5, 'Total_Revenue')[['Company_ID', 'Total_Revenue']]
st.table(top_5_companies)

st.markdown(""" Conclusiones: El análisis de rentabilidad entre los países revela que China se destaca con la mayor ventaja, alcanzando un 30.3% en rentabilidad. Este rendimiento sobresaliente también se refleja en la industria de Manufactura, que reporta una rentabilidad del 30.8%. Sin embargo, al examinar más de cerca las empresas dentro de estos segmentos, observamos que una de las compañías más endeudadas se encuentra en la misma industria, lo que plantea preocupaciones sobre su salud financiera.

A pesar de la alta rentabilidad que presentan estas empresas, su situación de endeudamiento y un bajo ratio de liquidez sugieren que podrían enfrentar desafíos significativos en la gestión de sus obligaciones financieras a corto plazo. Esto indica que, aunque la rentabilidad es un aspecto positivo, la capacidad de las empresas para cumplir con sus deudas y mantener una liquidez adecuada es igualmente crucial para asegurar su sostenibilidad en el mercado.""")