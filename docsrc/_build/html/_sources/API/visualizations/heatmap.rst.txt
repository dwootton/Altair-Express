.. _countplot:

============
Countplot
============

.. altair-plot::

    import altair_express as alx
    from vega_datasets import data
    df = data.movies()


    alx.heatmap(df.groupby("Major_Genre").mean(numeric_only=True))

The heatmap() function is used to showcase how a numerical variable