# Demo

## Packages to Install
Please install the following additional packages, prior to running the demo:
* sklearn:
```
        pip install -U scikit-learn
```

* category_encoders:
```
        pip install category_encoders
```


```python
import pyclimb as pc
from pyclimb.vis_func import clus_map, heat_map
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from category_encoders import TargetEncoder
from sklearn.ensemble import RandomForestRegressor # For the weighted linear regression
import seaborn as sns
```

## Loading and Cleaning
First, use the load_data function to load in the preloaded datasets for the demo. The preloaded datasets include the climbing dataset both in clean, and in raw form, a weather dataset from Utah weather stations, and a Utah cities dataset scraped from the web. For this demo, we are using the raw form of the data set, to demonstrate how to use the built in cleaning function.

If reading in your own data from mountainproject.com. Put all of your files in the same working directory and use the pc.concat() function.


```python
# if using your own files dowloaded from mountain project,then uncomment this code
# climbs = pc.concat(['route-finder(1).csv', 'route-finder(2).csv', 'route-finder(3).csv'])
climbs = pc.load_data('raw')
weather = pc.load_data('weather')
cities = pc.load_data('cities')
```

You can then clean the data using the pc.clean() function.


```python
pc.clean(climbs, inplace = True)
```

## Scraping
Additionally, there is a scraper function that will collect additional data from each climb, the crawl-delay requested by mountain project.com, is 60 seconds, so for the purposes of this demo, I will leave it commented out, but if you are using your own data feel free to uncomment it.


```python
# pc.scrape_mp(climbs, inplace = True) # uncomment this section to scrape from MP
# I have already scraped the data from MP and it is in the clean dataset below
climbs = pc.load_data('clean')
```

## Merging the data
Once you have your cleaned data, use merge_data_dist to merge the desired dataframes based on the closest latitude and longitude. This example merges the climbs dataset with two others, weather stations and cities


```python
climbing = pc.merge_data_dist(climbs, weather, 'ELEVATION', 'Area Latitude', 'Area Longitude', 'LATITUDE', 'LONGITUDE')
# function adds distance variable by default, so we rename it to be more specific
climbing.rename({'Distance' : 'station_dist', 'Location' : 'climb_location'}, inplace = True, axis = 1) 
climbing = pc.merge_data_dist(climbing, cities, 'Location')
climbing.rename({'Distance' : 'city_dist', 'Location' : 'city'}, inplace = True, axis = 1)

climbing.info()
```

    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 6107 entries, 0 to 6106
    Data columns (total 34 columns):
     #   Column          Non-Null Count  Dtype  
    ---  ------          --------------  -----  
     0   Route           6107 non-null   object 
     1   URL             6107 non-null   object 
     2   Avg Stars       6062 non-null   float64
     3   Rating          6107 non-null   object 
     4   Pitches         6107 non-null   int64  
     5   Length          5474 non-null   float64
     6   Latitude        6107 non-null   float64
     7   Longitude       6107 non-null   float64
     8   PG13            6107 non-null   bool   
     9   R               6107 non-null   bool   
     10  State           6107 non-null   object 
     11  Region          6107 non-null   object 
     12  climb_location  6107 non-null   object 
     13  Crag            5874 non-null   object 
     14  Wall            4702 non-null   object 
     15  Trad            6107 non-null   bool   
     16  Alpine          6107 non-null   bool   
     17  TR              6107 non-null   bool   
     18  Aid             6107 non-null   bool   
     19  Boulder         6107 non-null   bool   
     20  Mixed           6107 non-null   bool   
     21  Rating_num      6107 non-null   float64
     22  numVotes        6107 non-null   int64  
     23  numViews        6107 non-null   int64  
     24  Year            6107 non-null   int64  
     25  ViewsPerMonth   6107 non-null   int64  
     26  Shared_by       6107 non-null   object 
     27  Month           6107 non-null   int64  
     28  Day             6107 non-null   int64  
     29  Date            6107 non-null   object 
     30  ELEVATION       6107 non-null   object 
     31  station_dist    6107 non-null   float64
     32  city            6107 non-null   object 
     33  city_dist       6107 non-null   float64
    dtypes: bool(8), float64(7), int64(7), object(12)
    memory usage: 1.3+ MB
    

## Maps
Once the datasets are merged, you can make an interactive cluster or heat map. This uses the latitude, longitude, and a description for each point. These maps save by default but can be printed to screen instead by using save = False.


```python
clus_map(climbing, desc = 'Route')
```


```python
heat_map(climbing, desc = 'Avg Stars')
```

## Analysis
Here we use scikit-learn to create a random forest model and predict the Rating_num.


```python
# Change Elevation to a float
climbing['ELEVATION'] = climbing.ELEVATION.mask(climbing['ELEVATION'] == " ", np.nan).astype(float)

# Drop na values
climbing.dropna(inplace = True)

# Change Booleans to 1 and 0
for col in ['R', 'PG13', 'Trad', 'Alpine', 'TR', 'Aid', 'Boulder', 'Mixed']:
    climbing[col] = climbing[col].map({True : 1, False : 0})

# Target encode categorical features
label_encoder = LabelEncoder()
categorical_variables = ['Region', 'climb_location', 'Crag', 'Wall', 'city']
for var in categorical_variables:
    climbing[var] = label_encoder.fit_transform(climbing[var])

# fit the model
X = climbing.drop(['Rating_num', 'URL',             # Remove uninformative features
                   'Route', 'Rating', 'Shared_by', 
                   'State', 'Date'], axis = 1)
y = climbing['Rating_num']
weights = climbing['numVotes']

# Finish encoding the variables
target_encoder = TargetEncoder(cols = categorical_variables)
X = target_encoder.fit_transform(X, y)

# Convert to numpy array
X = np.array(X)
y = np.array(y)

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2)

# Create the model
rf_mod = RandomForestRegressor()
rf_mod.fit(X_train, y_train)
```




