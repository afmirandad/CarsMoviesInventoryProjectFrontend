from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State  # Agregar la importación correcta
import dash_bootstrap_components as dbc
import requests

# URL base de la API
BASE_URL = "https://carsmoviesinventoryproject-production.up.railway.app/api/v1/carsmovies"

# Crear la app de Dash
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout de la aplicación
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Gestión de Películas de Autos"), width={"size": 6, "offset": 3}),
    ], className="my-4"),

    dbc.Row([
        dbc.Col(dcc.Input(id='movie_id', type='text', placeholder="ID de Película", debounce=True), width=4),
        dbc.Col(dbc.Button("Obtener Película", id='get_movie_button', color="primary"), width=2),
    ], className="my-3"),

    dbc.Row([
        dbc.Col(html.Div(id="movie_details"), width=12),
    ], className="my-3"),

    dbc.Row([
        dbc.Col(dcc.Input(id='movie_name', type='text', placeholder="Nombre de la Película"), width=3),
        dbc.Col(dcc.Input(id='movie_year', type='text', placeholder="Año de la Película"), width=3),
        dbc.Col(dcc.Input(id='movie_duration', type='number', placeholder="Duración"), width=3),
        dbc.Col(dbc.Button("Crear Película", id='create_movie_button', color="success"), width=3),
    ], className="my-3"),

    dbc.Row([
        dbc.Col(dbc.Button("Eliminar Película", id='delete_movie_button', color="danger"), width=3),
    ], className="my-3"),
])


# Función para obtener la película
@app.callback(
    Output('movie_details', 'children'),
    [Input('get_movie_button', 'n_clicks')],
    [State('movie_id', 'value')]
)
def get_movie(n_clicks, movie_id):
    if not movie_id:
        return "Por favor, ingrese un ID válido de la película."

    if n_clicks is None:
        return ""

    response = requests.get(f"{BASE_URL}/{movie_id}")
    
    if response.status_code == 200:
        movie_data = response.json()
        return html.Div([
            html.H4(f"Nombre: {movie_data['carMovieName']}"),
            html.P(f"Año: {movie_data['carMovieYear']}"),
            html.P(f"Duración: {movie_data['duration']} minutos")
        ])
    else:
        return "Error al obtener la película."


# Función para crear una película
@app.callback(
    Output('movie_details', 'children'),
    [Input('create_movie_button', 'n_clicks')],
    [State('movie_name', 'value'),
     State('movie_year', 'value'),
     State('movie_duration', 'value')]
)
def create_movie(n_clicks, name, year, duration):
    if n_clicks is None:
        return ""

    if not name or not year or not duration:
        return "Por favor, ingrese todos los datos."

    movie_data = {
        "carMovieName": name,
        "carMovieYear": year,
        "duration": duration
    }
    
    response = requests.post(BASE_URL, json=movie_data)

    if response.status_code in [200, 201]:
        return "Película creada con éxito."
    else:
        return "Error al crear la película."


# Función para eliminar una película
@app.callback(
    Output('movie_details', 'children'),
    [Input('delete_movie_button', 'n_clicks')],
    [State('movie_id', 'value')]
)
def delete_movie(n_clicks, movie_id):
    if n_clicks is None or not movie_id:
        return ""

    response = requests.delete(f"{BASE_URL}/{movie_id}")

    if response.status_code in [200, 202, 204]:
        return "Película eliminada con éxito."
    else:
        return "Error al eliminar la película."


# Ejecutar la aplicación
if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True)
