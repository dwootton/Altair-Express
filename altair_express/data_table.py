import altair as alt
from .distributional import hist, countplot
from pandas.api.types import is_numeric_dtype

def data_table(data=None,vars=None,row_limit=25):
  if vars is None:
    vars = data.columns
  
  # sort so they're in line with the table marks
  if type(vars) is list:
    vars.sort()
  
  brush = alt.selection_interval(name='brush', resolve="intersect")
  picker = alt.selection_single(name='picker',encodings=['x'],resolve='union')
  charts = []

  column_width = 90

  chart_padding = 15
  chart_width = column_width-chart_padding

  for index, variable in enumerate(vars):
    if index == 0:
         spacer = alt.Chart(data=data).mark_circle(size=2,opacity=0).encode(
             alt.X(variable,axis=None),
             alt.Y(variable,axis=None)
         ).properties(width=chart_width-50, height=50)
         charts.append(spacer)
         
    chart_index = index + 1 # for spacer
    if(is_numeric_dtype(data[variable])):

      charts.append(hist(data = data,x = variable,width=chart_width,interactive=brush,xAxis=None,yAxis=None,filters=[picker]))

      brush_name = brush.name
      signal_index = f'{brush_name}.{variable}'
      max=np.max(data[variable])
      min=np.min(data[variable])
      bounds = alt.hconcat(alt.Chart(data=pd.DataFrame({'min':['']}))
            .transform_calculate(calculate=f"{signal_index} ? +format({signal_index}[0],'.2f'):+format({min},'.2f')", as_="min")
            .mark_text()
            .encode(alt.Text(field='min')),
          alt.Chart(data=pd.DataFrame({'max':['']})).transform_calculate(calculate=f"{signal_index} ? +format({signal_index}[1],'.2f'):+format({max},'.2f')", as_="max")
            .mark_text()
            .encode(alt.Text(field='max'))
          
          )
      
      
      charts[chart_index] = alt.vconcat(charts[chart_index],bounds, spacing=0)
    else:
      print(f'not numeric {variable}')
      # append blank till count plot are ready
      spacer = countplot(data=data,x=variable,interactive=picker,width=column_width,height=50,filters=[brush],xAxis=None,yAxis=None)
      signal_index = False
      bounds = alt.hconcat(alt.Chart(data=pd.DataFrame({'min':['_']}))
            .mark_text()
            .encode(alt.Text(field='min')),
          alt.Chart(data=pd.DataFrame({'max':['_']}))
            .mark_text()
            .encode(alt.Text(field='max'))
          
          )

      charts.append(spacer)
      charts[chart_index] = alt.vconcat(charts[chart_index],bounds, spacing=0)

  merged = alt.hconcat(*charts, spacing=chart_padding)# 8 seconds

  # for each column to view
  text_width = column_width - chart_padding
  table_width = column_width * (len(vars)+1)


  
  table = (alt.Chart(data)
    .transform_filter(brush)
    .transform_filter(picker)
    .transform_window(window=[{"op":"row_number","as":"row_num"}])
    .transform_filter(
        alt.FieldLTEPredicate(field='row_num', lte=row_limit)
    )
    .transform_fold(list(vars))
    .mark_text(align='center', limit=text_width)
    .encode(
        alt.Y(field="row_num",type="ordinal", axis=None),
        alt.Text(field="value",type="nominal"),
        alt.X(field="key",sort=list(vars), type="nominal",scale=alt.Scale(padding=chart_padding,rangeMax=table_width),axis=alt.Axis(orient="top",labelAngle= 0,title=None, domain=False, ticks=False)))
  ).properties(width=table_width).add_selection(brush).add_selection(picker)
  return alt.vconcat(merged,table,spacing=0)
