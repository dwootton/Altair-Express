.. _countplot:

============
Countplot
============
.. altair-plot::

    import altair_express as alx
    from vega_datasets import data
    df = data.cars()

    alx.countplot(df,x='Origin')

The countplot() function is used to display the distribution of a categorical variable. For numerical variables, use use :ref:`hist`.

This function creates a bar plot where the height of each bar represents the count of each category in the data.

It shows the frequency of the data points in different ranges, also known as bins.
The height of each bar in the histogram represents the number of data points that fall within that bin. 
By visualizing the distribution, the shape of the data can be determined,  outliers identified, and data skew assessed.

Parameters
**********************
data : pandas dataframe or pandas series
    The data to visualize as a pandas dataframe. If a series is provided, the series is used as the variable to be encoded in a histogram.
x : string
    The column name of the categorical series used for the x axis.
color : string 
    A valid CSS color to make the chart or a column name in the dataframe to color the bars by.
width : int
    The width of the chart in pixels.
height : int
    The height of the chart in pixels.
effects : :ref:`effects-object`
    The effects of interactions to be applied to the chart.

