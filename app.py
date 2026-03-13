import dash
from dash import dcc, html
import plotly.graph_objects as go
import pandas as pd

# przykładowe dane (centroidy gmin)
data = {
    "gmina": [
        "Lipno","Rydzyna","Święciechowa",
        "Wijewo","Osieczna","Krzemieniewo"
    ],
    "lat": [51.93, 51.78, 51.87, 51.95, 51.90, 51.86],
    "lon": [16.56, 16.66, 16.49, 16.20, 16.60, 16.70],
    "density": [3000, 4200, 5100, 5600, 6100, 7000]
}

df = pd.DataFrame(data)

# klasy takie jak w Twoim JS
bins = [0,3540,5008,5454,5997,6376,999999]
labels = [
    "0 - 3540",
    "3540 - 5008",
    "5008 - 5454",
    "5454 - 5997",
    "5997 - 6376",
    "6376 +"
]

sizes = [5,10,15,20,30,40]

colors = [
    '#feedde',
    '#fdd0a2',
    '#fdae6b',
    '#fd8d3c',
    '#e6550d',
    '#a63603'
]

df["class"] = pd.cut(df["density"], bins=bins, labels=labels)

# aplikacja dash
app = dash.Dash(__name__)
server = app.server
fig = go.Figure()

# dodanie punktów według klas
for label, size, color in zip(labels, sizes, colors):

    subset = df[df["class"] == label]

    fig.add_trace(
        go.Scattermapbox(
            lat=subset["lat"],
            lon=subset["lon"],
            mode="markers",
            marker=dict(
                size=size*2,
                color=color,
                opacity=0.9
            ),
            name=label,
            text=subset["gmina"],
            customdata=subset["density"],
            hovertemplate=
            "<b>Gmina:</b> %{text}<br>" +
            "<b>Gęstość:</b> %{customdata}<extra></extra>"
        )
    )

fig.update_layout(

    mapbox=dict(
        style="https://api.maptiler.com/maps/019b307b-5d41-73d7-97d8-364ae32624d5/style.json?key=yE4pMpWGGPpLz4Gx37Rq",
        center=dict(lat=51.83850, lon=16.58703),
        zoom=9
    ),

    margin=dict(l=0,r=0,t=0,b=0),
    legend_title="Ilość budynków"
)

app.layout = html.Div([

    html.H3("Mapa ilości budynków w gminach powiatu Leszczyńskiego"),

    dcc.Graph(
        figure=fig,
        style={"height":"95vh"}
    )

])


if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0",port=8050)