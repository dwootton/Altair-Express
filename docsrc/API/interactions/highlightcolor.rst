.. _highlight-color:

============
Highlight Color
============

*Highlight Color is used to query elements of the data that share a specific color.* It is 
particularly used for cases like selecting groups that may not be spatially located at the same place.

.. altair-plot::

    import altair_express as alx
    from vega_datasets import data


    alx.highlight_color() + alx.scatterplot(data=data.cars(),x='Horsepower',y='Miles_per_Gallon',color='Origin')
