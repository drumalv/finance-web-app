import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# Cargar tus datos
df = pd.read_csv('Finance Recap - Transacciones.csv')
df['Fecha'] = pd.to_datetime(df['Fecha'], dayfirst=True)

# External CSS - Using a Bootswatch theme (Bootstrap theme)
external_stylesheets = [dbc.themes.BOOTSTRAP]

# Inicializar la aplicación Dash con external_stylesheets
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Definir el layout de la aplicación con componentes de Bootstrap
app.layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(html.H1("Dashboard Financiero", className="text-center mb-4"), width=12)
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H5("Filtros", className="text-center"),
                        dcc.Dropdown(
                            id='owner-dropdown',
                            options=[{'label': owner, 'value': owner} for owner in df['Owner'].unique()],
                            value=df['Owner'].unique()[0]
                        ),
                        dcc.DatePickerRange(
                            id='date-range',
                            start_date=df['Fecha'].min(),
                            end_date=df['Fecha'].max(),
                            display_format='DD/MM/YYYY'
                        ),
                    ],
                    md=4,
                ),
                dbc.Col(
                    [
                        dcc.Graph(id='financial-graph'),
                    ],
                    md=8,
                ),
            ],
            align="center",
        ),
        # Más Rows y Cols pueden ser añadidos según necesites
    ],
    fluid=True,
)

# Define the callbacks for interactivity (if needed)
@app.callback(
    Output('financial-graph', 'figure'),
    [Input('owner-dropdown', 'value'),
     Input('date-range', 'start_date'),
     Input('date-range', 'end_date')]
)
def update_graph(selected_owner, start_date, end_date):
    filtered_df = df[(df['Owner'] == selected_owner) & (df['Fecha'] >= start_date) & (df['Fecha'] <= end_date)]
    fig = px.bar(filtered_df, x='Categoría', y='Valor', title="Gastos por Categoría")
    return fig

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run_server(debug=True)
