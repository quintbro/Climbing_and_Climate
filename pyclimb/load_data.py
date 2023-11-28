import pkg_resources
import pandas as pd

def load_data(type = "clean", which = [1,2,3,4,5,6,7,8]):
    if type == 'clean':
        path_to_data = "data/utah_climbs.csv"
    elif type == "weather":
        path_to_data = "data/Utah_Weather_Stations.csv"
    if type == 'raw':
        str_num = [str(i) for i in which]
        paths = ['data/route-finder_' + num  + '.csv' for num in which]
        list = []
        for file in paths:
            data_path = pkg_resources.resource_filename("pyclimb", file)
            list.append(pd.read_csv(data_path))
            return list
    
    file_path = pkg_resources.resource_filename("pyclimb", path_to_data)

    return pd.read_csv(file_path)