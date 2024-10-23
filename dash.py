import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
from query import conexao
import streamlit as st


# *** Primeira Constulta / Atualizações de Dados
# Consultar os dados
query = "SELECT * FROM tb_carros"

# Carregar os dados
df = conexao(query)

# Botão para atualizar
if st.button("Atualizar Dados"):
    df = conexao(query)

# **** ESTRUTURA LATERAL DE FILTROS *****

st.sidebar.header("Selecione o Filtro")

marca = st.sidebar.multiselect("Marca Selecionada", # Nome do seletor
                               options= df["marca"].unique(), # Opções
                               default= df["marca"].unique() # As marcas
                               )

modelo = st.sidebar.multiselect("Modelo Selecionado",
                                options= df["modelo"].unique(),
                                default= df["modelo"].unique()
                                )

ano = st.sidebar.multiselect("Ano Selecionado",
                             options= df["ano"].unique(),
                             default= df["ano"].unique()
                             )

valor = st.sidebar.multiselect("Valor Selecionado",
                               options= df["valor"].unique(),
                               default= df["valor"].unique()
                               )

cor = st.sidebar.multiselect("Cor Selecionada",
                             options= df["cor"].unique(),
                             default= df["cor"].unique()
                             )

numero_vendas = st.sidebar.multiselect("Numero de Vendas Selecionada",
                             options= df["numero_vendas"].unique(),
                             default= df["numero_vendas"].unique()
                             )


# Aplicar os filtros selecionados
df_selecionado = df[
    (df["marca"].isin(marca)) &
    (df["modelo"].isin(modelo)) &
    (df["ano"].isin(ano)) &
    (df["valor"].isin(valor)) &
    (df["cor"].isin(cor)) &
    (df["numero_vendas"].isin(numero_vendas)) 
]

# **** EXIBIR VALORES MÉDIOS - ESTASTICAS ****
def Home():
    with st.expander("Valores"): # Cria uma caixa expánsivel com um titulo
        mostrarDados = st.multiselect('Filter: ', df_selecionado.columns, default=[])

        # Verifica se o usuário selecionou colunas para exibir
        if mostrarDados:
            # Exibe os dados filtrados pelas colunas selecionadas
            st.write(df_selecionado[mostrarDados])
    
    if not df_selecionado.empty:
        venda_total = df_selecionado["numero_vendas"].sum()
        venda_media = df_selecionado["numero_vendas"].mean()
        venda_mediana = df_selecionado["numero_vendas"].median()

        total1, total2, total3 = st.columns(3, gap="large")

        with total1:
            st.info("Valor total de vendas dos Carros", icon='🚨')
            st.metric(label="Total", value=f"{venda_total:,.0f}")

        with total2:
            st.info("Valor médio das vendas", icon='🚨')
            st.metric(label="Média", value=f"{venda_media:,.0f}")

        with total3:
            st.info("Valor Mediano dos carros", icon='🚨')
            st.metric(label="Mediana", value=f"{venda_mediana:,.0f}")

    # Exibe um aviso se não houver dados disponivéis com os filtros aplicados
    else:
        st.warning("Nenhum dado disponível com os filtros selecionados")

    # Insere uma lista divisória para separar as seções
    st.markdown("""---------""")


