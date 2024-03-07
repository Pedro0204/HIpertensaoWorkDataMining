import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go

# Carregar os dados do arquivo CSV
dados_filtrados = pd.read_csv("datatest.csv")

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
app = dash.Dash(__name__)

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
    dcc.Graph(id='diagnosis-pie-chart'),
    dcc.Graph(id='sex-pie-chart'),
    dcc.Graph(id='visits-pie-chart')
])

# Callback para atualizar os gráficos com base na região selecionada
@app.callback(
    [Output('diagnosis-pie-chart', 'figure'),
     Output('sex-pie-chart', 'figure'),
     Output('visits-pie-chart', 'figure')],
    [Input('region-dropdown', 'value')]
)
def update_charts(selected_region):
    # Filtrar os dados com base na região selecionada
    filtered_data = dados_filtrados[dados_filtrados['Estado'].map(codigo_regiao_map) == selected_region]
    filtered_hipertensao = filtered_data[filtered_data['Diagnóstico_Hipertensao'] == 1]

    # Calcular porcentagens para o diagnóstico de hipertensão
    total_pessoas = filtered_data.shape[0]
    count_diagnosis = filtered_data['Diagnóstico_Hipertensao'].value_counts()
    labels_diagnosis = ['Tem Hipertensão' if x == 1 else 'Não Tem Hipertensão' for x in count_diagnosis.index]
    values_diagnosis = (count_diagnosis / total_pessoas) * 100

    # Criar o gráfico de pizza para o diagnóstico de hipertensão
    fig_diagnosis = go.Figure(data=[go.Pie(labels=labels_diagnosis, values=values_diagnosis, hole=0.3)])
    fig_diagnosis.update_layout(title=f'Distribuição de Diagnóstico de Hipertensão na Região {selected_region}')

    # Calcular porcentagens para o sexo das pessoas com hipertensão
    count_sex = filtered_hipertensao['Sexo'].value_counts()
    labels_sex = ['Homem' if x == 1 else 'Mulher' for x in count_sex.index]
    values_sex = (count_sex / count_sex.sum()) * 100

    # Criar o gráfico de pizza para o sexo das pessoas com hipertensão
    fig_sex = go.Figure(data=[go.Pie(labels=labels_sex, values=values_sex, hole=0.3)])
    fig_sex.update_layout(title=f'Distribuição por Sexo das Pessoas com Hipertensão na Região {selected_region}')

    # Calcular porcentagens para a frequência de visitas médicas regulares
    count_visits = filtered_hipertensao['Visita_Medico_Regulares'].value_counts()
    labels_visits = count_visits.index.astype(str)
    values_visits = (count_visits / count_visits.sum()) * 100

    # Criar o gráfico de pizza para a frequência de visitas médicas regulares
    fig_visits = go.Figure(data=[go.Pie(labels=labels_visits, values=values_visits, hole=0.3)])
    fig_visits.update_layout(title=f'Distribuição de Frequência de Visitas Médicas Regulares na Região {selected_region}')

    return fig_diagnosis, fig_sex, fig_visits

if __name__ == '__main__':
    app.run_server(debug=True)
