.. _composing-interactions:

============
Composing Interactions
============

You can compose interactions by adding them together as if you're layering multiple charts:

.. altair-plot::
    :output: repr
    import pandas as pd

    test = pd.DataFrame([
      {"a": 30, "b": 28, "label": "Andy"},
      {"a": 25, "b": 65, "label": "Brian"},
      {"a": 70, "b": 43, "label": "Charlie"}
    ])

    alx.pan_zoom() + (alx.highlight_type(target='label') + alt.Chart(test).mark_text().encode(text='label',x='a',y='b'))#.add_params(query_param).transform_filter()




You can also isolate the effects of an interaction, and compose that directly


and 


.. altair-plot::
    import altair_express as alx
    from vega_datasets import data

    overview = alx.filter_brush()
    group_interaction = alx.group_color()

    chrt1 = overview + alx.lineplot(data=data.stocks(),x='date',x_axis=None,y_axis=None,y='price',color='symbol',height=100)
    chrt2 = group_interaction + alx.lineplot(data=data.stocks(),x='date',y='price',color='symbol',effects={"filter":overview})

    chrt1 & chrt2
