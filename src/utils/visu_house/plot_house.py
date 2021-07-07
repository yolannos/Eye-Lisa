import rasterio
import rasterio.mask
import plotly.graph_objects as go
import fiona
import numpy as np
import pandas as pd
import pathlib

#import house
def plot_house(chm, house_coordinates):
    '''
    Return fig to plot inside the streamlit app
    '''
    data = rasterio.open(chm)
    xMin, yMin, xMax, yMax = data.bounds

    z_data = pd.DataFrame(data.read(1))
    z_data.index   = list(range(int(yMax), int(yMin), -1))
    z_data.columns = list(range(int(xMin), int(xMax)))
    z_data = z_data.applymap(lambda x: 0.5 if x < 1 else round(x, 1))


    fig = go.Figure(go.Surface(z=z_data.values, x=z_data.columns, y=z_data.index, opacity=1))

    l, b = house_coordinates[0], house_coordinates[1]
    r, t = house_coordinates[0], house_coordinates[1]

    ## TO PLOT THE AREA SPECIFIC TO THE ADDRESS FROM THE 3D BUILDINGS FILE
    with fiona.open("dataset/3d_objects/Shapefile/GRBGebL1D2.shp", "r") as shapefile:
        
        for feature in shapefile.filter(bbox=(l, b, r, t)):
            
            ### WITHOUT TRACE
            _ = feature["geometry"]["coordinates"][0]
            data_xy = np.array(_)
            height = np.full(len(data_xy), feature["properties"]["HN_MAX"] )
            # base = np.full(len(data_xy), 0.5)
            df_up = pd.DataFrame(data_xy, columns=["x","y"])
            df_up["z"] = height.tolist()
            # df_down = pd.DataFrame(data_xy, columns=["x","y"])
            # df_down["z"] = base.tolist()
            
        #     df = pd.concat([df_up, df_down],axis = 0)

            # #WITH TRACE
            # data_ = np.array(feature["geometry"]["coordinates"][0])
            # x_, y_ = map(list,zip(*data_))
            # df = pd.DataFrame(index = x_, columns = y_)
            # df.loc[:,:] = feature["properties"]["HN_MAX"]
            # # fig.add_scatter3d(y=df.columns, x=df.index, z=df.values, mode='lines',showlegend=True, line=dict(color='red', width=10))
            

            # fig2 = go.Figure(data=[go.Surface(y=df.columns, x=df.index, z=df.values)])
            
            fig.add_scatter3d(x=df_up['x'], y=df_up['y'], z=df_up["z"], surfaceaxis= -1, mode='lines',showlegend=False, line=dict( width=5))
        #     print(df)

#     fig.add_trace(fig2)
    fig.update_layout(
            width=900,
            height=1000,
            margin=dict(t=40, r=0, l=0, b=40),
            scene = {"xaxis": {'showspikes': False},
                    "yaxis": {'showspikes': False},
                    "zaxis": {'showspikes': False},
                    'camera_eye': {"x": 0, "y": -0.5, "z": 0.5},
                    "aspectratio": {"x": 1, "y": 1, "z": 0.1}
                    })

    return fig