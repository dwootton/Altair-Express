import numpy as np
import pandas as pd

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