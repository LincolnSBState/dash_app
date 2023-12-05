import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import random

dash_app = dash.Dash(__name__)
app = dash_app.server

# Define a list of quotes
quotes = [
    "Chinese diplomats denouncing US trade agreements",
    "Italy calls for greater EU cooperation.",
    "Russia vetos latest UN security council resolution",
    "India calls for greater AI regulation",
    "Diplomats from Canada express support for new NAFTA",
]

def process_query(query, speakers, n_results):
    # You can implement your query processing logic here.
    # For this example, we'll return a static summary and random quotes.
    summary = "Example summary"
    result = random.sample(quotes, min(n_results, len(quotes)))
    return summary, result

dash_app.layout = html.Div([
    html.Div([
        html.H1("Public Remarks by State Officials"),
        html.P("*This semantic search application allows users to ask questions about public remarks and find policy insights.*"),
    ], style={'width': '30%', 'float': 'left'}),
    
    html.Div([
        html.H1(""),
        html.Div([
            html.Label("What have Department of State officials said about:"),
            dcc.Textarea(id="query", placeholder="AI, China, multilateralism, etc."),
        ]),
        
        html.Div([
            html.Label("Speakers"),
            dcc.Dropdown(
                id="speakers",
                options=[
                    {'label': 'Secretary Blinken', 'value': 'Secretary Blinken'},
                    {'label': 'D-MR Verma', 'value': 'D-MR Verma'},
                ],
                multi=True,
                value=['Secretary Blinken'],
            ),
        ]),
        
        html.Div([
            html.Label("Max Results"),
            dcc.Input(id="n_results", type="number", min=1, max=100, value=10),
        ]),
        
        html.Button("Submit", id="submit-button"),
    ], style={'width': '70%', 'float': 'right'}),
    
    html.Div(id="summary-output", style={'clear': 'both'}),
    html.Div(id="quotes-output"),
])

@dash_app.callback(
    [Output("summary-output", "children"), Output("quotes-output", "children")],
    [Input("submit-button", "n_clicks"),
    Input("query", "value"),
    Input("speakers", "value"),
    Input("n_results", "value")]
)
def update_results(n_clicks, query, speakers, n_results):
    if n_clicks is None:
        return None, None

    summary, result = process_query(query, speakers, n_results)
    
    summary_output = [
        html.H2("Summary"),
        html.P(summary)
    ]

    quotes_output = [
        html.H2("Quotes")
    ]

    for doc in result:
        quotes_output.append(html.Info(doc))

    return summary_output, quotes_output

if __name__ == '__main__':
    dash_app.run_server(debug=True)