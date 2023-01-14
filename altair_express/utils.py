import numpy as np
import pandas as pd
import altair as alt

def is_axis_aggregate(chart,axis):
    if is_undefined(chart.encoding):
        return False
    
    encoding = chart.encoding[axis]
    AGGREGATION_NAMES = ["count","sum","distinct","missing","mean","average","variance","stdev"]

    if encoding:
        print((chart.to_dict()['encoding']).get(axis))
        axis_encode = chart.to_dict()['encoding'].get(axis)
        if axis_encode is None:
            return False
        
        encode_string = f'{axis_encode}'
        for aggregation_name in AGGREGATION_NAMES:
            if encode_string.find(aggregation_name) > -1:
                return False
        return True
    else: 
        return False
    
def alt_get(chart,prop):
    return prop in dir(chart)

def is_undefined(obj):
    return str(obj) == 'Undefined'

def check_axis_meaningful(chart,axis):
    is_meaningful = is_axis_aggregate(chart,axis)
    
    # if a layered chart, 
    if alt_get(chart,'layer'):
        for layer in chart.layer:
            if is_axis_aggregate(layer,axis):
                return True
    return is_meaningful

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
    print('getting field',encoding)
    # check if field is there
    if not is_undefined(getattr(chart.encoding[encoding],'field','Undefined')) :
        return chart.encoding[encoding].field
    elif not is_undefined(getattr(chart.encoding[encoding],'shorthand','Undefined')):
        return chart.encoding[encoding].shorthand[:-2]
    return None

def get_field_from_encoding(chart,axis):
    print('in gett field',axis)
    if alt_get(chart,'layer'):
        print('in layer')
        for layer in chart.layer:

            if get_field_from_unit_encoding(layer,axis):
                
                return get_field_from_unit_encoding(layer,axis)
    
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