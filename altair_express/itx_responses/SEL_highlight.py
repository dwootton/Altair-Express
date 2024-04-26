import pandas as pd 
import altair as alt 

from ..utils import check_if_line, add_encoding, get_field_from_encoding, check_axis_aggregate, check_axis_binned, add_colors

def highlight_chart(chart,selection):
    # for text box interaction, use query filter

    # if any of the axes are aggregated
    x_agg = check_axis_aggregate(chart,'x')
    y_agg = check_axis_aggregate(chart,'y')

    x_binned = check_axis_binned(chart,'x')
    y_binned = check_axis_binned(chart,'y')

    is_line = check_if_line(chart)

    if  is_line:

        # for line charts, create a new layer with a color scale that maps to light gray
        color = get_field_from_encoding(chart,'color')      

        transform = None

        if getattr(chart,'transform',None):
            transform = getattr(chart,'transform',None) 
            chart.transform = alt.Undefined

        chart = chart + chart 

        if color == None:
            chart.layer[0]=chart.layer[0].encode(color=alt.value('lightgray'))
            chart.layer[1]=chart.layer[1].encode(color=alt.value('steelblue'))
        else: 
            # using pd.unique to ensure Nones are encorporated
            unique = pd.unique(chart.data[color])
            chart.layer[0]=chart.layer[0].encode(alt.Color(legend=None,field=color,scale=alt.Scale(domain=unique,range=['lightgray' for value in unique])))
            chart.layer[1]= add_colors(chart.layer[1],chart.data[color],color)

        if transform:
          chart.transform = transform

        chart
        chart=chart.resolve_scale(
            color='independent'
        )

        filter_transform = alt.FilterTransform({"param": selection.name}) 

        if type(chart.layer[1].transform) is not alt.utils.schemapi.UndefinedType:
            chart.layer[1].transform.insert(0,filter_transform)
        else:
            chart.layer[1].transform = [filter_transform]
    elif (not x_agg and not y_agg) and (not x_binned and not y_binned) :
        # non-binned charts ()

        # if the chart already has a color encoding, use that as a conditional
        highlight = get_field_from_encoding(chart,'color') or alt.value('steelblue')

        color = alt.condition(selection,highlight,alt.value('lightgray'))

        # NON: Selection based
        # if interaction.action['trigger'] == "type":
        #      query_string = f"(!query || test(regexp(query,'i'), toString(datum['{interaction.action['target']}'])))"
        #      color = alt.condition(query_string,highlight,alt.value('lightgray'))
             

     
        chart = add_encoding(chart,color)
        
    else:

        # used for any elements where height, width, etc are controlled by filter 
        color_encoding = chart.encoding.color
        #chart.encoding.color.scale=alt.Scale(scheme='greys')

        chart.encoding.color = alt.value('lightgray')
        chart = chart + chart 
        chart.layer[1].encoding.color = color_encoding

        filter_transform = alt.FilterTransform({"param": selection.name})

       

        if type(chart.layer[1].transform) is not alt.utils.schemapi.UndefinedType:
            chart.layer[1].transform.insert(0,filter_transform)
        else:
            chart.layer[1].transform = [filter_transform]

    return chart