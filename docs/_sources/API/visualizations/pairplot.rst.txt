.. _pairplot:

============
Pair Plot
============
.. altair-plot::

    import altair_express as alx
    from vega_datasets import data
    df = data.gapminder()

    alx.highlight_brush() + alx.pairplot(df)

The pairplot() function creates a matrix of scatterplots and histograms to visualize the pairwise relationships between variables in a dataset.

pairplot() is a convenient way to quickly visualize the distribution and relationship between multiple variables in a dataset.
By plotting all possible pairs of numeric variables, this function allows you to quickly identify any potential correlations, distributions, or outliers in your data. 
It can be particularly useful for exploring and understanding the structure of a dataset before building more sophisticated models.




