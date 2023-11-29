import pkg_resources
import pandas as pd
from pyclimb.clean_climbing import concat

def load_data(type = "clean", which = [1,2,3,4,5,6,7,8]):
    '''
    This function loads in preloaded datasets

    Parameters
    ==========
    type : string
        Options are 'clean', 'raw', or 'weather' 
        'clean' - this is a data set of all of the outdoor sport climbs in Utah from the 
            mountain project database as of October 2023 
        'raw' - this is the files that the 'clean' data came from, there are 8 different 
            files the default is to return a single data frame with all 8 files, but you can 
            request  any one of the files by specifying the argument which 
        'weather' this is climate data taken from Utah Weather Stations

    which : list of ints (1-8)
        This arguement specifies which of the data files you want if you select the 'raw' option.
    '''
    if type == 'clean':
        path_to_data = "data/utah_climbs.csv"
    elif type == "weather":
        path_to_data = "data/Utah_Weather_Stations.csv"
    elif type == 'raw':
        str_num = [str(i) for i in which]
        paths = ['data/route-finder_' + num  + '.csv' for num in str_num]
        actual_path = [pkg_resources.resource_filename("pyclimb", file) for file in paths]
        return concat(actual_path)
    else:
        print("ERROR: please use a valid type 'clean', 'raw', or 'weather'")
        return -1
    
    file_path = pkg_resources.resource_filename("pyclimb", path_to_data)

    return pd.read_csv(file_path)