import pandas as pd
import folium
from folium.plugins import MarkerCluster


def clus_map(df, lat = 'Latitude', lon = 'Longitude', desc = 'Description', name = 'cluster_map', save = True):
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
    