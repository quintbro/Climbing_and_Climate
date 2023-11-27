import pandas as pd
from scipy.spatial import cKDTree

def merge_data_dist(df1, df2, keep_col, lat = 'Latitude', lon = 'Longitude'):
    # Rename the df to correct column names
    df1 = df1.rename(columns={lat: 'Latitude', lon: 'Longitude'})
    df2 = df2.rename(columns={lat: 'Latitude', lon: 'Longitude'})
    
    # Create KDTree for df2
    tree = cKDTree(df2[['Latitude', 'Longitude']])
    
    # Function to find closest point in df2 for each row in df1
    def find_closest(row):
        distance, index = tree.query([row['Latitude'], row['Longitude']])
        closest_data = df2.iloc[index]
        return pd.Series({keep_col: closest_data[keep_col], 'Distance': distance})

    # Apply the function to each row in df1
    closest = df1.apply(find_closest, axis=1)
    
    # Combine the results with df1
    merged = pd.concat([df1, closest], axis=1)

    return merged