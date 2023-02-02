"""Interactions module."""


import altair as alt
import pandas as pd
import numpy as np
from .utils import add_encoding,check_axis_binned, get_field_from_encoding, check_axis_aggregate, is_undefined, alt_get, extent_from_column
'''
Interactions have effects and triggers. 
"instruments" are the location-triggers (how to create) 
'''

DEFAULT_COLORS = ["#5778a4", "#e49444", "#d1615d","#85b6b2","#6a9f58","#e7ca60","#a87c9f","#f1a2a9","#967662","#b8b0ac"]
                  
def add_cursor_to_mark(unit_chart,cursor_type):
    if isinstance(unit_chart.mark,str):
        mark_type = unit_chart.mark
        unit_chart.mark = alt.MarkDef(type=mark_type,cursor=cursor_type)
    else: 
        unit_chart.mark.cursor = cursor_type
    
    
    return unit_chart

def recursively_add_to_mark(chart,cursor_type):
    if hasattr(chart,'mark') :
        chart = add_cursor_to_mark(chart,cursor_type)

# todo fix this, to not add click pointer to background 
    
    if  cursor_type != "pointer" and (hasattr(chart,'mark') or hasattr(chart,'layer')):
        chart.view = {
            "cursor":cursor_type,
            "stroke":None
        }
        return chart

    attributes_for_recursion = ['layer','hconcat','vconcat']
    for attribute in attributes_for_recursion:
        # TODO: fix this following line. Right now, it enters into if for any layer, concat.
        # instead, it should see if any exists, and if it does, it should use that as the item to search
        if alt_get(chart,attribute):
          for unit_spec in chart[attribute]:
              unit_spec = recursively_add_to_mark(unit_spec,cursor_type)
 
    return chart

ALX_SELECTION_PREFIX = "ALX_SELECTION_"
ALX_SELECTION_SUFFIX= {
    "filter":"_FILTER",
    "scale_bind":"_FILTER",
    "highlight":"_FILTER",
    "group":"_GROUP"
}

def check_if_unit_line(chart):
    
    if isinstance(chart.mark,str):
        return chart.mark == 'line' or chart.mark == 'area'  
    else: 
        return chart.mark.type == 'line' or chart.mark.type == 'area'

def check_if_line(chart):
    if hasattr(chart,'mark'):
        return check_if_unit_line(chart)

    attributes_for_recursion = ['layer','hconcat','vconcat']
    for attribute in attributes_for_recursion:
        # TODO: fix this following line. Right now, it enters into if for any layer, concat.
        # instead, it should see if any exists, and if it does, it should use that as the item to search
        if alt_get(chart,attribute):
          for unit_spec in chart[attribute]:
              if(check_if_line(unit_spec)):
                return True
    return False


def create_selection(chart,interaction):
    selection = None
    # only allow selection on an axis if it is meaningful (ie data encoded, not 'count')
    # check if any axis is aggregate
    
    if interaction.action['trigger'] == "drag":
        encodings =  ['x','y'] # by default
        encodings = [encoding for encoding in encodings if not check_axis_aggregate(chart,encoding)]

        # if it is a line chart without additional encodings options, use x
        has_options = getattr(interaction,'options',None) != None
        if check_if_line(chart) and (not has_options or (has_options and 'encodings' not in interaction.options)):
            encodings = ['x']

        if has_options and 'encodings' in interaction.options:
            encodings = interaction.options['encodings']

        name = ALX_SELECTION_PREFIX+'drag'+ALX_SELECTION_SUFFIX[interaction.effect['transform']]
        selection = alt.selection_interval(encodings=encodings, name=name)
    if interaction.action['trigger'] == "click":
        name = ALX_SELECTION_PREFIX+'click'+ALX_SELECTION_SUFFIX[interaction.effect['transform']]

        selection = alt.selection_point(name=name)
        
        if 'target' in interaction.action:
            field = get_field_from_encoding(chart,interaction.action['target'])
            selection=alt.selection_point(name=name, encodings=[interaction.action['target']], fields=[field])
        else: 
            x_is_aggregate = check_axis_aggregate(chart,'x')
            y_is_aggregate = check_axis_aggregate(chart,'y')

            fields = []
            if get_field_from_encoding(chart,'column'):
                fields = [get_field_from_encoding(chart,'column')]
            

            if  x_is_aggregate and not y_is_aggregate:
                # if x is aggregated (ie is a count), then add y field to selection 
                selection=alt.selection_point(name=name, encodings=['y'],fields=fields)
            elif not  x_is_aggregate and  y_is_aggregate:
                # if both of them are 
                selection=alt.selection_point(name=name, encodings=['x'],fields=fields)
            elif not x_is_aggregate and not y_is_aggregate:
                selection=alt.selection_point(name=name, encodings=['x','y'],fields=fields)

    if interaction.action['trigger'] == "type":
        name = ALX_SELECTION_PREFIX+'query'+ALX_SELECTION_SUFFIX[interaction.effect['transform']]

        selection = alt.param(name=name,value="",bind=alt.binding(name=interaction.action['target']+": ",input='text', placeholder='Type to search...'))

    if interaction.action['trigger'] == "panzoom":
        encodings =  [] # by default
        if interaction.options['bind_x']:
            encodings.append('x')
        if interaction.options['bind_y']:
            encodings.append('y')
        name = ALX_SELECTION_PREFIX+'panzoom'+ALX_SELECTION_SUFFIX[interaction.effect['transform']]
        selection = alt.selection_interval(name=name,bind="scales", encodings=encodings)
    
    return selection 

