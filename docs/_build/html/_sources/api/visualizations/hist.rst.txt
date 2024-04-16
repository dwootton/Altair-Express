.. _hist:

============
Histogram
============


.. altair-plot::

    import altair_express as alx
    from vega_datasets import data
    df = data.cars()

    alx.hist(df,x='Horsepower')

The hist() function generates histograms to visualize the distribution of a single numeric variable. For categorical variables, use :ref:`countplot`.

It shows the frequency of the data points in different ranges, also known as bins.
The height of each bar in the histogram represents the number of data points that fall within that bin. 
By visualizing the distribution, the shape of the data can be determined,  outliers identified, and data skew assessed.

Parameters
**********************
data : pandas dataframe or pandas series
    The data to visualize as a pandas dataframe. If a series is provided, the series is used as the variable to be encoded in a histogram.
x : string
    The column name of the data to be aggregated into a histogram.
color : string 
    A valid CSS color to make the chart or a column name in the dataframe to color the bars by.
max_bins : int
    The maximum number of bins to use in the histogram. If the number of bins is not specified, the number of bins is set to 10.
width : int
    The width of the chart in pixels.
height : int
    The height of the chart in pixels.
effects : :ref:`effects-object`
    The effects of interactions to be applied to the chart.

Examples
**********************

Interactive Brush
^^^^^^^^^^^^^^^^^^^^^^
.. altair-plot::

    import altair_express as alx
    from vega_datasets import data
    df = data.cars()

    #alx.highlight_brush()+alx.hist(df,x='Horsepower')

    
Split by color  
^^^^^^^^^^^^^^^^^^^^^^
.. altair-plot::

    import altair_express as alx
    from vega_datasets import data
    df = data.cars()

    alx.hist(df,x='Horsepower',color='Origin', max_bins=25)

