# visit http://127.0.0.1:8050/ in your web browser.
from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import pandas as pd

app = Dash(__name__)

name_records = pd.read_csv("data/name_records.csv")
name_rankings = pd.read_csv("data/name_rankings.csv")
name_rankings_with_11 = pd.read_csv("data/name_rankings_with_11.csv")
total_births = pd.read_csv("data/total_births.csv")
unique_names = pd.read_csv("data/unique_names.csv")

most_used_names = name_records.groupby('Name')['Number'].sum().reset_index() \
                      .sort_values(by=["Number"], ascending=False).reset_index(drop=True)[:100]

color_dict = {
    "F": "#F347D3",
    "M": "#0AA5FC",
    "Both": "#75E924",
}

total_births_per_year_fig = px.line(total_births, x="YearOfBirth", y="Number", color="Sex",
                                    color_discrete_map=color_dict)
unique_names_per_year_fig = px.line(unique_names, x="YearOfBirth", y="Count", color="Sex",
                                    color_discrete_map=color_dict)
treemap_fig = px.treemap(
    names=most_used_names["Name"],
    parents=["" for _ in range(most_used_names.shape[0])],
    values=most_used_names["Number"],
    color_discrete_map=px.colors.qualitative.Pastel
)


@app.callback(
    Output('name_usage', 'figure'),
    Input('selected_name', 'value'))
def update_name_usage_fig(selected_name):
    selected_name_data = name_records[name_records["Name"] == selected_name]
    return px.line(selected_name_data, x="YearOfBirth", y="Number", color="Sex", color_discrete_map=color_dict)


@app.callback(
    Output('name_proportion', 'figure'),
    Input('selected_name', 'value'))
def update_name_proportion_fig(selected_name):
    selected_name_data = name_records[name_records["Name"] == selected_name]
    return px.line(selected_name_data, x="YearOfBirth", y="Proportion", color="Sex", color_discrete_map=color_dict)


@app.callback(
    Output('selected_name', 'value'),
    Input('name_treemap', 'clickData'))
def update_selected_name(click_data):
    if not click_data:
        return "Mary"
    return click_data["points"][0]["label"]


def plot_rank_chart():
    df = name_rankings_with_11.copy()

    fig1 = px.scatter(df, x="Decade", y="Rank", color="Name")
    fig1['layout']['yaxis']['autorange'] = "reversed"
    fig2 = px.line(df, x="Decade", y="Rank", color="Name", hover_name="Name")
    fig2.update_traces(line={"width": 10}, opacity=0.3)
    fig2['layout']['yaxis']['autorange'] = "reversed"
    fig = go.Figure(data=fig1.data + fig2.data)
    # fig['layout']['yaxis']['autorange'] = "reversed"
    fig['layout']['yaxis']['range'] = (11, 0)
    return fig


app.layout = html.Div(children=[
    html.H1(children='Data Vis'),

    dcc.Tabs([
        dcc.Tab(label='Total Births', children=[
            dcc.Graph(figure=total_births_per_year_fig, style={"height": "calc(100vh - 150px)"})
        ]),
        dcc.Tab(label='Unique Names', children=[
            dcc.Graph(figure=unique_names_per_year_fig, style={"height": "calc(100vh - 150px)"})
        ]),
        dcc.Tab(label='Name Analysis', children=[
            html.Div(children=[
                dcc.Graph(id="name_usage", style={"width": "50%"}),
                dcc.Graph(id="name_proportion", style={"width": "50%"}),
            ], style={"display": "flex"}),
            html.Label(htmlFor="selected_name", children=["Selected Name :"], style={"margin-left": "100px"}),
            dcc.Input(id='selected_name', value='Mary', type='text', style={"margin-left": "10px"}),
            dcc.Graph(id="name_treemap", figure=treemap_fig)
        ]),
        dcc.Tab(label='Name Ranking', children=[
            dcc.Graph(id="name_ranking", figure=plot_rank_chart(), style={"height": "calc(100vh - 150px)"}),
        ]),
    ]),
])

if __name__ == '__main__':
    app.run_server(debug=True)