def add_colors(chart,data,field):
    unique_values = pd.unique(data)
    unique_values.sort()
    domain = ['Group']
    range = ['black']
    for index,value in enumerate(unique_values):
        domain.append(value)
        if index < len(DEFAULT_COLORS):
            range.append(DEFAULT_COLORS[index])
        else: 
            range.append("lightgray")
    color_scale = alt.Scale(domain=domain,range=range)
    chart=chart.encode(alt.Color(field=field,scale=color_scale))
    return chart

def apply_effect(chart,interaction,selection):
    attributes_for_recursion = ['layer','hconcat','vconcat']
    for attribute in attributes_for_recursion:

        if alt_get(chart,attribute):
            specs = []
            for unit_spec in chart[attribute]:
                #if alt_get(chart,'data') and not is_undefined(chart.data):
                #    print('adding data',len(chart.data))
                    #unit_spec.data = chart.data

                
                specs.append(apply_effect(unit_spec,interaction,selection))
            chart[attribute] = specs


    if getattr(chart,'mark',None) is not None:
        chart =  apply_effect_recurse(chart,interaction,selection)
    
    return chart

def apply_effect_recurse(previous_chart,interaction,selection):
    chart = previous_chart.copy(deep=True)
    # alter the chart object to allow for interaction
    # apply the transform 
    
    if interaction.effect['transform'] == "filter":
         chart = filter_chart(chart,interaction,selection)
                
        # if no encodings exist, 
    
    if interaction.effect['transform'] == "highlight":
        chart = highlight_chart(chart,interaction,selection)
    
    if interaction.effect['transform'] == "group":
        chart = group_chart(chart,interaction,selection)
        
    if interaction.effect['transform'] == "scale_bind":
        chart = pan_zoom_chart(chart,interaction,selection)

    return chart