# ************* GRÁFICOS *****************
def graficos(df_selecionado):
    if df_selecionado.empty:
        st.warning("Nenhum dado disponível para gerar gráficos")
        # Interrompe a função, pois não tem motivo para continuar executando sem dados
        return
    
    # Criação dos Gráficos
    # 4 Abas -> Gráfico de barras, grafico de linhas, gráfico de pizza e Dispersão

    graf1, graf2, graf3, graf4, graf5, graf6= st.tabs(["Gráfico de Barras", "Gráfico de Linhas", "Gráfico de Pizza", "Gráfico de Dispersão", "Gráfico de Dispersão Simples", "Gráfico de Área"])

    with graf1:
        st.write("Gráfico de Barras") # Título

        investimento = df_selecionado.groupby("marca").count()[["valor"]].sort_values(by="valor", ascending=False)
        # Agrupa pela marca e conta o número de ocorrências da coluna valor. Depois ordena o resultado de forma decrescente

        fig_valores = px.bar(investimento, # COntém os dados sobre os valores por marca
                             x=investimento.index,
                             y="valor",
                             orientation="h",
                             title= "<b>Valores de Carros</b>",
                             color_discrete_sequence=["#0083b3"])

        # Exibe a figura e ajusta na tela para ocupar toda a largura disponivel.
        st.plotly_chart(fig_valores, use_container_width= True)


    with graf2:
        st.write("Gráfico de Linhas")
        dados = df_selecionado.groupby("marca").count()[["valor"]]
        
        fig_valores2 = px.line(dados,
                               x=dados.index,
                               y="valor",
                               title="<b>Valores por Marca</b>",
                               color_discrete_sequence=["#0083b3"])
                               
        st.plotly_chart(fig_valores2, use_container_width=True)

    
    with graf3:
        st.write("Gráfico de Pizza")
        dados2 = df_selecionado.groupby("marca").sum()[["valor"]]

        fig_valores3 = px.pie(dados2,
                              values="valor", # Valores que serão representados
                              names=dados2.index, # Os nomes (marcas) que irão rotular
                              title="<b>Distribuição de Valores por Marca</b>")

        st.plotly_chart(fig_valores3, use_container_width=True)

    with graf4:
        st.write("Gráfico de Dispersão")
        dados3 = df_selecionado.melt(id_vars=["marca"], value_vars=["valor"])

        fig_valores4 = px.scatter(dados3,
                                  x="marca",
                                  y="value",
                                  color="variable",
                                  title="<b>Dispersão de Valores por Marca</b>")
            
        st.plotly_chart(fig_valores4, use_container_width=True)

    with graf5:
        st.write("Gráfico de Dispersão Simples")
    
        fig_valores5 = px.scatter(df_selecionado,                            
                                  x="marca",
                                  y="valor",
                                  title="<b>Dispersão Simples de Valores por Marca</b>",
                                  color="marca",
                                  hover_name="marca",
                                  size="numero_vendas",
                                  size_max=20,
                                  template="plotly_white")
    
        st.plotly_chart(fig_valores5, use_container_width=True)
        

    with graf6:
        st.write("Gráfico de Área")

        if not df_selecionado.empty:
            dados_area = df_selecionado.groupby(['marca', 'ano']).sum().reset_index()

            fig_valores6 = px.area(dados_area,
                                   x='ano',
                                   y='numero_vendas',
                                   color='marca',
                                   title="<b>Evolução das Vendas por Marca</b>",
                                   labels={'numero_vendas': 'Número de Vendas', 'ano': 'Ano'},
                                   template='plotly_white')

            st.plotly_chart(fig_valores6, use_container_width=True)

        else:
            st.warning("Nenhum dado disponível para gerar o gráfico de área.")

def barraprogresso():
    valorAtual = df_selecionado["numero_vendas"].sum()
    objetivo = 20000000
    percentual= round((valorAtual/objetivo * 100))


    if percentual > 100:
        st.subheader("Valores Atingidos !")
    else:
        st.write(f"Você tem {percentual}% de {objetivo}. Corra atrás Filhão !!")

        mybar = st.progress(0)
        for percentualCompleto in range(percentual):
            mybar.progress(percentualCompleto + 1, text="Alvo %")

# ****** MENU LATERAL ******

def menuLateral():
    with st.sidebar:
        selecionado = option_menu(menu_title="Menu", options=["Home", "Progresso"],
                                  icons=["house", "eye"], menu_icon="cast",
                                  default_index=0)
        
    if selecionado == "Home":
        st.subheader(f"Página: {selecionado}")
        Home()
        graficos(df_selecionado)

    if selecionado == "Progresso":
        st.subheader(f"Página:{selecionado}")
        barraprogresso()
        graficos(df_selecionado)


menuLateral()


# python -m streamlit run dash.py *** TESTAR