<style>#sk-container-id-1 {color: black;}#sk-container-id-1 pre{padding: 0;}#sk-container-id-1 div.sk-toggleable {background-color: white;}#sk-container-id-1 label.sk-toggleable__label {cursor: pointer;display: block;width: 100%;margin-bottom: 0;padding: 0.3em;box-sizing: border-box;text-align: center;}#sk-container-id-1 label.sk-toggleable__label-arrow:before {content: "▸";float: left;margin-right: 0.25em;color: #696969;}#sk-container-id-1 label.sk-toggleable__label-arrow:hover:before {color: black;}#sk-container-id-1 div.sk-estimator:hover label.sk-toggleable__label-arrow:before {color: black;}#sk-container-id-1 div.sk-toggleable__content {max-height: 0;max-width: 0;overflow: hidden;text-align: left;background-color: #f0f8ff;}#sk-container-id-1 div.sk-toggleable__content pre {margin: 0.2em;color: black;border-radius: 0.25em;background-color: #f0f8ff;}#sk-container-id-1 input.sk-toggleable__control:checked~div.sk-toggleable__content {max-height: 200px;max-width: 100%;overflow: auto;}#sk-container-id-1 input.sk-toggleable__control:checked~label.sk-toggleable__label-arrow:before {content: "▾";}#sk-container-id-1 div.sk-estimator input.sk-toggleable__control:checked~label.sk-toggleable__label {background-color: #d4ebff;}#sk-container-id-1 div.sk-label input.sk-toggleable__control:checked~label.sk-toggleable__label {background-color: #d4ebff;}#sk-container-id-1 input.sk-hidden--visually {border: 0;clip: rect(1px 1px 1px 1px);clip: rect(1px, 1px, 1px, 1px);height: 1px;margin: -1px;overflow: hidden;padding: 0;position: absolute;width: 1px;}#sk-container-id-1 div.sk-estimator {font-family: monospace;background-color: #f0f8ff;border: 1px dotted black;border-radius: 0.25em;box-sizing: border-box;margin-bottom: 0.5em;}#sk-container-id-1 div.sk-estimator:hover {background-color: #d4ebff;}#sk-container-id-1 div.sk-parallel-item::after {content: "";width: 100%;border-bottom: 1px solid gray;flex-grow: 1;}#sk-container-id-1 div.sk-label:hover label.sk-toggleable__label {background-color: #d4ebff;}#sk-container-id-1 div.sk-serial::before {content: "";position: absolute;border-left: 1px solid gray;box-sizing: border-box;top: 0;bottom: 0;left: 50%;z-index: 0;}#sk-container-id-1 div.sk-serial {display: flex;flex-direction: column;align-items: center;background-color: white;padding-right: 0.2em;padding-left: 0.2em;position: relative;}#sk-container-id-1 div.sk-item {position: relative;z-index: 1;}#sk-container-id-1 div.sk-parallel {display: flex;align-items: stretch;justify-content: center;background-color: white;position: relative;}#sk-container-id-1 div.sk-item::before, #sk-container-id-1 div.sk-parallel-item::before {content: "";position: absolute;border-left: 1px solid gray;box-sizing: border-box;top: 0;bottom: 0;left: 50%;z-index: -1;}#sk-container-id-1 div.sk-parallel-item {display: flex;flex-direction: column;z-index: 1;position: relative;background-color: white;}#sk-container-id-1 div.sk-parallel-item:first-child::after {align-self: flex-end;width: 50%;}#sk-container-id-1 div.sk-parallel-item:last-child::after {align-self: flex-start;width: 50%;}#sk-container-id-1 div.sk-parallel-item:only-child::after {width: 0;}#sk-container-id-1 div.sk-dashed-wrapped {border: 1px dashed gray;margin: 0 0.4em 0.5em 0.4em;box-sizing: border-box;padding-bottom: 0.4em;background-color: white;}#sk-container-id-1 div.sk-label label {font-family: monospace;font-weight: bold;display: inline-block;line-height: 1.2em;}#sk-container-id-1 div.sk-label-container {text-align: center;}#sk-container-id-1 div.sk-container {/* jupyter's `normalize.less` sets `[hidden] { display: none; }` but bootstrap.min.css set `[hidden] { display: none !important; }` so we also need the `!important` here to be able to override the default hidden behavior on the sphinx rendered scikit-learn.org. See: https://github.com/scikit-learn/scikit-learn/issues/21755 */display: inline-block !important;position: relative;}#sk-container-id-1 div.sk-text-repr-fallback {display: none;}</style><div id="sk-container-id-1" class="sk-top-container"><div class="sk-text-repr-fallback"><pre>RandomForestRegressor()</pre><b>In a Jupyter environment, please rerun this cell to show the HTML representation or trust the notebook. <br />On GitHub, the HTML representation is unable to render, please try loading this page with nbviewer.org.</b></div><div class="sk-container" hidden><div class="sk-item"><div class="sk-estimator sk-toggleable"><input class="sk-toggleable__control sk-hidden--visually" id="sk-estimator-id-1" type="checkbox" checked><label for="sk-estimator-id-1" class="sk-toggleable__label sk-toggleable__label-arrow">RandomForestRegressor</label><div class="sk-toggleable__content"><pre>RandomForestRegressor()</pre></div></div></div></div></div>




```python
# Make predictions and evalutate model performance
preds = rf_mod.predict(X_test)
mean_squared_error(y_test, preds)
```




    0.9987337505008477


