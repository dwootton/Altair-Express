.. _pairplot:

============
Pair Plot
============
.. altair-plot::

    import altair_express as alx
    from vega_datasets import data
    df = data.gapminder()

    alx.pairplot(df)

The pairplot() function creates a matrix of scatterplots and histograms to visualize the pairwise relationships between variables in a dataset.

pairplot() is a convenient way to quickly visualize the distribution and relationship between multiple variables in a dataset.
By plotting all possible pairs of numeric variables, this function allows you to quickly identify any potential correlations, distributions, or outliers in your data. 
It can be particularly useful for exploring and understanding the structure of a dataset before building more sophisticated models.



Parameters
**********************
data : pandas dataframe
    The data to visualize as a pandas dataframe. 
variables : string[]
    An array of column names to visualize in the pairplot. Defaults to all numeric columns in the dataframe.


Examples
**********************

Interactive Brush
^^^^^^^^^^^^^^^^^^^^^^
.. altair-plot::

    import altair_express as alx
    from vega_datasets import data

    alx.highlight_brush() + alx.jointplot(data=data.cars(),x='Miles_per_Gallon',y='Horsepower')


