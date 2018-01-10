import plotly.plotly as py
import plotly.graph_objs as go
import pandas as pd
import numpy as np

mapbox_access_token = 'pk.eyJ1Ijoic2ViYXN0aWFuYmVydG9saSIsImEiOiJjamI3MDd2MzEwdTcxMndxenlxeG84MW84In0.NGEBEkX3qU7NFDw31j56AQ'

def plot_datasample(df_plotting):
    '''
    Initial plot showing some datapoints on the map.

    Parameters:
    -- Pandas dataframe containing latitude-longitude columns.

    Returns:

    '''
    fig = go.Figure(data = [go.Scattermapbox(lat=df_plotting["latitude"],
                                            lon=df_plotting["longitude"],
                                            mode='markers',
                                            text="User ID: " + df_plotting["user_id"].apply(str),
                                            textposition='bottom',
                                            marker=go.Marker(size=3,opacity = 0.3))
                            ],
                    layout = go.Layout(autosize=False,
                                    width=680,
                                    height=340,
                                    margin=go.Margin(
                                        l=0,
                                        r=0,
                                        b=0,
                                        t=0,
                                        pad=0),
                                    hovermode='closest',
                                    mapbox=dict(
                                        accesstoken=mapbox_access_token,
                                        bearing=0,
                                        center=dict(
                                            lat=df_plotting["latitude"].median(),
                                            lon=df_plotting["longitude"].median()),
                                    pitch=0,
                                    style='light',
                                    zoom=9.5)))
    return fig

def plot_one_user(df_plotting):
    '''
    Initial plot showing some datapoints on the map.

    Parameters:
    -- Pandas dataframe containing latitude-longitude columns.

    Returns:

    '''
    fig = go.Figure(data = [go.Scattermapbox(lat=df_plotting["latitude"],
                                            lon=df_plotting["longitude"],
                                            mode='markers+text',
                                            text=("Time: " 
                                                  + df_plotting["timestamp"].dt.hour.apply(str)
                                                  + ":" 
                                                  + df_plotting["timestamp"].dt.minute.apply(str).str.zfill(2)), 
                                            textposition='bottom',
                                            marker=go.Marker(size=14,opacity = 0.7))
                            ],
                    layout = go.Layout(autosize=False,
                                       width=680,
                                       height=340,
                                       margin=go.Margin(l=0, r=0, b=0, t=0, pad=0),
                                       hovermode='closest',
                                       mapbox=dict(accesstoken=mapbox_access_token,
                                                   bearing=0,
                                                   center=dict(lat=df_plotting["latitude"].mean(),lon=df_plotting["longitude"].mean()),
                                                   pitch=0,
                                                   style='light',
                                                   zoom=15
                                                  ),
                                    #    annotations=[dict(x=116.3432,
                                    #                      y=39.92548,
                                    #                      xref='x',
                                    #                      yref='y',
                                    #                      text='Hello',
                                    #                      showarrow=True,
                                    #                      arrowhead=7,
                                    #                      ax=-10,
                                    #                      ay=-10
                                    #                     )
                                    #                 ]
                                       )
                    )
    return fig

def plot_stops(df_plotting):
    fig = go.Figure(data = [go.Scattermapbox(lat=df_plotting["latitude"],
                                            lon=df_plotting["longitude"],
                                            mode='markers',
                                            text="User ID: " + df_plotting["user_id"].apply(str),
                                            textposition='bottom',
                                            marker=go.Marker(size=5,opacity = 1, color='orange'))
                            ],
                    layout = go.Layout(autosize=False,
                                    width=680,
                                    height=340,
                                    margin=go.Margin(
                                        l=0,
                                        r=0,
                                        b=0,
                                        t=0,
                                        pad=0),
                                    hovermode='closest',
                                    mapbox=dict(
                                        accesstoken=mapbox_access_token,
                                        bearing=0,
                                        center=dict(
                                            lat=df_plotting["latitude"].median(),
                                            lon=df_plotting["longitude"].median()),
                                    pitch=0,
                                    style='light',
                                    zoom=9.5)))
    return fig

def plot_destinations(df_plotting):
    df_plotting = df_plotting.sort_values(by='count')
    sizes = np.sqrt(df_plotting['count']) + 3
    cluster_colors = np.log(df_plotting['count'])
    fig = go.Figure(data = [go.Scattermapbox(lat=df_plotting["latitude"],
                                            lon=df_plotting["longitude"],
                                            mode='markers',
                                            text="User ID: " + df_plotting["user_id"].apply(str) 
                                                 + "<br>Destination ID: " + df_plotting["cluster_assignment"].apply(str)
                                                 + "<br># Stops: " + df_plotting["count"].apply(str),
                                            textposition='bottom',
                                            marker=go.Marker(size=sizes,
                                                            opacity = 1, 
                                                            color=cluster_colors))
                            ],
                    layout = go.Layout(autosize=False,
                                    width=680,
                                    height=340,
                                    margin=go.Margin(
                                        l=0,
                                        r=0,
                                        b=0,
                                        t=0,
                                        pad=0),
                                    hovermode='closest',
                                    mapbox=dict(
                                        accesstoken=mapbox_access_token,
                                        bearing=0,
                                        center=dict(
                                            lat=df_plotting["latitude"].median(),
                                            lon=df_plotting["longitude"].median()),
                                    pitch=0,
                                    style='light',
                                    zoom=9.5)))
    return fig