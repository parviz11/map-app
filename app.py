from dash import Dash, html, dcc, Input, Output

import graphs

import pandas as pd
import numpy as np


external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = Dash(__name__, external_stylesheets=external_stylesheets)

"""
external_stylesheets=[dbc.themes.BOOTSTRAP],
    meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1'}]
"""

# Define random sample of customers
"""customers = [{'country':'Norway','age': random.randint(20,70),
              'income': random.randint(50000,200000),'latitude': random.uniform(59,71),
              'longitude': random.uniform(4,33), 'gender': np.random.choice(["M", "F"])} for i in range(100)] + \
            [{'country':'Sweden','age': random.randint(20,70),
              'income': random.randint(50000,200000),'latitude': random.uniform(55,69),
              'longitude': random.uniform(11,24), 'gender': np.random.choice(["M", "F"])} for i in range(150)] + \
            [{'country':'Denmark','age': random.randint(20,70),
              'income': random.randint(50000,200000),'latitude': random.uniform(54,58),
              'longitude': random.uniform(7,15), 'gender': np.random.choice(["M", "F"])} for i in range(60)] + \
            [{'country':'Finland','age': random.randint(20,70),
              'income': random.randint(50000,200000),'latitude': random.uniform(59,70),
              'longitude': random.uniform(20,32), 'gender': np.random.choice(["M", "F"])} for i in range(40)]

df = pd.DataFrame(customers)"""

df = pd.read_csv("test_data.csv")


# Import initial graphs
## Map
map_fig = graphs.main_map(df)
## Age histogram
age_hist = graphs.age_hist(df)
## Income histogram
income_hist = graphs.inc_hist(df)

# Add radio items to select between base map and satellite.

# Define app layout

app.layout = html.Div(
    [
        html.H1("Geolocations of the active insurances"),
        html.Div(
            [
                html.Div(
                    [
                        dcc.Dropdown(
                            df["country"].unique().tolist(),
                            placeholder="Country",
                            id="country-filter",
                            multi=True,
                        ),
                    ],
                    style={"width": "15%", "float": "left", "display": "inline-block"},
                ),
                html.Div(
                    [
                        dcc.Dropdown(
                            df["partner"].unique().tolist(),
                            placeholder="Partner",
                            id="partner-filter",
                            multi=True,
                        ),
                    ],
                    style={"width": "15%", "float": "left", "display": "inline-block"},
                ),
                html.Div(
                    [
                        dcc.Dropdown(
                            df["product"].unique().tolist(),
                            placeholder="Product",
                            id="product-filter",
                            multi=True,
                        ),
                    ],
                    style={"width": "15%", "float": "left", "display": "inline-block"},
                ),
            ],
            style={"padding-bottom": "2.5%"},
        ),
        html.Div(
            [
                html.Div(
                    [dcc.Graph(id="map", figure=map_fig)],
                    style={"width": "75%", "display": "inline-block", "flex": "1"},
                ),
                html.Div(
                    [
                        dcc.Graph(
                            id="age",
                            figure=age_hist,
                            style={"height": "40vh"},  # hight of the graph
                        ),
                        dcc.Graph(
                            id="income",
                            figure=income_hist,
                            style={"height": "40vh"},  # height of the graph
                        ),
                    ],
                    style={
                        "width": "25%",
                        "display": "inline-block",
                        "padding-left": "1.5%",
                    },
                ),
            ],
            style={
                "padding-top": "2.5%",
                "display": "flex",
                "float": "left",
                "width": "100%",
                "padding-bottom": "1.5%",
            },
        ),  # display : flex allows to put two children html divisions at the same position. In this case, places them on the top of the parent html division.
        html.Div(id="result", style={"whiteSpace": "pre-line"}),
    ]
)

# Callbacks


##Map callback to show customers based on filters
@app.callback(
    Output("map", "figure"),
    Input("country-filter", "value"),
    Input("partner-filter", "value"),
    Input("product-filter", "value"),
    prevent_initial_call=True,
)
def update_main_map(country, partner, product):
    input_list = []
    # Callback triggers when app is running. it returns callback error
    # if the function is not receiving any input from the beginning.
    # The first check below 'if item is not None' avoids callback errors.

    # The first 'for' loop requires column names as inputs. If column names change, update this loop.
    for j, item in zip(["country", "partner", "product"], [country, partner, product]):
        if item is not None:
            if (type(item) == list) & (len(item) > 1):
                item_list = []
                delimeter = " or "
                for i in item:
                    item_list.append("`" + j + "` == " + "'" + i + "'")
                a = "(" + delimeter.join(item_list) + ")"
                input_list.append(a)
            elif len(item) == 1:
                a = "`" + j + "` == " + "'" + item[0] + "'"
                input_list.append(a)
            elif len(item) == 0:
                pass
            else:
                a = "`" + j + "` == " + "'" + item + "'"
                input_list.append(a)

    delimeter = " and "

    if len(input_list) > 0:
        query_string = delimeter.join(input_list)
        dff = df.query(
            query_string
        )  # query method in pandas allows to enter complex row filtering with one string.
    else:
        dff = df.copy()

    return graphs.main_map(dff)


# Callback for age and income histogram


@app.callback(
    Output("age", "figure"),
    Output("income", "figure"),
    Input("map", "hoverData"),
    prevent_initial_call=True,
)
def update_hist(hoverData):
    gender = hoverData["points"][0]["customdata"][3]
    age = hoverData["points"][0]["customdata"][4]
    income = hoverData["points"][0]["customdata"][5]

    dff = df[df["country"] == hoverData["points"][0]["customdata"][0]]
    return graphs.age_hist(dff, age, gender), graphs.inc_hist(
        dff, income, gender
    )


@app.callback(
    Output("result", "children"), Input("map", "clickData"), prevent_initial_call=True
)
def update_hist(clickData):
    return clickData["points"][0]["customdata"]


if __name__ == "__main__":
    app.run_server(debug=True)
