import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import pandas as pd
import os
import requests

# Dash App initialisieren
app = dash.Dash(__name__)
app.title = "Analyse und Visualisierung von Online-Suchergebnissen zur maritimen Branche"

# === Design: Farben & Schriftart ===
font_family = "Barlow Condensed, sans-serif"
color_palette = [
    "#10225A",  # Blau
    "#D1655B",  # Coralle
    "#376179",  # Dunkleres Blau
    "#005B96",  # Blau
    "#4B85A6",  # Aqua
    "#939498",  # Grau
]

# === Logo DMZ ===
logo_url = "https://raw.githubusercontent.com/chrigw/regulations/c35d31e13ee72dd06a221bb0dd5afd4d1e270f1b/logo_dmz.png"
link_url = "https://www.deutsches-maritimes-zentrum.de"

logo_html = html.Div([
    html.A([
        html.Img(src=logo_url, style={'height': '80px'})
    ], href=link_url, target="_blank")
], style={
    'position': 'fixed',
    'top': '10px',
    'right': '10px',
    'background-color': 'white',
    'padding': '8px',
    'border-radius': '8px',
    'box-shadow': '0 0 6px rgba(0,0,0,0.2)',
    'zIndex': 9999
})

# GitHub-Basis-URLs
GITHUB_RAW_BASE = "https://raw.githubusercontent.com/chrigw/maritime-analysen/main"
IMAGE_BASE_URL = f"{GITHUB_RAW_BASE}/images"
DATA_BASE_URL = f"{GITHUB_RAW_BASE}/data"

# Suchbegriffe definieren
search_queries = [
    "Deutsches Maritimes Zentrum e.V.",
    "Maritime Branche Deutschland",
    "Maritime Sicherheit Deutschland",
    "Maritime Förderprogramme Europa",
    "Nachhaltigkeit und Klimawandel maritime Branche Deutschland",
    "Technologischer Wandel maritime Branche Deutschland",
    "Fachkräftemangel maritime Branche Deutschland",
    "Elon Musk",
    "Deutsche Schifffahrt",
    "Deutsche Seehäfen",
    "Wettbewerbsfähigkeit deutsche maritime Branche",
    "Demografie und Nachwuchssicherung deutsche maritime Branche",
    "KI-Methoden in der maritimen Branche Deutschlands",
    "Donald Trump",
    "Alternative Handelsrouten Arktis",
    "Dekarbonisierung Schifffahrt",
    "Alternative Treibstoffe Schifffahrt",
    "Dieter Janecek",
    "Robert Habeck",
    "Volker Wissing",
    "Angela Titzrath",
    "Friedrich Merz",
    "Maritime Agenda 2025",
    "Maritime Energiewende",
    "Offshore-Windkraft",
    "Maritime Digitalisierung",
    "Maritime Sicherheit",
    "Schiffbauzulieferer",
    "Maritime Messen und Kongresse",
    "Hafenentwicklung und -logistik",
    "Autonome Schifffahrt Deutschland",
    "Digitale Zwillinge Schifffahrt",
    "Cybersecurity maritime Wirtschaft"
    "Maritime Ausbildungsberufe",
    "Requalifizierung maritime Branche",
    "EU-Emissionshandel Schifffahrt",
    "Zero-Emission-Schiffe",
    "Schiffsrecycling Deutschland",
    "Supply Chain Resilienz Seehandel",
    "Chinesische Beteiligungen deutsche Häfen",
    "Nationale Hafenstrategie Deutschland",
    "Offshore-Wind und maritime Synergien",
    "https://dmz-maritim.de/handlungsfelder/",
    "Patrick Schnieder",
    "German inland waterway transport",
]
search_queries.sort()

plot_types = [
    "wordcloud",
    "sentiments",
    "extreme_sentiments",
    "keyword_distribution",
    "trending_keywords",
    "network",
    "country_distribution"
]