def group_chart(chart,interaction,selection):
    # point interactions can only occur on categorical fields 
    if interaction.action['trigger'] == "click":
        # determine if either x or y is independent
        # if so, group by that axis, do all groupings 
        groupby_category = ['column','color','x','y'] 
        
        for category in groupby_category:
            field = get_field_from_encoding(chart,category)

            if not field:
                continue

            # check if field is an independent axis 
            group_name = "ALX_GROUP_COLUMN_" + field
            if_statement = f'''
              if(isDefined({selection.name}["{group_name}"]),
                indexof({selection.name}["{group_name}"],datum["{field}"]) > -1 ?
                    "Group" : datum["{field}"],
                datum["{field}"]
              ) 
            '''
            if_statement= ' '.join(if_statement.split())


            # must pass as a dictionary because of use of as (a reserved keyword)
            calculate_transform = alt.CalculateTransform(**{'calculate':if_statement,'as':group_name})

            if not is_undefined(chart.transform):
                chart.transform.insert(0,calculate_transform)
            else:
                chart.transform = [calculate_transform]

          


            # check if x or y is aggregate
            x_is_aggregate = check_axis_aggregate(chart,'x')
            y_is_aggregate = check_axis_aggregate(chart,'y')
            if not y_is_aggregate and not x_is_aggregate:
                y_field = get_field_from_encoding(chart,'y')
                x_field = get_field_from_encoding(chart,'x')
                color_field = get_field_from_encoding(chart,'color')

               
                # TODO, smartly determine if x or y are indepdent or dependent variables
                groupby = [x_field]
                # if color was used to create separate data points, then group by color
                if color_field:
                  groupby.append(group_name)


                y_avg = f'avg{y_field}'


                chart.encoding.y.field = y_avg


                chart = chart.transform_aggregate(aggregate=[alt.AggregatedFieldDef("average",y_field,**{'as':y_avg})],groupby=groupby)


            y_field = get_field_from_encoding(chart,'y')
            # TODO: calculate another datum property that can be used for tooltips

            if_2 = f'''
            if(isDefined({selection.name}["{group_name}"]),
              datum["{group_name}"] == "Group"?
                  {selection.name}["{group_name}"] : datum["{group_name}"],
              datum["{group_name}"]
            )
            '''

            if_2= ' '.join(if_2.split())

            calculate_transform2 = alt.CalculateTransform(**{'calculate':if_2,'as':"_tooltip_column"})
            chart.transform.append(calculate_transform2)
            chart= chart.encode(tooltip=alt.Tooltip("_tooltip_column",type='nominal'))


            chart.encoding[category].field = group_name

            # for line charts, add interaction to an overlay so that mouse events have larger hitbox
            if check_if_line(chart):
                # do 
                if category == 'color':
                    chart = add_colors(chart,chart.data[field],group_name)

                # add mouse overlay
                params = chart.params
                chart.params = []
                interaction_overlay = chart.copy(deep=True).mark_line(strokeWidth= 8, stroke="transparent")
                properties = chart.mark
                if isinstance(properties,str):
                  interaction_overlay=interaction_overlay.mark_line(strokeWidth= 8, stroke="transparent")
                else:
                  properties['strokeWidth'] = 8
                  properties['stroke'] = "transparent"
                  interaction_overlay=interaction_overlay.mark_line(**properties)
                interaction_overlay.params = params
                
                chart = alt.LayerChart(layer=[chart,interaction_overlay])
                #chart.encoding.y.field = "_grouping_column"
                #chart.encoding.x.field = "_grouping_column"

            
            break
    # brush interactions can occur on both categorical and quantitative fields
    

    
    return chart
    
    
    
    
def filter_chart(chart,interaction,selection):
    filter_transform = alt.FilterTransform({"param": selection.name})

    # for text box interaction, use query filter
    #(!ALX_SELECTION_query_FILTER || test(regexp(ALX_SELECTION_query_FILTER), toString(datum['job'])))
    if interaction.action['trigger'] == "type":
        query_string = f"(!{selection.name} || test(regexp({selection.name},'i'), toString(datum['{interaction.action['target']}'])))"
        filter_transform = alt.FilterTransform(**{"filter": query_string})


        # insert at begining to ensure all data gets filtered correctly
    if not is_undefined(chart.transform):
        chart.transform.insert(0,filter_transform)
    else:
        chart.transform = [filter_transform]
        
    # for each encoding in selection 
    selection_type = getattr(selection.param,'select',{})
    encodings = getattr(selection_type,'encodings',None) or ["x","y"] # default to x and y to maintain reference of chart
    
    # fix the encoding scales so that the view remains static 
    if encodings and not is_undefined(encodings): 
        for encoding in encodings:
            field = get_field_from_encoding(chart,encoding)
            
            if not is_undefined(chart.data) and field:
                extent = extent_from_column(chart.data,field)
                # TODO: copy the existing scale, just overwrite the domain
                scale = alt.Scale(domain=extent)
                chart['encoding'][encoding]['scale'] = scale
            
    return chart

def pan_zoom_chart(chart,interaction,selection):
    return chart.add_params(selection)

def highlight_chart(chart,interaction,selection):
     # for text box interaction, use query filter
   

    # if any of the axes are aggregated
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

        chart=chart.resolve_scale(
            color='independent'
        )

        filter_transform = alt.FilterTransform({"param": selection.name})
        if type(chart.layer[1].transform) is not alt.utils.schemapi.UndefinedType:
            chart.layer[1].transform.insert(0,filter_transform)
        else:
            chart.layer[1].transform = [filter_transform]

    elif not x_binned and not y_binned :
        # non-binned charts ()


        # if the chart already has a color encoding, use that as a conditional
        highlight = get_field_from_encoding(chart,'color') or alt.value('steelblue')

        color = alt.condition(selection,highlight,alt.value('lightgray'))

        if interaction.action['trigger'] == "type":
             query_string = f"(!query || test(regexp(query,'i'), toString(datum['{interaction.action['target']}'])))"
             color = alt.condition(query_string,highlight,alt.value('lightgray'))
             

     
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



