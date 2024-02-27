import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import dash_bootstrap_components as dbc

# Carregar os dados filtrados por idade e hipertensão
dados_31_40 = pd.read_csv("dados_31_40_filtered.csv")

# Mapeamento entre códigos de estados e regiões
codigo_regiao_map = {
    # Sudeste
    35: 'Sudeste',  # São Paulo
    33: 'Sudeste',  # Rio de Janeiro
    31: 'Sudeste',  # Minas Gerais
    32: 'Sudeste',  # Espírito Santo
    # Nordeste
    29: 'Nordeste',  # Bahia
    28: 'Nordeste',  # Sergipe
    27: 'Nordeste',  # Alagoas
    26: 'Nordeste',  # Pernambuco
    25: 'Nordeste',  # Paraíba
    24: 'Nordeste',  # Rio Grande do Norte
    23: 'Nordeste',  # Ceará
    22: 'Nordeste',  # Piauí
    21: 'Nordeste',  # Maranhão
    # Sul
    43: 'Sul',  # Rio Grande do Sul
    42: 'Sul',  # Santa Catarina
    41: 'Sul',  # Paraná
    # Norte
    16: 'Norte',  # Amapá
    15: 'Norte',  # Pará
    14: 'Norte',  # Roraima
    13: 'Norte',  # Amazonas
    12: 'Norte',  # Acre
    11: 'Norte',  # Rondônia
    17: 'Norte',  # Tocantins
    # Centro-Oeste
    53: 'Centro-Oeste',  # Distrito Federal
    52: 'Centro-Oeste',  # Goiás
    51: 'Centro-Oeste',  # Mato Grosso
    50: 'Centro-Oeste',  # Mato Grosso do Sul
}

# Criar lista de regiões únicas
regioes = list(set(codigo_regiao_map.values()))

# Criar aplicativo Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout do aplicativo
app.layout = html.Div([
    html.H1("Dados de Hipertensão por Região"),
    dcc.Dropdown(
        id='region-dropdown',
        options=[
            {'label': regiao, 'value': regiao} for regiao in regioes
        ],
        value='Sudeste',  # Valor padrão para a região inicial
        clearable=False,
        searchable=False,
        placeholder="Selecione uma região"
    ),
    dcc.Graph(id='bar-chart'),
    dcc.Graph(id='age-chart'),
    dcc.Graph(id='pregnancy-pie-chart')
])

# Callback para atualizar os gráficos com base na região selecionada
@app.callback(
    [Output('bar-chart', 'figure'),
     Output('age-chart', 'figure'),
     Output('pregnancy-pie-chart', 'figure')],
    [Input('region-dropdown', 'value')]
)
def update_charts(selected_region):
    # Filtrar os dados com base na região selecionada
    filtered_data = dados_31_40[dados_31_40['V0001'].isin([codigo for codigo, regiao in codigo_regiao_map.items() if regiao == selected_region])]
    
    # Contagem de homens e mulheres na região selecionada
    contagem_sexo = filtered_data['C006'].map({2: 'Mulheres', 1: 'Homens'}).value_counts().reset_index()
    contagem_sexo.columns = ['Sexo', 'Número de Pessoas']
    
    # Criar o gráfico de barras
    bar_chart = px.bar(contagem_sexo, x='Sexo', y='Número de Pessoas', color='Sexo', barmode='group', title=f'Distribuição de Hipertensão por Sexo na Região {selected_region}')
  
    # Calcular a média de idade por sexo na região selecionada
    media_idade = filtered_data.groupby('C006')['Q003'].mean().reset_index()
    media_idade['Sexo'] = media_idade['C006'].map({1: 'Homens', 2: 'Mulheres'})
    
    # Criar o gráfico de dispersão
    age_chart = px.scatter(media_idade, x='Sexo', y='Q003', color='Sexo', title=f'Média de Idade por Sexo na Região {selected_region}')
    
    # Filtrar mulheres hipertensas grávidas
    mulheres_gravidas = filtered_data[filtered_data['C006'] == 2]
    mulheres_gravidas_hipertensas = mulheres_gravidas[mulheres_gravidas['Q00202'] == 1]
    num_mulheres_gravidas_hipertensas = len(mulheres_gravidas_hipertensas)
    num_mulheres_gravidas_nao_hipertensas = len(mulheres_gravidas) - num_mulheres_gravidas_hipertensas
    
    # Criar o gráfico de pizza
    pregnancy_pie_chart = px.pie(names=['Hipertensas', 'Não Hipertensas'], values=[num_mulheres_gravidas_hipertensas, num_mulheres_gravidas_nao_hipertensas], title='Proporção de Mulheres Hipertensas Grávidas na Região')

    return bar_chart, age_chart, pregnancy_pie_chart

if __name__ == '__main__':
    app.run_server(debug=True)
