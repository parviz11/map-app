import plotly.express as px

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

    mapbox_figure = dict(
        type="scattermapbox",
        lat=df["latitude"],
        lon=df["longitude"],
        marker=dict(size=7, opacity=0.7, color="#006400"),
        #cluster=dict(color='#8BC8AA',opacity=0.9),
        customdata=customdata,
        hovertemplate=
        "<b>%{customdata[1]}</b><br>"
        "%{customdata[2]}<br>"
        "%{customdata[3]}"
        "<extra></extra>",    
    )

    layout = dict(
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

    figure = {"data": [mapbox_figure], "layout": layout}

    return figure

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