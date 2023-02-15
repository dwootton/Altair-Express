.. _hist:

============
Histogram
============


.. altair-plot::

    import altair_express as alx
    from vega_datasets import data
    df = data.cars()

    alx.highlight_brush() + alx.hist(df,x='Horsepower')

The hist() function generates histograms to visualize the distribution of a single numeric variable. For categorical variables, use :ref:`countplot`.

It shows the frequency of the data points in different ranges, also known as bins.
The height of each bar in the histogram represents the number of data points that fall within that bin. 
By visualizing the distribution, the shape of the data can be determined,  outliers identified, and data skew assessed.

Parameters 
**********************

:param data: description
:param x: description
:param y: description
:param color: description
:param x_axis: description

:param width: description
:param height: description
:param effects: description

:type arg1: type description
:type arg1: type description
:return: return description
:rtype: the return type description
