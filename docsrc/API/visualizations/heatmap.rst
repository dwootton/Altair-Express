.. _heatmap:

============
Heatmap
============

.. altair-plot::

    import altair_express as alx
    from vega_datasets import data
    df = data.movies()

    grouped_df = df.groupby("Major_Genre").mean(numeric_only=True)
    
    alx.heatmap(grouped_df)

The heatmap() function is used to visualize a matrix where each cell in the matrix is represents a single scalar value. 

Heatmaps are particularly useful for visualizing the relationship how two categorical variables influence a numerical variable. 

Parameters
**********************
data : 
    The data to visualize as M x N pandas dataframe where each cell in the dataframe represents a single numerical value.


Examples
**********************

Interactive Brush
^^^^^^^^^^^^^^^^^^^^^^
.. altair-plot::

    import altair_express as alx
    from vega_datasets import data
    df = data.movies()

    grouped_df = df.groupby("Major_Genre").mean(numeric_only=True)
    
    alx.tooltip_hover() + alx.heatmap(grouped_df)

    
Tooltip  
^^^^^^^^^^^^^^^^^^^^^^
.. altair-plot::

    import altair_express as alx
    from vega_datasets import data
    df = data.cars()

    alx.hist(df,x='Horsepower',color='Origin', max_bins=25)

