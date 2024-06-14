import streamlit as st 
import pandas as pd 
import plotly.express as px 
from streamlit_option_menu import option_menu
import altair as alt
import time

# Título do dashboard
st.set_page_config(
    page_title="Dashboard de Vendas",
    page_icon=":bar_chart:",
    layout= "wide"
)

df = pd.read_excel("quioske_sales.xlsx")
df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values("Date")

df ["Month"] = df["Date"].apply(lambda x: str(x.year) + "-" + str (x.month))

with st.sidebar:
    selected = option_menu("Main Menu", ["Home", "Upload", 'Filtro Mês'], 
        icons=['house', 'gear',], menu_icon="cast", default_index=1)
month = st.sidebar.selectbox("Mês", df["Month"].unique())

df_filtered =  df[ df["Month"] == month ]

# Título do dashboard
st.title('Dashboard de Vendas')
with st.spinner('Wait for it...'):
  time.sleep(3)

# Gráfico de vendas por dia
st.header('Faturamento por Dia')
fig_date = px.bar(df_filtered, x="Date", y="Total")
st.plotly_chart(fig_date)

# Gráfico de vendas por dia
st.header('Faturamento por Dia (Períodos)')
fig_day = px.bar(df_filtered, x="Date", y="Total", color= "period")
st.plotly_chart(fig_day)

# Gráfico de vendas por produto
st.header('Faturamento por Produto')
fig_prod = px.bar(df_filtered, x="Date", y="Product line",color="period", orientation="h")
st.plotly_chart(fig_prod)

#Gráfico de vendas por Período
st.header('Faturamento por Período')
period_total = df_filtered.groupby('period')[('Total')].sum().reset_index()
fig_period = px.bar(period_total, x="period", y="Total")
st.plotly_chart(fig_period)


#Gráfico de vendas por Período
st.header('Faturamento por Tipo de Pagamento')
fig_kind = px.pie(df_filtered, values="Total", names="Payment")
st.plotly_chart(fig_kind)

# Opções de filtro
st.title('Filtros de produtos')
produtos = st.multiselect('Selecione os Produtos', df_filtered['Product line'].unique())
if produtos:
    df_filtered = df_filtered[df_filtered['Product line'].isin(produtos)]

# Gráfico de vendas filtradas por produto
product_filtered = df_filtered.groupby('Product line')[('Total')].sum().reset_index()
fig_filtered =alt.Chart(product_filtered).mark_bar().encode(
        x=alt.X('Product line', sort=None),
        y='Total'
).properties(
        width=600,
        height=400
    )

text_filtrado = fig_filtered.mark_text(
    align='center',
    baseline='middle',
    dy=-10 
).encode(
    text='Total'
)

st.altair_chart(fig_filtered + text_filtrado, use_container_width=True)