import pandas as pd
from scipy.spatial import cKDTree

def merge_data_dist(df1, df2, keep_col, lat1 = 'Latitude', lon1 = 'Longitude', lat2 = 'Latitude', lon2 = 'Longitude'):
    ''' Function to merge a dataframe containing latitude and longitude with 
    the climbing dataframe
    
    Parameters
    ==========
    df1 : Pandas dataframe
        Left dataframe that you want to join. All rows will be kept

    df2 : Pandas dataframe
        Right dataframe that you want to join. Not all of the rows in this dataframe will
        necessarily be joined with df1.
    
    keep_col : str
        name of the column from df2 that you want to join to df1

    lat1 : str, default = "Latitude"
        the name of the latitude column in df1
    
    lon1 : str, default = "Longitude"
        The name of the longitude column in df1
    
    lat2 : str, default = "Latitude"
        the name of the latitude column in df2
    
    lon2 : str, default = "Longitude"
        The name of the longitude column in df2
    
    Notes
    =====
    1. this will perform a left join, meaning that all of the columns in df1 will
    be kept but not all of the columns in df2 will necessarily be kept

    2. This assumes that df1 has column names "Latitude" and "Longitude". Otherwise, the name of those columns 
    *must* be the same names as df2 which is specified by the lat and lon arguements
    '''
    # Rename the df to correct column names
    df1 = df1.rename(columns={lat1: 'Latitude', lon1: 'Longitude'})
    df2 = df2.rename(columns={lat2: 'Latitude', lon2: 'Longitude'})
    
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