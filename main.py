# visit http://127.0.0.1:8050/ in your web browser.
from dash import Dash, html, dcc, Input, Output, ctx
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

name_records = pd.read_csv("data/name_records.csv")
total_births = pd.read_csv("data/total_births.csv")
unique_names = pd.read_csv("data/unique_names.csv")
unisex_names = pd.read_csv("data/unisex_names.csv")
COLORS = {
    "F": "#F347D3",
    "M": "#0AA5FC",
    "Both": "#75E924",
}


def total_births_per_year_fig():
    return px.line(total_births, x="YearOfBirth", y="Number", color="Sex", color_discrete_map=COLORS)


def unique_names_per_year_fig():
    return px.line(unique_names, x="YearOfBirth", y="Count", color="Sex", color_discrete_map=COLORS)


@app.callback(
    Output('treemap_fig', 'figure'),
    Input('name_treemap_slider', 'value'))
def update_treemap_fig(value):
    if not value:
        value = 50
    most_used_names = name_records.groupby('Name')['Number'].sum().reset_index() \
                          .sort_values(by=["Number"], ascending=False).reset_index(drop=True)[:value]
    most_used_names["Rank"] = [i+1 for i in range(most_used_names.shape[0])]
    fig = px.treemap(
        data_frame=most_used_names,
        names="Name",
        parents=["" for _ in range(most_used_names.shape[0])],
        values="Number",
        color_discrete_map=px.colors.qualitative.Pastel,
        custom_data=["Rank"]
    )
    fig.update_traces(hovertemplate='%{label}<br>Times used : %{value}<br>Rank : %{customdata}<extra></extra>')
    fig.update_layout(
        title_text='Most popular names'
    )
    return fig


@app.callback(
    Output('unisex_names_fig', 'figure'),
    Input('unisex_names_slider', 'value'))
def update_unisex_names_fig(value):
    if not value:
        value = 50
    most_popular_unisex_names = unisex_names[:value]
    most_popular_unisex_names["Rank"] = [i+1 for i in range(most_popular_unisex_names.shape[0])]
    fig = px.treemap(
        data_frame=most_popular_unisex_names,
        names="Name",
        parents=["" for _ in range(most_popular_unisex_names.shape[0])],
        values="Number",
        color_discrete_map=px.colors.qualitative.Pastel,
        custom_data=["Rank"]
    )
    fig.update_traces(hovertemplate='%{label}<br>Minimum times used : %{value}<br>Rank : %{customdata}<extra></extra>')
    fig.update_layout(
        title_text='Most popular unisex names'
    )
    return fig


@app.callback(
    Output('name_usage', 'figure'),
    Input('selected_name', 'value'))
def update_name_usage_fig(selected_name):
    selected_name_data = name_records[name_records["Name"] == selected_name]
    return px.line(selected_name_data, x="YearOfBirth", y="Number", color="Sex", color_discrete_map=COLORS)


@app.callback(
    Output('name_proportion', 'figure'),
    Input('selected_name', 'value'))
def update_name_proportion_fig(selected_name):
    selected_name_data = name_records[name_records["Name"] == selected_name]
    return px.line(selected_name_data, x="YearOfBirth", y="Proportion", color="Sex", color_discrete_map=COLORS)


@app.callback(
    Output('selected_name', 'value'),
    Input('treemap_fig', 'clickData'),
    Input('unisex_names_fig', 'clickData'))
def update_selected_name(mpn_data, mpun_data):
    if ctx.triggered_id is None:
        return "Mary"
    click_data = mpn_data if ctx.triggered_id == "treemap_fig" else mpun_data
    return click_data["points"][0]["label"]


@app.callback(
    Output('name_ranking_fig', 'figure'),
    Input('name_ranking_slider', 'value'))
def update_name_rankings_fig(value):
    if not value:
        value = 5

    def select_top_names(group):
        group = group.sort_values(by=["Number"], ascending=False).reset_index(drop=True)[:value]
        group["Rank"] = [i for i in range(1, value + 1)]
        return group

    name_rankings = name_records.groupby(["Decade", "Name"])["Number"].mean().reset_index().groupby("Decade").apply(
        select_top_names).reset_index(drop=True)

    decades = name_rankings["Decade"].unique()

    def add_missing_ranks(group):
        name = group["Name"].unique()[0]
        for decade in decades:
            if group[group["Decade"] == decade].size == 0:
                last_row = pd.DataFrame({
                    "Decade": [decade],
                    "Name": [name],
                    "Number": [0],
                    "Rank": [value + 2],
                })
                group = pd.concat([group, last_row], ignore_index=True)
        return group

    name_rankings = name_rankings.groupby("Name").apply(add_missing_ranks).reset_index(drop=True).sort_values(
        by=["Decade"]).reset_index(drop=True)
    fig1 = px.scatter(name_rankings, x="Decade", y="Rank", color="Name")
    fig2 = px.line(name_rankings, x="Decade", y="Rank", color="Name", hover_name="Name")
    fig2.update_traces(line={"width": 10}, opacity=0.5)
    fig = go.Figure(data=fig1.data + fig2.data)
    fig['layout']['yaxis']['range'] = (value + 1, 0)
    return fig


app.layout = html.Div(children=[
    html.H1(children='Data Visualisation : Baby Names in the USA from 1880 to 2015', style={"margin-left": "10px"}),

    dcc.Tabs([
        dcc.Tab(label='Total Births', children=[
            dcc.Graph(figure=total_births_per_year_fig(), style={"height": "calc(100vh - 190px)"})
        ]),
        dcc.Tab(label='Unique Names', children=[
            dcc.Graph(figure=unique_names_per_year_fig(), style={"height": "calc(100vh - 190px)"})
        ]),
        dcc.Tab(label='Name Analysis', children=[
            html.Div(children=[
                dcc.Graph(id="name_usage", style={"width": "50%"}),
                dcc.Graph(id="name_proportion", style={"width": "50%"}),
            ], style={"display": "flex"}),
            html.Label(htmlFor="selected_name", children=["Selected Name :"], style={"margin-left": "100px"}),
            dcc.Input(id='selected_name', value='Mary', type='text', style={"margin-left": "10px"}),
        ]),
        dcc.Tab(label='Most Popular Names', children=[
            dcc.Slider(10, 100, 5, marks={i: {"label": str(i)} for i in range(10, 101, 5)}, id='name_treemap_slider',
                       value=50),
            dcc.Graph(id="treemap_fig", style={"height": "calc(100vh - 200px)"}),
        ]),
        dcc.Tab(label='Unisex Names', children=[
            dcc.Slider(10, 100, 5, marks={i: {"label": str(i)} for i in range(10, 101, 5)}, id='unisex_names_slider',
                       value=50),
            dcc.Graph(id="unisex_names_fig", style={"height": "calc(100vh - 200px)"})
        ]),
        dcc.Tab(label='Name Ranking', children=[
            dcc.Slider(3, 10, 1, marks={i: {"label": str(i)} for i in range(3, 11, 1)}, id='name_ranking_slider',
                       value=5),
            dcc.Graph(id="name_ranking_fig", style={"height": "calc(100vh - 165px)"}),
        ]),
    ]),
])

if __name__ == '__main__':
    app.run_server(debug=True)
