import pandas as pd
import numpy as np

# Creates a list of strings that match the files in the directory
nums = [str(num) for num in range(1, 9)]
data = ["route-finder_" + i + ".csv" for i in nums]

# Creates a list of dataframes, one for each .csv file in the directory
route_finder_list = [pd.read_csv(climb) for climb in data]

# Stacks all of the dataframes to make one big dataframe
climbs = pd.concat(route_finder_list).reset_index()

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
type_names = ['Trad', 'Alpine', 'TR', 'Aid', 'Boulder', 'Mixed']
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

# Write out the cleaned version of the climbing data so that I have a csv with all of the data in it 
climbs.to_csv("utah_climbs.csv", index = False)