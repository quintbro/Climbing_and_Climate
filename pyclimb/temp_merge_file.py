import pandas as pd
from scipy.spatial import cKDTree

def merge_data_dist(df1, df2, keep_col, lat = 'Latitude', lon = 'Longitude'):
    '''
    df1: Left data frame that you want to join 
    NOTE: this will perform a left join, meaning that all of the columns in df1 will
    be kept but not all of the columns in df2 will necessarily be kept

    df2: Right data frame that you want to join
    
    keep_col: name of the column from df2 that you want to join to df1

    lat and lon: the name of the latitude and longitude column for df2
    NOTE: This assumes that df1 has column names "Latitude" and "Longitude"
    respectively. Otherwise, the name of those columns must be the same names as
    df2 which is specified by the lat and lon arguements
    '''
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