# Layout
app.layout = html.Div([
    logo_html,
    html.Div(style={'height': '100px'}),
    html.H1(
        "Analyse und Visualisierung von Online-Suchergebnissen zur maritimen Branche",
        style={"color": color_palette[0], "fontFamily": font_family}
    ),

    html.Div([
        html.Label("Suchbegriff auswählen:", style={"color": color_palette[2], "fontFamily": font_family, 'fontSize': '18px'}),
        dcc.Dropdown(
            id='search-dropdown',
            options=[{'label': term, 'value': term} for term in search_queries],
            value=search_queries[0],
            style={
                'fontFamily': font_family,
                'backgroundColor': 'white',
                'border': f'2px solid {color_palette[2]}',  # Dunkleres Blau
                'borderRadius': '6px',
                'padding': '10px',
                'fontSize': '16px',
                'color': color_palette[0],
                'boxShadow': '0 2px 6px rgba(0,0,0,0.15)'
            }
        )
    ], style={
        'padding': '15px',
        'marginBottom': '30px',
        'backgroundColor': '#f9f9f9',
        'borderRadius': '8px',
        'boxShadow': '0 2px 4px rgba(0,0,0,0.05)'
    }),

    html.H3(id='selected-term', style={"color": color_palette[2], "fontFamily": font_family}),
    html.Div(id='results-table', style={'marginBottom': '20px'}),
    html.Div(id='plots-container', style={'margin-bottom': '30px'}),
    html.H3("Top Topics", style={"color": color_palette[1], "fontFamily": font_family}),
    html.Div(id='top-topics-table'),
], style={"fontFamily": font_family, 'padding': '20px'})


# Hilfsfunktion für CSV-Ladung
def load_csv(folder, filename, height="300px"):
    url = f"{DATA_BASE_URL}/{folder}/{filename}"
    try:
        response = requests.get(url)
        if response.status_code != 200:
            return html.Div()
        df = pd.read_csv(url)
        return dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{"name": i, "id": i} for i in df.columns],
            style_table={'overflowX': 'auto', 'maxHeight': height, 'overflowY': 'auto'},
            style_cell={
                'textAlign': 'left', 'padding': '5px', 'fontSize': 14,
                'fontFamily': font_family, 'color': color_palette[0]
            },
            style_header={'fontWeight': 'bold', 'backgroundColor': color_palette[4], 'color': 'white'}
        )
    except:
        return html.Div()

# Callback
@app.callback(
    [
        Output('selected-term', 'children'),
        Output('plots-container', 'children'),
        Output('top-topics-table', 'children'),
        Output('results-table', 'children')
    ],
    [Input('search-dropdown', 'value')]
)
def update_dashboard(selected_term):
    search_term_formatted = selected_term.replace(" ", "_")

    # Tabellen vorbereiten
    extreme_table = load_csv("extreme_sentiments", f"{search_term_formatted}_extreme_sentiments.csv", height="200px")
    token_table = load_csv("token_sentiments", f"{search_term_formatted}_token_sentiments.csv", height="200px")
    top_topics_table = load_csv("top_topics", f"{search_term_formatted}_top_topics.csv")
    results_table = load_csv("results", f"{search_term_formatted}_results.csv", height="150px")

    # Plots laden
    plots = []
    for plot_type in plot_types:
        image_url = f"{IMAGE_BASE_URL}/{plot_type}/{search_term_formatted}_{plot_type}.png"
        try:
            if requests.get(image_url).status_code == 200:
                if plot_type == "wordcloud":
                    plots.append(html.Div([
                        html.H5("Aggregierte Ergebnisse", style={"color": color_palette[1], "fontFamily": font_family}),
                        results_table
                    ]))
                plots.append(html.Div([
                    html.H4(plot_type.replace("_", " ").capitalize(),
                            style={"color": color_palette[0], "fontFamily": font_family}),
                    html.Img(src=image_url, style={'width': '80%', 'margin-bottom': '10px'})
                ]))
                if plot_type == "sentiments":
                    plots.append(html.Div([
                        html.H5("Token Sentiments Tabelle", style={"color": color_palette[1], "fontFamily": font_family}),
                        token_table
                    ]))
                elif plot_type == "extreme_sentiments":
                    plots.append(html.Div([
                        html.H5("Extreme Sentiments Tabelle", style={"color": color_palette[1], "fontFamily": font_family}),
                        extreme_table
                    ]))
        except:
            continue

    return (
        f"Suchbegriff: {selected_term}",
        plots,
        top_topics_table,
        html.Div()  # results_table wird jetzt direkt vor Wordcloud eingebunden
    )

# Server starten
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8050)))
