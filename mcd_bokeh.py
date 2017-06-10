from bokeh.io import show, output_notebook, curdoc
from bokeh.layouts import row, column
from bokeh.models import ColumnDataSource, HoverTool, Select
from bokeh.plotting import figure
from bokeh.layouts import widgetbox
import pandas as pd

def subset(df, category):
    df2 = df[df['Category'] == category].copy()
    df2 = df2.sort_values('Calories', ascending = False)
    df2 = df2.reset_index(drop=True).reset_index()
    return ColumnDataSource(df2)

def update_plot(attrname, old, new):
    category = select.value
    df3 = subset(test, category)
    source.data.update(df3.data)

mcd = pd.read_csv('C:/Users/Matt/Documents/GitHub/Bokeh-Example/menu.csv')
select = Select(title="Category:", value="Breakfast", options=mcd['Category'].unique().tolist())

df = mcd[['Category', 'Item', 'Total Fat', 'Carbohydrates', 'Protein', 'Sugars', 'Cholesterol']]
test = df.copy()
test['Calories'] = test['Total Fat']*9.0 + test['Carbohydrates']*4.0 + test['Protein']*4.0
test['h1'] = test['Protein']
test['h2'] = test['Protein'] + test['Total Fat']
test['h3'] = test['Protein'] + test['Total Fat'] + test['Carbohydrates']

df1 = test[test['Category'] == 'Breakfast']
df1 = df1.sort_values('Calories', ascending = False).reset_index(drop=True).reset_index()

source = ColumnDataSource(df1)
TOOLS = "pan, wheel_zoom, reset, save"
hover = HoverTool(tooltips=[
            ("Name", "@Item"),
            ("Calories", "@Calories"),
            ("Fat", "@{Total Fat}"),
            ("Carbohydrates", "@Carbohydrates"),
            ("Protein", "@Protein")
        ])

p = figure(title="McDonalds Nutrition Info", tools=TOOLS)
p.add_tools(hover)
p.vbar(x = 'index',  width = .8, bottom =0, top = 'h1', color = 'orange', source = source)
p.vbar(x = 'index',  width = .8, bottom = 'h1', top = 'h2', color = 'yellow', source = source)
p.vbar(x = 'index',  width = .8, bottom ='h2', top = 'h3', color = 'brown', source = source)

select.on_change('value', update_plot)

controls = column(select)
curdoc().add_root(row(p, controls))

# bokeh serve --show "c:/Users/Matt/Documents/GitHub/Bokeh-Example/mcd_bokeh.py"
