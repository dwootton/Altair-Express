.. _effects-object:

============
Effect Objects
============

Sometimes you want to apply an interactions effect to a certain visualization without making that chart interactive itself. 
For example, you might want to highlight a certain group of points in a scatterplot, but you don't want to also brush on a countplot.
You can accomplish this by passing in a your interaction object in the effects dictionary of a chart. 

.. warning::
    Effect objects are still quite experimental. Right now the only effect that works is the filter and highlight effects.
    

You can compose interactions by adding them together as if you're layering multiple charts:
    

.. note::
    You may have noticed that our ``overview_itx`` object is a highlight brush, but we pass it in as a filter effect. 
    This is a unique capabilities between highlight and filter interactions as they can be interchanged freely. 
    

