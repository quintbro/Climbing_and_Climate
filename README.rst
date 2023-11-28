PYCLIMB
=======
This package is used to clean and vizualize data that can be obtained from mountainproject.com.

Documentation
-------------

Installation
------------
Use the package manager `pip` to install pyclimb.

.. code-block:: bash

    pip install git+https://github.com/quintbro/Climbing_and_Climate.git

In order to obtain the .csv files that work with this package go to the `mountain project route finder <https://www.mountainproject.com/route-finder>` and filter to the desired routes that you want data on. then hit "export csv" which will download the .csv file that will work with all of the functions in this package. 
**NOTE** the route finder will only export 1000 climbs at a time, so if you want export more climbs than that you will need to export multiple .csv files then use the dataConcat function to concatenate all of them into a single dataframe.

Example
-------
Here is a demo of how to use the package:

if you have multiple .csv files the dataConcat function found in the clean_climbing module will concatenate them together for you.

.. code-block:: python

    from pyclimb.clean_climbing import dataConcat

    files = ["route-finder_1.csv", "route-finder_2.csv"]
    climbs = dataConcat(list_of_files = files)

You can then use the dataClean function from the clean_climbing module to clean the data for you.

.. code-block:: python

    from pyclimb.clean_climbing import dataClean

    dataClean(df = climbs, inplace = True)

You can also get additional data by using the scrape_mp function from the scrape_climbing module
**NOTE** the crawl delay required by mountain project is 60

.. code-block:: python
    from pyclimb.scrape_climbing import scrape_mp

    new_data = scrape_mp(df = climbs, crawl_delay = 60)
