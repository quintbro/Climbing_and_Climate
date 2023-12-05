import pandas as pd
import folium
from folium.plugins import MarkerCluster
from folium.plugins import HeatMap


def clus_map(df, lat = 'Latitude', lon = 'Longitude', desc = 'Description', name = 'cluster_map', save = True):
    '''Create an interactive map of climbs with the desired description/attribute

    Parameters
    ==========
    df : pandas dataframe
        The Dataframe must include a latitude and longitude column

    lat : str, default = "Latitude"
        This is the name of the column in df that contains the latitude
    
    lon : str, default = "Longitude"
        This is the name of the column in df that contains the longitude
    
    desc : str, default = "Description"
        This is the name of the column in df that you want each point on the graph to display
        You can also think of this as an attribute

    name : str, default = "cluster_map"
        This is the name of the html file that you want to write the map out to

    save : boolean, default = True
        When set to True, it will write out the map to an html file, when set to False,
        the function will return the map as a folium map object

    Returns
    =======
    folium map object

    Notes
    =====
    By default the function will return nothing, if you set save = False, it will return a folium map object

    Example
    =======
    This example uses the data that can be loaded using the load_data function and 

    >>> import pyclimb as pc
    >>> from pyclimb.vis_func import clus_map
    >>> clus_map(pc.load_data("clean"), lat = "Area Latitude", lon = "Area Longitude", desc = "Route")
    
    '''
    # Rename the df to correct column names
    df = df.rename(columns={lat: 'Latitude', lon: 'Longitude', desc: 'Description'})
    
    map_center = [df['Latitude'].mean(), df['Longitude'].mean()]
    map = folium.Map(location=map_center, zoom_start=6.5)

    # Create a MarkerCluster object
    marker_cluster = MarkerCluster().add_to(map)

    # Add markers to the map using data from the DataFrame
    for index, row in df.iterrows():
        folium.Marker([row['Latitude'], row['Longitude']], popup=row['Description'], icon=folium.Icon(prefix='fa', icon='star')).add_to(marker_cluster)

    # Save the map as an HTML file
    if save:
        map.save(f'{name}.html')
    else:
        return map

def heat_map (df, lat = 'Latitude', lon = 'Longitude', desc = 'Description', name = 'heat_map', save = True):
    '''Create a heat map of climbs with the desired description/attribute

    Parameters
    ==========
    df : pandas dataframe
        The Dataframe must include a latitude and longitude column

    lat : str, default = "Latitude"
        This is the name of the column in df that contains the latitude
    
    lon : str, default = "Longitude"
        This is the name of the column in df that contains the longitude
    
    desc : str, default = "Description"
        This is the name of the column in df that you want each point on the graph to display
        You can also think of this as an attribute

    name : str, default = "heat_map"
        This is the name of the html file that you want to write the map out to

    save : boolean, default = True
        When set to True, it will write out the map to an html file, when set to False,
        the function will return the map as a folium map object

    Returns
    =======
    folium map object

    Notes
    =====
    By default the function will return nothing, if you set save = False, it will return a folium map object

    Example
    =======
    This example uses the data that can be loaded using the load_data function and 

    >>> import pyclimb as pc
    >>> from pyclimb.vis_func import heat_map
    >>> heat_map(pc.load_data("clean"), lat = "Area Latitude", lon = "Area Longitude", desc = "Route")
    
    '''
    # Rename the df to correct column names
    df = df.rename(columns={lat: 'Latitude', lon: 'Longitude', desc: 'Description'})
    
    # Convert df into readable data and create heatmap
    data = df[['Latitude', 'Longitude']].values.tolist()
    map_center = [df['Latitude'].mean(), df['Longitude'].mean()]
    heat_map = folium.Map(location=map_center, zoom_start=6.5)
    HeatMap(data).add_to(heat_map)
    
    # Save the map as an HTML file
    if save:
        map.save(f'{name}.html')
    else:
        return map