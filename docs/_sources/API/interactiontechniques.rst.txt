.. _interaction-techniques:

============
Interaction Techniques
============

+-----------------------+------------------------+-----------------+--------------+
| Interaction Techniques| Command              | Pandas Command    | Status       |
+=======================+========================+=================+==============+
| :ref:`filter-brush`   | alx.filter_brush()     | query (filter)  | implemented  |
+-----------------------+------------------------+-----------------+--------------+
| :ref:`filter-point`   | alx.filter_point()     | query (filter)  | implemented  |
+-----------------------+------------------------+-----------------+--------------+
| :ref:`filter-type`    | alx.filter_type()      | query (filter)  | implemented  |
+-----------------------+------------------------+-----------------+--------------+
| :ref:`highlight-brush`| alx.highlight_brush()  | query (filter)  | implemented  |
+-----------------------+------------------------+-----------------+--------------+
| :ref:`group-point`    | alx.group_point()      | groupby         | implemented  |
+-----------------------+------------------------+-----------------+--------------+
| :ref:`panzoom`        | alx.panzoom()          | None            | implemented  |
+-----------------------+------------------------+-----------------+--------------+
| :ref:`highlight-color`| alx.highlight_color()  | query (filter   | implemented  |
+-----------------------+------------------------+-----------------+--------------+
| group_brush           | alx.group_brush()      | groupby         | in-progress  |
+-----------------------+------------------------+-----------------+--------------+
| encode_axis           | alx.encode_axis()      | None            | in-progress  |
+-----------------------+------------------------+-----------------+--------------+

The interaction typology is a set of interaction techniques that are helpful when 
using charts to explore data.  These interaction techniques can be now! layered ontop of charts
by simply layering them on top like:

.. altair-plot::

    import altair_express as alx
    from vega_datasets import data


    alx.filter_brush() + alx.scatterplot(data=data.cars(),x='Horsepower',y='Miles_per_Gallon')

These interactions can also be composed together, for more information see :ref:`composing-interactions`. 
