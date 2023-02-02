.. _filter-brush:

============
Filter Brush
============


The filter_type() function creates an interactive visualization with a search box that allows a user to filter the data based on text.

When working with large datasets, it can be challenging to quickly find and focus on specific data points. 
The filter_type() function provides a solution by using a searchbox to filter down to specific elements of the data.
This is a convenient way to quickly locate and focus on relevant data that has text properties (ie names, categories, etc).

.. altair-plot::

    import altair_express as alx
    from vega_datasets import data

    df = data.jobs().sample(5000) # sample 5k data points to avoid altair's limit
    alx.filter_type(target='job') + alx.lineplot(df,x='year',color='job',y='count')
    
