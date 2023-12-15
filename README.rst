PYCLIMB
=======
This package is used to clean and vizualize data that can be obtained from mountainproject.com.

Documentation
-------------
To read the documentation please visit `<https://quintbro.github.io/Climbing_and_Climate/>`_

Installation
------------
Use the package manager `pip` to install pyclimb.

.. code-block:: bash

    pip install git+https://github.com/quintbro/Climbing_and_Climate.git

In order to obtain the .csv files that work with this package go to the `mountain project route finder <https://www.mountainproject.com/route-finder>`_ and filter to the desired routes that you want data on. then hit "export csv" which will download the .csv file that will work with all of the functions in this package. 
**NOTE:** the route finder will only export 1000 climbs at a time, so if you want export more climbs than that you will need to export multiple .csv files then use the concat function to concatenate all of them into a single dataframe.

Example
-------
Here is a demo of how to use the package:

if you have multiple .csv files the concat function found in the clean_climbing module will concatenate them together for you.

.. code-block:: python

    import pyclimb as pc

    files = ["route-finder_1.csv", "route-finder_2.csv"]
    climbs = pc.concat(list_of_files = files)

You can then use the clean function from the clean_climbing module to clean the data for you.

.. code-block:: python

    pc.clean(df = climbs, inplace = True)

You can also get additional data by using the scrape_mp function from the scrape_climbing module
**NOTE:** the crawl delay required by mountain project is 60

.. code-block:: python

    new_data = pc.scrape_mp(df = climbs, crawl_delay = 60)

The additional data used in the demo.ipynb was collected from UtahWeatherStations.gov and mapsofworld.com
