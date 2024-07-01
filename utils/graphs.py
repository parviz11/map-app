import geopandas as gpd
import json, os
import plotly.express as px
import plotly.graph_objects as go
from . import conversion

# Get the root directory (parent of the current directory)
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

#Main map
def main_map(df):

    customdata = list(
        zip(
            df["country"],
            df["partner"],
            df["product"],
            df["gender"],
            df['age'],
            df['income']
            
        ))

    mapbox_figure = go.Figure(go.Scattermapbox(
        lat=df["latitude"],
        lon=df["longitude"],
        marker=dict(size=7, opacity=0.7, color="#006400"),
        customdata=customdata,
        hovertemplate="<b>%{customdata[1]}</b><br>"
                      "%{customdata[2]}<br>"
                      "%{customdata[3]}"
                      "<extra></extra>",
    ))

    mapbox_figure.update_layout(
        mapbox=dict(
            style="open-street-map",
            uirevision=True,
            zoom=6,
            center=dict(
                lon=12.00,
                lat=57.67,
            ),
        ),
        margin=dict(l=0, t=0, b=0, r=0),
        height=780,
        showlegend=False,
        hovermode="closest"
    )

    return mapbox_figure

#Age histogram in one graph
def age_hist(df,*args):
    fig = px.histogram(df, x="age", color="gender",
                   
                   hover_data=['age','country'],
                  color_discrete_map = {'F':'lightcoral','M':'deepskyblue'})
    if len(args)>0:
        fig.add_vline(x=args[0], line_width=3, line_dash="dash", line_color="green",
                      annotation_text=str(args[1]), annotation_position="top left",
                      annotation=dict(font_size=14, 
                                        font_family="Times New Roman",
                                        bordercolor="#c7c7c7",
                                        borderwidth=2,
                                        borderpad=4,
                                        bgcolor="#ff7f0e",
                                        opacity=0.8))    
    fig.update_layout(
                margin=dict(l=10, r=20, t=70, b=20),
                title_text="Age distribution"
    )

    return fig


#Income histogram in one graph
def inc_hist(df,*args):
    fig = px.histogram(df, x="income", color="gender",
                   
                   hover_data=['age','country'],
                  color_discrete_map = {'F':'orangered','M':'dodgerblue'})
    if len(args)>0:
        fig.add_vline(x=args[0], line_width=3, line_dash="dash", line_color="green",
                      annotation_text=str(args[1]), annotation_position="top left",
                      annotation=dict(font_size=14, 
                                        font_family="Times New Roman",
                                        bordercolor="#c7c7c7",
                                        borderwidth=2,
                                        borderpad=4,
                                        bgcolor="#ff7f0e",
                                        opacity=0.8)) 
    fig.update_layout(
                margin=dict(l=10, r=20, t=70, b=20), #this defines margins around the graph. by default margins are large and affect graph positioning.
                title_text="Income distribution"
    )

    return fig


# Polygon layer, urban areas borders:
def polygon_layer():
    # Read data
    # Construct the path to the data file
    parquet_path = os.path.join(root_dir, 'data', 'tatorter_1980_2020.parquet')

    # Create a GeoDataFrame from the list of dictionaries
    gdf = gpd.read_parquet(parquet_path)

    # Convert to geojson
    geojson_data = gdf.to_json()

    # Parse the GeoJSON string
    geojson_obj = json.loads(geojson_data)

    # Create the polygon layer
    layer_data = go.Choroplethmapbox(geojson=geojson_obj,
                                    locations=gdf['TATORTSKOD'],
                                    z=gdf['BEF'],
                                    colorscale="Viridis",
                                    zmin=gdf['BEF'].min(),
                                    zmax=gdf['BEF'].max(),
                                    featureidkey='properties.TATORTSKOD',
                                    marker_opacity=0.5,
                                    colorbar=dict(title='Population'),
                                    )
    return layer_data