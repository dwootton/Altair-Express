.. _getting-started-interaction:

====================================
Geting Started With Interactive Data Analysis
====================================

If data exploration is a conversation between you and your data, then interactive data analysis is 
the non-verbal communication. It's the gestures, expressions, and actions that help you communicate
your intent without having to be overly specific with the language– or code –that you write to direct
your analysis. 

For example, let's say you're analyzing a dataset of the horsepower and miles_per_gallon efficency of various cars.
You create a scatterplot of these variables, and you're interested in understanding why the relationship
"flattens out" where gains in horsepower no longer translate to gains in miles per gallon. 

To do that you can add a brush that lets you select the datapoints in that region.

Go ahead and give it a try. Once you have the data points highlighted, hit CMD+C (or control + C on windows) to
create a pandas query that selects the data points you've highlighted.

.. altair-plot::

    import altair_express as alx
    from vega_datasets import data


    alx.highlight_brush() + alx.scatterplot(data=data.cars(),x='Horsepower',y='Miles_per_Gallon')

.. note::  To interact with the above plot, click and drag on the plot to create a brush. Once you've created a brush, 
    you can click and drag the edges of the brush to resize it. Once you have a brush, you can hit CMD+C (or control + C on windows) to
    create a pandas query that selects the data points you've highlighted.


.. raw:: html

    <input type="text" id="my-textbox" placeholder="Paste your copied query" style="width: 100%;">


Sometimes, certain queries are difficult to express just using a mouse. For example, let's say you want to select
cars that have a particular name. Let's use altair express to create a similar scatterplot, but with a filter that lets you search
for cars by name.

.. altair-plot::

    import altair_express as alx
    from vega_datasets import data

    alx.filter_type(target='Name') + alx.scatterplot(data=data.cars(),x='Horsepower',y='Miles_per_Gallon')

.. note::  To interact with the above plot, enter text into the search box to filter the data points to only data whose name 
    matches the text you've entered. The textbox supports regular expressions; (volkswagen|ford) would find all cars whose name
    contains either volkswagen or ford. 


    You'll use a tooltip in the next chart to confirm the data is correctly filtered.

Sometimes you may want to "point and look" at the data to see more information about it– such as the names of circles on a scatterplot.
For that, you can use the `tooltip_hover` function.


.. altair-plot::

    import altair_express as alx
    from vega_datasets import data


    alx.tooltip_hover() + alx.filter_type(target='Name') + alx.scatterplot(data=data.cars(),x='Horsepower',y='Miles_per_Gallon')


.. note::  To interact with the above plot, hover your mouse over data points to see a tooltip with more information. You can 
    also use the text box to 

And at other times, you may want to actually zoom in on a region of plot to see the data in more fidelity.
Overplotted scatterplots make it difficult to really understand how many data points are in a region, but by 
zooming in you can see the data in more detail.

.. altair-plot::

    import altair_express as alx
    from vega_datasets import data


    alx.pan_zoom() + alx.scatterplot(data=data.cars(),x='Horsepower',y='Miles_per_Gallon')

.. note::  To interact with the above plot, click and drag to pan the plot. Pinch to zoom in and out.

This was a quick introduction to a few of the interaction techniques supported by altair express. Go check out 
our :ref:`interaction-techniques` section to learn more about the different interaction techniques supported by altair express.