class Interaction:
    def __init__(self, effect, action,options=None):
        self.effect = effect
        self.action = action
        self.options = options


    def __add__(self, other):
        #chart 
        return add_interaction(other,self)
    def __radd__(self, other):
        return self.__add__(other)

    def set_selection(self,selection):
        self.selection = selection

    def get_selection(self):
        return getattr(self,'selection',None)

# Input Effects
highlight = {"transform":"highlight"}
_filter = {"transform":"filter"} # _filter as to avoid overloading python's filter function
group = {"transform":"group"}
scale_bind = {"transform":"scale_bind"}
tooltip = {"transform":"tooltip"}

# Input Actions
brush = {"trigger":"drag"}
point = {"trigger":"click"}
color = {"trigger":"click","target":"color"}
text = {"trigger":"type"}
brush = {"trigger":"drag"}
hover = {"trigger":"mouseover"}

def tooltip_hover():
    return Interaction(effect=tooltip,action=hover)

def highlight_brush(options=None):
    return Interaction(effect=highlight,action=brush,options=options)

def highlight_point():
    return Interaction(effect=highlight,action=point)
def highlight_color():
    return Interaction(effect=highlight,action=color)
def filter_brush():
    return Interaction(effect=_filter,action=brush)
def filter_point():
    return Interaction(effect=_filter,action=point)

def group_brush():
    return Interaction(effect=group,action=brush)
def group_point():
    return Interaction(effect=group,action=point)
def group_color():
    return Interaction(effect=group,action=color)

def pan_zoom(bind_x=True, bind_y=True):    
    return Interaction(effect=scale_bind,action={"trigger":"panzoom"},options={'bind_x':bind_x,'bind_y':bind_y})

def filter_type(target):
    action = { "trigger": "type", "target": target}
    return Interaction(effect=_filter,action=action)

def highlight_type(target):
    action = { "trigger": "type", "target": target}
    return Interaction(effect=highlight,action=action)
# group_brush
# group_point

# tooltip_point # shows information about one specific value 
# tooltip_brush  # calculates summary statistics about data in selection


def process_effects(chart,effects):
    if 'filter' in effects:
      chart = process_filters(chart,effects['filter'])
    elif 'highlight' in effects:
      chart = process_highlights(chart,effects['highlight'])
    elif 'group' in effects:
      chart = process_groups(chart,effects['group'])
    return chart

def process_highlights(chart,highlights):
  # if filter is not an array, make it an array
  if not isinstance(highlights, list):
      highlights = [highlights]
  for highlight in highlights:
      if isinstance(highlight, Interaction):
          parameter = highlight.get_selection()
          if parameter is None:
              parameter = create_selection(chart,highlight)

          chart = apply_effect(chart,highlight,parameter)
  return chart

def process_filters(chart,filters):
  if not isinstance(filters, list):
      filters = [filters]

  for filter in filters:
      # if filter is Interaction instance 
      if isinstance(filter, Interaction):
          parameter = filter.get_selection()
          chart = chart.transform_filter(parameter)
      else: 
          chart = chart.transform_filter(filter)
  return chart

def process_groups(chart,groups):
  if not isinstance(groups, list):
      groups = [groups]

  for group in groups:
      # if filter is Interaction instance 
      if isinstance(group, Interaction):
          parameter = group.get_selection()
          if parameter is None:
              parameter = create_selection(chart,group)
          chart = apply_effect(chart,group,parameter)
      
  return chart
def add_cursor(chart,interaction):
    if interaction.action['trigger'] == "drag":
        chart = recursively_add_to_mark(chart,'crosshair')

        #chart.view ={"cursor":"crosshair","stroke":None}
    if interaction.action['trigger'] == "click":
        chart = recursively_add_to_mark(chart,'pointer')
    if interaction.action['trigger'] == "panzoom":
        chart = recursively_add_to_mark(chart,'move')
        #chart.view ={"cursor":"move"}
    return chart

def add_interaction(chart, interaction):
    
    parameter = create_selection(chart,interaction)
    interaction.set_selection(parameter)
    chart=chart.add_params(parameter)
    chart =  apply_effect(chart,interaction,parameter)
    chart = add_cursor(chart,interaction)

    return chart

