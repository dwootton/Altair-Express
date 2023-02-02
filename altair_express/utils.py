import numpy as np
import pandas as pd

import altair as alt

def add_encoding(chart,color):
    if getattr(chart,'encode',None) and getattr(chart,'mark',None) is not None:
        chart= chart.encode(color=color)
    
    return chart

    #chart = add_encoding(chart,{'color':color})

def is_axis_aggregate(chart,axis):
    if not getattr(chart,'encoding',None) or is_undefined(chart.encoding):
        return False
    encoding = chart.encoding[axis]

    AGGREGATION_NAMES = ["count","sum","distinct","missing","mean","average","variance","stdev"]

    if encoding:
        axis_encode = chart.to_dict()['encoding'].get(axis)
        if axis_encode is None:
            return False
        
        encode_string = f'{axis_encode}'
        for aggregation_name in AGGREGATION_NAMES:
            if encode_string.find(aggregation_name) > -1:
                return True
        return False
    else: 
        return False

def is_axis_binned(chart,axis):
    if not getattr(chart,'encoding',None) or is_undefined(chart.encoding):
        return False
    
    encoding = chart.encoding[axis]

    if encoding:
        axis_encode = chart.to_dict()['encoding'].get(axis)
        if axis_encode is None:
            return False
        else:
          return axis_encode.get('bin')
    else: 
        return False

def alt_get(chart,prop):
    return prop in dir(chart)

def is_undefined(obj):
    return str(obj) == 'Undefined'

'''
Recurses through concat or layer units of a visualization spec, calling function
on each unit spec. If the function returns a truthy value 
'''
# one to recruse through in finding first value
# on to recurse threough to do something to each chart
def recurse_through_units(chart,function,exitOnFirst = False):
    attributes_for_recursion = ['layer','hconcat','vconcat']
    for attribute in attributes_for_recursion:
        if alt_get(chart,attribute):
          # if it has that combination, then recurse through it
          results = []
          for unit in chart.to_dict()[attribute]:
              result = recurse_through_units(chart,function,exitOnFirst)
              results.append(result)
              
              result = function(unit)
              if exitOnFirst and result:
                return result
def check_axis_binned(chart,axis):
    is_meaningful = is_axis_binned(chart,axis)
    
    # if a layered chart, 
    if alt_get(chart,'layer'):
        for layer in chart.layer:
            if is_axis_binned(layer,axis):
                return True
    return is_meaningful


def check_axis_aggregate(chart,axis):
    is_aggregate = is_axis_aggregate(chart,axis)
    
    attributes_for_recursion = ['layer','hconcat','vconcat']
    for attribute in attributes_for_recursion:
        if alt_get(chart,attribute):
          # TODO, make this recursive instead of one layer deep
          for unit_spec in chart[attribute]:
            if not is_axis_aggregate(unit_spec,axis):
                return False
           
    return is_aggregate

def extent_from_column(data,column):
    if alt.utils.infer_vegalite_type(data[column]) == 'ordinal' or alt.utils.infer_vegalite_type(data[column]) == 'nominal':
        return np.unique(data[column])
    elif alt.utils.infer_vegalite_type(data[column]) == 'temporal':
        # TODO: fix error where a month is specified
        # ie we want to create a stacked bar chart by months, even with a temporal column, we should have an ordinal value
        return [np.min(data[column]).isoformat().replace("NaT", ""),np.max(data[column]).isoformat().replace("NaT", "")]
    else: 
        # default to quantitative 
        return [np.min(data[column]),np.max(data[column])]
        
def get_field_from_unit_encoding(chart,encoding):
    if getattr(chart,'encoding',None) == None or is_undefined(chart.encoding):
      return None
    # check if field is there
    if not is_undefined(getattr(chart.encoding[encoding],'field','Undefined')) :
        return chart.encoding[encoding].field
    elif not is_undefined(getattr(chart.encoding[encoding],'shorthand','Undefined')):
        shorthand = chart.encoding[encoding].shorthand
        CODES = [':Q',':O',':N',':T',':G']
        for code in CODES:
          shorthand = shorthand.replace(code,'')
        return shorthand
    return None

def get_field_from_encoding(chart,axis):
    attributes_for_recursion = ['layer','hconcat','vconcat']
    for attribute in attributes_for_recursion:
        if alt_get(chart,attribute):
          # TODO, make this recursive instead of one layer deep
          for unit_spec in chart[attribute]:
              if get_field_from_unit_encoding(unit_spec,axis):
                  return get_field_from_unit_encoding(unit_spec,axis)

    return get_field_from_unit_encoding(chart,axis)

def data_type_converter(data_type):
  #TODO: add ordinal/maybe geojson
  if data_type == np.dtype('datetime64[ns]'):
    return 'T'#temporal
  elif data_type == np.int64 or data_type == np.float64:
    return 'Q'#quantitative
  elif data_type == np.string_ or data_type == np.object0:
    return 'N'#nominal
  else:
    raise ValueError('[data_type_converter] data_type ' + str(data_type) + ' is not mappable to a vl datatype')




def create_dataframe(data=None, *, x=None, y=None):
  # create data if x and y are pandas series
  if data is None:
    if isinstance(x, pd.Series) and isinstance(y, pd.Series):
      # TODO: make general so if x or y aren't provided
      data = pd.DataFrame({'x':x,'y':y})

      x = 'x'
      y = 'y'

      if size is not None:
        data['size'] = size
        size = 'size'
    else : 
      raise ValueError('[process inputs] no dataframe provided or no series from x and y')
  return data,x,y