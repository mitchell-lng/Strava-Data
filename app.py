# Data
import pandas as pd
from helpers import WEEK_DAYS
from datetime import datetime

# Dash Plotly
from dash import Dash, html, dcc, dash_table, Input, Output
import plotly.express as px
import pandas as pd
import numpy as np

app = Dash(__name__)

colors = {
    'background': '#111111',
    'text': '#2b3338'
}

df = 0

# Read data
def read_data():
    global df

    df = pd.read_csv('strava_activities.csv')

    df['Pace (min/mile)'] = df[df['Type'] != "Rowing"]['Speed'].apply(lambda x: (60 / x))
    df['Day of Week'] = df['Start Date Local'].apply(lambda x: WEEK_DAYS[datetime.strptime(x, "%Y-%m-%dT%H:%M:%SZ").timetuple().tm_wday])

read_data()

@app.callback(Output('general-info', 'figure'), Input('general-slider', 'value'))
def general_info(value):
    fig = px.scatter(df, x="Start Date Local", y="Pace (min/mile)",
                    size="Distance", color="Type", symbol="Type", hover_name="Name",
                    log_x=False, size_max=value/1.3, title="General Information")

    fig.update_layout(
        font_family="Sans-Serif",
        title_font_family="Sans-Serif",
        height=600
    )

    return fig

@app.callback(Output('general-exertion', 'figure'), Input('general-slider', 'value'))
def general_exertion(value):
    global df

    fig = px.scatter(df[df['Avg Heartrate'] != 0], x="Distance", y="Pace (min/mile)",
                    size="Total Elevation Gain", color="Avg Heartrate", hover_name="Name",
                    log_x=False, size_max=value/1.3, title="General Exertion Information")

    fig.update_layout(
        font_family="Sans-Serif",
        title_font_family="Sans-Serif",
        height=600
    )

    return fig

@app.callback(Output('heartrate-time', 'figure'), Input('general-slider', 'value'))
def heartrate_time(value):
    global df

    fig = px.scatter(df[df['Avg Heartrate'] != 0], x="Start Date Local", y="Pace (min/mile)", 
        size="Distance", size_max=value/1.3, hover_name="Name",
        color="Avg Heartrate", title="Heartrate Over Time in Conjucture With Speed"
        )

    fig.update_layout(
        font_family="Sans-Serif",
        title_font_family="Sans-Serif",
        height=600
    )

    return fig

def week_day():
    global df

    fig = px.histogram(df, x="Day of Week", 
        hover_name="Name",
        color="Type", title="Activities v. Day of Week",
        barmode='group',
        histfunc='sum'
        )

    fig.update_xaxes(categoryorder='array', categoryarray=WEEK_DAYS)

    fig.update_layout(
        font_family="Sans-Serif",
        title_font_family="Sans-Serif",
        height=600
    )

    return fig

# Create Layout
def main():
    global df
    
    from statistics import streak, current_daily_average_365, mph_to_pace
    import updateData

    # Read data
    read_data()

    return html.Div(
        children=[
            # Insert Titles
            html.H1(
                children='Mitchell Long',
                style={
                    'color': colors['text'],
                    "fontFamily": "Sans-Serif"
                }
            ),
            html.H3(
                children='Strava Data',
                style={
                    'color': colors['text'],
                    "fontFamily": "Sans-Serif"
                }
            ),

            html.P(
                children="Use the following slider to alter the size of the points below."
            ),

            # Size Slider
            html.Div(
                children=[
                    dcc.Slider(15, 30, value=24, marks=None, id='general-slider'),
                ]
            ),

            html.Div(
                children=[
                    html.Div(
                        id="streak",
                        children=[
                            html.H2(
                                children=[
                                    html.Span(children="Current Streak: ", style={ 'fontWeight': '400' }),
                                    html.Span(children=str(streak())),
                                    html.Span(children=" days")
                                ]
                            ),
                            html.H2(
                                children=[
                                    html.Span(children="Average Daily Distance (Over Last 365 days): ", style={ 'fontWeight': '400' }),
                                    html.Span(children=str(round(current_daily_average_365()[0], 5))),
                                    html.Span(children=" miles")
                                ]
                            ),
                            html.H2(
                                children=[
                                    html.Span(children="Average Speed (Over Last 365 days): ", style={ 'fontWeight': '400' }),
                                    html.Span(children=current_daily_average_365()[1]),
                                    html.Span(children=" pace")
                                ]
                            )
                        ],
                        style={
                            "backgroundColor": "rgb(240, 240, 240)",
                            "borderRadius": "5px",
                            "margin": "30px",
                            "fontFamily": "Sans-Serif",

                            "display": "flex",
                            "justifyContent": "center",
                            "alignItems": "center",
                            "flexDirection": "column",

                            "width": "850px",
                            "minWidth": "700px",
                            "maxWidth": "1000px",
                            "flex": "1",
                        }
                    ),

                    # Insert General Info
                    dcc.Graph(
                        id='general-info',
                        style={
                            "width": "850px",
                            "minWidth": "700px",
                            "maxWidth": "1000px",
                            "flex": "1"
                        }
                    ),

                    # Insert General Exertion
                    dcc.Graph(
                        id='general-exertion',
                        style={
                            "width": "850px",
                            "minWidth": "700px",
                            "maxWidth": "1000px",
                            "flex": "1"
                        }
                    ),

                    # Compare heartrate to time
                    dcc.Graph(
                        id='heartrate-time',
                        style={
                            "width": "850px",
                            "minWidth": "700px",
                            "maxWidth": "1000px",
                            "flex": "1"
                        }
                    ),
                    dcc.Graph(
                        id='week-day',
                        figure=week_day(),
                        style={
                            "width": "1200px",
                            "minWidth": "1000px",
                            "maxWidth": "1400px",
                            "flex": "2"
                        }
                    )
                ],
                style={
                    "display": "flex",
                    "flexWrap": "wrap",
                    "justifyContent": "center",
                }
            ),

            # Insert Table
            dash_table.DataTable(
                data=df.to_dict('records'),
                filter_action="native",
                sort_action="native",
                columns=[{'id': c, 'name': c} for c in df.columns],
                style_header={ 'border': '1px solid black' },
                style_cell={ 'border': '1px solid grey' },
                style_data={
                    'whiteSpace': 'normal',
                    'height': 'auto',
                },
            )
        ],
        style={
            "margin": "0 15px"
        }
    )

app.layout = main

if __name__ == '__main__':
    app.run_server(debug=True)