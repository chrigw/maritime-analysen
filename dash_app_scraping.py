import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import pandas as pd

# Dash App initialisieren
app = dash.Dash(__name__)
app.title = "Analyse und Visualisierung von Online-Suchergebnissen zum Thema maritime Branche"

# Basis-URLs für GitHub-Daten
GITHUB_RAW_BASE = "https://raw.githubusercontent.com/chrigw/maritime-analysen/main"
IMAGE_BASE_URL = f"{GITHUB_RAW_BASE}/images"
DATA_BASE_URL = f"{GITHUB_RAW_BASE}/data"

# Liste der verfügbaren Suchbegriffe
search_queries = [
    "Deutsches Maritimes Zentrum DMZ",
    "Maritime Branche Deutschland",
    "Deutsche Schifffahrt",
    "Deutsche Seehäfen",
    "Fachkräftemangel deutsche maritime Branche",
    "Wettbewerbsfähigkeit deutsche maritime Branche",
    "Demografie und Nachwuchssicherung deutsche maritime Branche",
    "Deutsche maritime Sicherheit",
    "KI-Methoden in maritimen Behörden Deutschlands",
    "Maritime Förderprogramme Europa",
    "Nachhaltigkeit und Klimawandel maritime Branche",
    "Technologischer Wandel maritime Branche",
    "Alternative Handelsrouten Arktis",
    "Dekarbonisierung Schifffahrt",
    "Alternative Treibstoffe Schifffahrt",
    "Elon Musk",
    "Donald Trump",
    "Dieter Janecek",                   # Als Koordinator der Bundesregierung für maritime Wirtschaft und Tourismus ist er für die strategische Ausrichtung und Förderung der maritimen Branche in Deutschland verantwortlich.
    "Robert Habeck",                    # In seiner Funktion als Bundesminister für Wirtschaft und Klimaschutz spielt er eine Schlüsselrolle bei der Umsetzung der Energiewende, die erhebliche Auswirkungen auf die maritime Wirtschaft hat, insbesondere im Bereich der Offshore-Windenergie.
    "Volker Wissing",                   # Als Bundesminister für Digitales und Verkehr ist er für die Infrastrukturentwicklung zuständig, einschließlich der Hafenlogistik und der Digitalisierung der maritimen Wirtschaft.
    "Angela Titzrath",                  # Als Vorsitzende der Hamburger Hafen und Logistik AG (HHLA) und Präsidentin des Zentralverbands der deutschen Seehafenbetriebe (ZDS) setzt sie sich für die Interessen der Hafenwirtschaft ein und fordert beispielsweise eine erhöhte staatliche Unterstützung für die Hafeninfrastruktur.
    "Friedrich Merz",                   # Als Vorsitzender der CDU/CSU-Fraktion im Bundestag beeinflusst er die politische Debatte über wirtschaftliche Rahmenbedingungen, die auch die maritime Wirtschaft betreffen, beispielsweise durch Forderungen nach Bürokratieabbau und Infrastrukturinvestitionen.
    "Maritime Agenda 2025",             # Eine Langfriststrategie der deutschen Bundesregierung zur Förderung von Forschung und Innovation in der maritimen Wirtschaft.
    "Maritime Energiewende",            # Initiativen zur Reduktion von Treibhausgasemissionen in der Schifffahrt, einschließlich der Entwicklung alternativer Antriebstechnologien wie LNG und Akkumulatoren.
    "Offshore-Windkraft",               # Der Ausbau von Offshore-Windparks als Beitrag zur Energiewende und die damit verbundenen Chancen für die maritime Wirtschaft.
    "Maritime Digitalisierung",         # Die Integration digitaler Technologien in der Schifffahrt, bekannt als "Maritim 4.0", zur Steigerung von Effizienz und Wettbewerbsfähigkeit.
    "Maritime Sicherheit",              # Strategien zur Sicherung von Seewegen und Schutz vor maritimen Bedrohungen.
    "Schiffbauzulieferer",              # Die Bedeutung der Zulieferindustrie im Schiffbau und ihre Rolle im internationalen Wettbewerb
    "Maritime Messen und Kongresse",    # Veranstaltungen wie die SMM (Shipbuilding, Machinery & Marine Technology), die als weltweit führende Messe der maritimen Industrie gilt.
    "Hafenentwicklung und -logistik",   # Maßnahmen zur Steigerung der Wettbewerbsfähigkeit deutscher Häfen und Optimierung logistischer Prozesse.
]

# Reihenfolge der Abbildungen
plot_types = [
    "wordcloud",
    "sentiments",
    "extreme_sentiments",
    "keyword_distribution",
    "trending_keywords",
    "network",
    "country_distribution"
]

# Layout des Dashboards
app.layout = html.Div([
    html.H1("Analyse und Visualisierung von Online-Suchergebnissen zum Thema maritime Branche"),

    # Dropdown zur Auswahl des Suchbegriffs
    dcc.Dropdown(
        id='search-dropdown',
        options=[{'label': term, 'value': term} for term in search_queries],
        value=search_queries[0],  # Standardwert
    ),

    html.H3(id='selected-term'),

    # Plots (werden dynamisch hinzugefügt)
    html.Div(id='plots-container', style={'display': 'block', 'margin-bottom': '30px'}),

    # Tabelle für Top Topics
    html.H3("Top Topics"),
    html.Div(id='top-topics-table'),
])


# Callback zur Aktualisierung der Visualisierungen & Tabelle
@app.callback(
    [
        Output('selected-term', 'children'),
        Output('plots-container', 'children'),
        Output('top-topics-table', 'children')
    ],
    [Input('search-dropdown', 'value')]
)
def update_dashboard(selected_term):
    search_term_formatted = selected_term.replace(" ", "_")

    # 🔹 Plots laden
    plot_elements = [
        html.Div([
            html.H4(plot_type.replace("_", " ").capitalize()),
            html.Img(src=f"{IMAGE_BASE_URL}/{plot_type}/{search_term_formatted}_{plot_type}.png",
                     style={'width': '80%', 'margin-bottom': '20px'})
        ]) for plot_type in plot_types
    ]

    # 🔹 CSV-Daten für Top Topics laden
    def load_csv(folder, filename):
        url = f"{DATA_BASE_URL}/{folder}/{filename}"
        try:
            df = pd.read_csv(url)
            return dash_table.DataTable(
                data=df.to_dict('records'),
                columns=[{"name": i, "id": i} for i in df.columns],
                style_table={'overflowX': 'auto'},
                style_cell={'textAlign': 'left', 'padding': '5px', 'fontSize': 14},
                style_header={'fontWeight': 'bold'}
            )
        except Exception as e:
            return html.P(f"Fehler beim Laden der Daten: {str(e)}")

    top_topics_table = load_csv("top_topics", f"{search_term_formatted}_top_topics.csv")

    return (
        f"Suchbegriff: {selected_term}",
        plot_elements,
        top_topics_table
    )


if __name__ == '__main__':
    app.run(debug=True)
