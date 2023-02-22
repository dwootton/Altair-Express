.. _barplot:

============
Barplot
============

.. altair-plot::
    import altair_express as alx
    import pandas as pd

    df = pd.DataFrame({
        'a': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I'],
        'b': [28, 55, 43, 91, 81, 53, 19, 87, 52]
    })

    alx.barplot(df,x='a',y='b')
   
Barplots are a common type of chart used to visualize counts or summary statistics with respect to different categories.
Barplots are similar to histograms, but they are used to visualize counts of categorical variables rather than numerical variables.

Parameters
**********************
data : pandas dataframe or pandas series
    The data to visualize as a pandas dataframe. If a series is provided, the series is used as the variable to be encoded in a histogram.
x : string
    The column name of the series for the x axis.
y : string
    The column name of the series for the y axis.
color : string 
    A valid CSS color to make the chart or a column name in the dataframe to color the bars by.
column : string
    The column name to be used as the column facet to produced grouped bar charts
width : int
    The width of the chart in pixels.
height : int
    The height of the chart in pixels.
effects : :ref:`effects-object`
    The effects of interactions to be applied to the chart.

.. warning::
    Interaction with barplots is still experimental. Please report any issues you encounter.

Examples
**********************

Grouped Barplot
^^^^^^^^^^^^^^^^^^^^^^
.. altair-plot::
    import altair_express as alx
    from vega_datasets import data

    df = data.barley()

    alx.barplot(df,x='year:N',y='sum(yield)',color='year:N',column='site')

Stacked Barplot
^^^^^^^^^^^^^^^^^^^^^^
.. altair-plot::
    import altair_express as alx
    from vega_datasets import data

    df = data.barley()

    alx.barplot(df,x='year:N',y='sum(yield)',color='site:N')
