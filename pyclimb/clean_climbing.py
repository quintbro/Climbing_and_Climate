import pandas as pd
import numpy as np

def concat(list_of_files, path = ""):
    '''
    
    This function takes a list of .csv files as an argument and returns a 
    dataframe with the dataframes pulled from each file concatenated together
    vertically

    Parameters
    ==========
    list_of_files : list of strings
        The names of the files that you want to be concatentated together
    path : string
        There is an optional path argument which specifies the path if the data is not located 
        in the same directory as your script. if path is specified, inlude a '/' at the end of the script
        for example path = "data/" if the .csv files are located in a directory called "data" within
        your environment.

    Returns
    =======
    pandas dataframe
        A concatenated dataframe of the files that you specify in the list_of_files arguement
    '''

    if isinstance(list_of_files, list):
        check = True
    else:
        print("ERROR: 'list_of_files' must be a list")
        return -1
    route_finder_list = [pd.read_csv(path + climb) for climb in list_of_files]
    climbs = pd.concat(route_finder_list).reset_index()
    return climbs.drop('index', axis = 1)


def clean(df, inplace = False):
    '''
    Parameters
    ==========
    df: pandas dataframe
        This is a pandas data frame that can be obtained by downloading .csv files from 
        mountainproject.com and using the dataConcat function also found in this module
    inplace: boolean
        setting this equal to true will change the data frame that you pass in.
        setting equal to false will return a modified copy

    Returns
    =======
    pandas dataframe
        A cleaned pd.dataframe object as follows:

        This function will change "Rating" into two boolean factors, one for PG13 and one for R
        It will separate the Location column into 5 different columns called 
        "State", "Region", "Location", "Crag", and "Wall"

        it will change "Route Type" into separate boolean columns for each type namely
        'Trad', 'Alpine', 'TR', 'Aid', 'Boulder', 'Mixed' and 'Sport'

        Creates an encoding for the YSD ratings called Rating_num
        The encoding is as follows:
        'a', 'a/b', '-', 'b', 'b/c', '', 'c', 'c/d', '+', 'd' are mapped to 
        '.2', '.3', '.3', '.4', '.5', '.5', '.6', '.7', '.7', '.8' respectively
        and the first number remains the same and the 5 is dropped.

        NOTE: This does not create anything for boulder or ice/mixed or any other rating system
        it only uses the YSD

        Lastly this function will convert any values that are -1 in the Rating column 
        to np.NaN values
    '''
    if isinstance(df, pd.DataFrame):
        isdf = True
    else:
        print("ERROR: df must be given a pandas dataframe")
        return -1
    
    if inplace == True:
        climbs = df
    else:
        climbs = df.copy()
    
    # This Code creates two boolean factors for whether the climb is rated PG13 or R
    pg13 = climbs.Rating.str.extract("(PG13)")
    R = climbs.Rating.str.extract("(R)")
    climbs["PG13"] = pg13 == "PG13"
    climbs["R"] = R == "R"

    # Remove PG13 and R from the "Rating" column
    climbs["Rating"] = climbs.Rating.str.replace("(PG13|R)", "", regex = True)

    # This Code Separates out the "Location" column into "State", "Region", "Location", "Crag", and "Wall"
    locs = climbs.Location.apply(lambda x : x[::-1]).str.extract("([A-Za-z1-9& ]*)>*([A-Za-z1-9& ]*)>*([A-Za-z1-9 &]*)>*([A-Za-z1-9& ]*)>*([A-Za-z1-9& ]*)")
    locs["State"] = locs[0].apply(lambda x : x[::-1]).apply(lambda x : x.strip())
    locs["Region"] = locs[1].apply(lambda x : x[::-1]).apply(lambda x : x.strip())
    locs["Location"] = locs[2].apply(lambda x : x[::-1]).apply(lambda x : x.strip())
    locs["Crag"] = locs[3].apply(lambda x : x[::-1]).apply(lambda x : x.strip())
    locs["Wall"] = locs[4].apply(lambda x : x[::-1]).apply(lambda x : x.strip())

    # This Adds the new variables into the dataframe and drops "index" and "Your Stars"
    climbs.drop(["Location"], axis=1, inplace=True)
    climbs[["State", "Region", "Location", "Crag", "Wall"]] = locs.drop([0, 1, 2, 3, 4], axis=1).replace("", np.NaN)
    climbs.drop(["Your Stars"], axis=1, inplace=True)
    climbs.drop(["index"], axis = 1, inplace = True)

    # This data set contains only climbs marked as 'Sport' but some climbs were marked as Sport/Trad, Sport/TR, etc. or even
    # Sport/Trad/TR and so this makes a new variable as a boolean, true for if the type contained the column name in addition to sport
    # And drops the "Route Type" Feature.
    type_names = ['Trad', 'Alpine', 'TR', 'Aid', 'Boulder', 'Mixed', 'Sport']
    for type in type_names:
        climbs[type] = climbs['Route Type'].str.extract('(' + type + ')') == type

    climbs.drop('Route Type', axis = 1, inplace = True)

    # Remove extra ratings to leave only the YSD system
    climbs['Rating'] = climbs.Rating.str.extract("(5\.[0-9]{1,2}[a-d/\-+]{0,3})")

    # Creates a dictionary mapping the YSD grades to numbers so that we can encode them
    ratings = {}
    rating_num = ['.2', '.3', '.3', '.4', '.5', '.5', '.6', '.7', '.7', '.8']
    grades = ['a', 'a/b', '-', 'b', 'b/c', '', 'c', 'c/d', '+', 'd']

    for i in ['5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15']:
        for j in range(len(grades)):
            grade = '5.' + i + grades[j]
            numGrade = i + rating_num[j]
            ratings[grade] = numGrade

    climbs['Rating_num'] = climbs.Rating.replace(ratings).astype(float)

    # convert any climbs that had a rating of -1 to NaN values
    climbs['Avg Stars'].mask(climbs['Avg Stars'] == -1, np.nan, inplace = True)

    return climbs