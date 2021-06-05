# -*- coding: utf-8 -*-

import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import tensorflow as tf

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
# Load dataframe with simulation results
df = pd.read_csv("tmp/df.csv",index_col=0)
# Load the trained NN model
model = tf.keras.models.load_model('tmp/model')

# Define the basic app layout
app.layout = html.Div([
                html.H1("Flow around triangles"),
                html.Div([
                    html.P("Select x1:"),
                    dcc.Slider(
                            id='x1-slider',
                            min=df["x1"].min(),
                            max=df["x1"].max(),
                            step=0.5,
                            marks = {i: str(i) for i in df["x1"]},
                            value=df["x1"][0],
                        ),
                ],className="left-float"),
                html.Div([
                    html.P("Select y1:"),
                    dcc.Slider(
                            id='y1-slider',
                            min=df["y1"].min(),
                            max=df["y1"].max(),
                            step=0.5,
                            marks = {i: str(i) for i in df["y1"]},
                            value=df["y1"][0],
                        ),
                ],className="left-float"),
                html.Div([
                    html.P("Select x2:"),
                    dcc.Slider(
                            id='x2-slider',
                            min=df["x2"].min(),
                            max=df["x2"].max(),
                            step=0.5,
                            marks = {i: str(i) for i in df["x2"]},
                            value=df["x2"][0],
                        ),
                ],className="left-float"),
                html.Div([
                    html.P("Select y2:"),
                    dcc.Slider(
                            id='y2-slider',
                            min=df["y2"].min(),
                            max=df["y2"].max(),
                            step=0.5,
                            marks = {i: str(i) for i in df["y2"]},
                            value=df["y2"][0],
                        ),
                ],className="left-float"),
                html.Div([
                    html.P("Select x3:"),
                    dcc.Slider(
                            id='x3-slider',
                            min=df["x3"].min(),
                            max=df["x3"].max(),
                            step=0.5,
                            marks = {i: str(i) for i in df["x3"]},
                            value=df["x3"][0],
                        ),
                ],className="left-float"),
                html.Div([
                    html.P("Select y3:"),
                    dcc.Slider(
                            id='y3-slider',
                            min=df["y3"].min(),
                            max=df["y3"].max(),
                            step=0.5,
                            marks = {i: str(i) for i in df["y3"]},
                            value=df["y3"][0],
                        ),
                ],className="left-float"),
                html.Div([
                    dcc.Graph(
                        id="triangle-graph",
                        figure=go.Figure()
                    ),
                    dcc.Graph(
                        id="re-graph",
                        figure=go.Figure()
                    ),
                    # Optional time graph
                    # dcc.Graph(
                    #     id="time-graph",
                    #     figure=go.Figure()
                    # ),
                ],className="full-with clear-float"),
            ],id="content")

@app.callback(
    [dash.dependencies.Output('triangle-graph','figure'),
     dash.dependencies.Output('re-graph','figure'),
     #dash.dependencies.Output('time-graph','figure')
    ],
    [
    #dash.dependencies.Input('re-graph','clickData'),
    dash.dependencies.Input('x1-slider','value'),
    dash.dependencies.Input('y1-slider','value'),
    dash.dependencies.Input('x2-slider','value'),
    dash.dependencies.Input('y2-slider','value'),
    dash.dependencies.Input('x3-slider','value'),
    dash.dependencies.Input('y3-slider','value')]
)
def update_scatter(sel_x1,sel_y1,sel_x2,sel_y2,sel_x3,sel_y3):
    # Create a figure that displays the triangle that the user selected
    triangle_fig = go.Figure(go.Scatter(x=[sel_x1,sel_x2,sel_x3,sel_x1],y=[sel_y1,sel_y2,sel_y3,sel_y1]))
    triangle_fig.update_xaxes(range=[0, 60])
    triangle_fig.update_yaxes(range=[0, 40])
    for i in np.arange(1,8):
        triangle_fig.add_annotation(x=7, y=5*i, ax=-30, ay=0,
                text="",
                showarrow=True,
                arrowhead=1)
    x = [200,400,600]
    re_fig = go.Figure()
    # Get the model prediction for the chosen triangle and add a trace to the
    # second figure
    model_Cd = model.predict(x=[[sel_x1,sel_y1,sel_x2,sel_y2,sel_x3,sel_y3]])
    re_fig.add_trace(go.Scatter(x=x,y=model_Cd[0],name="Model prediction"))
    try:
        # Try if the same triangle was already in the training dataset
        y0 = float(df["mean Cd 200"][(df["x1"] == sel_x1) & (df["y1"] == sel_y1) & (df["x2"] == sel_x2) & (df["y2"] == sel_y2) & (df["x3"] == sel_x3) & (df["y3"] == sel_y3)])
        y1 = float(df["mean Cd 400"][(df["x1"] == sel_x1) & (df["y1"] == sel_y1) & (df["x2"] == sel_x2) & (df["y2"] == sel_y2) & (df["x3"] == sel_x3) & (df["y3"] == sel_y3)])
        y2 = float(df["mean Cd 600"][(df["x1"] == sel_x1) & (df["y1"] == sel_y1) & (df["x2"] == sel_x2) & (df["y2"] == sel_y2) & (df["x3"] == sel_x3) & (df["y3"] == sel_y3)])
        y = [y0,y1,y2]
        # If so add it to the figure for comparison
        re_fig.add_trace(go.Scatter(x=x,y=y,name="CFD calculation"))
    except Exception:
        # Otherwise do nothing
        pass
    # Add axis labels and activate the legend
    re_fig.update_layout(
        xaxis_title="Reynolds number",
        yaxis_title="Drag coefficient",
        showlegend=True
    )
    # Optional add possibility to observe the simulation data by clicking
    # on point in Re plot.
    # if clickData:
    #     sel_Re = clickData["points"][0]["x"]
    #     print("{}".format(sel_x1))
    #     selected_result = all_data[(x1 == sel_x1) & (y1 == sel_y1) & (x2 == sel_x2) & (y2 == sel_y2) & (x3 == sel_x3) & (y3 == sel_y3) & (Re == sel_Re)]
    #     time_fig = go.Figure(go.Scatter(x=selected_result["# Time"],y=50*selected_result["Cd"]))
    # else:
    #     time_fig = go.Figure()
    return triangle_fig, re_fig

if __name__ == '__main__':
    app.run_server(debug=True)
