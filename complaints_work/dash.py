import pandas as pd
from bokeh.io import curdoc
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, Select
from bokeh.plotting import figure

df = pd.read_csv('monthly_res_t.csv')

df['month'] = pd.to_datetime(df['month'])

zipcodes = df['zip_code'].unique().tolist()

source = ColumnDataSource(data=dict(month=[], response_time_all=[], response_time_zip1=[], response_time_zip2=[]))
p = figure(title="Monthly Average Response Time (in hours)", x_axis_label="Month", y_axis_label="Response Time (hours)",
           x_axis_type='datetime', width=1000, height=600)
p.line(x='month', y='response_time_all', source=source, legend_label="Avg(all)", color="blue")
p.line(x='month', y='response_time_zip1', source=source, legend_label="Zip Code 1",color="green")
p.line(x='month', y='response_time_zip2', source=source, legend_label="Zip Code 2",  color="red")
p.legend.location = "top_right"

zip1_select = Select(title="Select Zip Code 1", value=str(zipcodes[0]), options=[str(z) for z in zipcodes])
zip2_select = Select(title="Select Zip Code 2", value=str(zipcodes[1]), options=[str(z) for z in zipcodes])

def update_plot():
    zip1 = zip1_select.value
    zip2 = zip2_select.value
    all_zip_data = df.groupby('month')['response time'].mean().reset_index()
    zip1_data = df[df['zip_code'] == int(zip1)]
    zip2_data = df[df['zip_code'] == int(zip2)]
    source.data = dict(month=pd.to_datetime(all_zip_data['month']),
        response_time_all=all_zip_data['response time'],
        response_time_zip1=zip1_data['response time'].values,
        response_time_zip2=zip2_data['response time'].values
    )
zip1_select.on_change('value', lambda x, o, n: update_plot())
zip2_select.on_change('value', lambda x, o, n: update_plot())
update_plot()

layout = column(zip1_select, zip2_select, p)
curdoc().add_root(layout)
curdoc().title = "NYC 311 Response Time Dashboard"
