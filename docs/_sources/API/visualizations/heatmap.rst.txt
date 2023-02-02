.. _countplot:

============
Countplot
============
.. altair-plot::

    import altair_express as alx
    from vega_datasets import data
    df = data.cars()

    alx.highlight_brush() + alx.countplot(df,x='Origin')

The countplot() function is used to display the distribution of a categorical variable. For numerical variables, use use :ref:`hist`.

 This function creates a bar plot where the height of each bar represents the count of each category in the data.
The hist() function generates histograms to visualize the distribution of a single numeric variable. For categorical variables, use :ref:`countplot`.

It shows the frequency of the data points in different ranges, also known as bins.
The height of each bar in the histogram represents the number of data points that fall within that bin. 
By visualizing the distribution, the shape of the data can be determined,  outliers identified, and data skew assessed.
