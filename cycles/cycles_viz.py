#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  1 12:53:35 2019

@author: deborahkhider

Visualization for Cycles using a lookup table 
"""
import pandas as pd
from collections import defaultdict
from bokeh.layouts import row, column, widgetbox, gridplot
from bokeh.models import Slider, LabelSet, Legend, Plot, LinearAxis, Grid, MultiLine, HoverTool
from bokeh.plotting import figure, output_file, show, ColumnDataSource, curdoc
from bokeh.palettes import Spectral5
from bokeh.transform import factor_cmap 
from bokeh.models.glyphs import VBar, Wedge, Line, Text
from math import pi
from bokeh.transform import cumsum
from bokeh.models.widgets import Div, Paragraph, Dropdown
import numpy as np

def update_all(attr,old,new):
    # Get values for everything
    year_dynamic = slider_year.value
    planting_dynamic = slider_planting.value
    
    # filter based on widgets criteria
    if dd_crop.value == 'sorghum':
        df_filter = sorghum_data[(sorghum_data['location']==dd_loc.value) & \
                                    (sorghum_data['year']==year_dynamic) &\
                                    (sorghum_data['planting_date_fixed']==True) &\
                                    (sorghum_data['planting_date']==planting_dynamic)]
    elif dd_crop.value == 'maize':
        df_filter = maize_data[(maize_data['location']==dd_loc.value) & \
                                    (maize_data['year']==year_dynamic) &\
                                    (maize_data['planting_date_fixed']==True) &\
                                    (maize_data['planting_date']==planting_dynamic)]
    else:
        print("Dropdown value is incorrect")
        
    #update the plot
    weeds = df_filter['weed_fraction'].unique()
    weeds = np.sort(weeds)
    #empty list
    NR=[]
    weedF =[]
    yearS=[]
    GY =[]
    annotation=[]
    for weed in weeds:
        #calculate unique values
        df_temp = df_filter[df_filter['weed_fraction']==weed]
        df_temp2 = df_temp.groupby('nitrogen_rate').mean().reset_index()
        NR.append(np.array(df_temp2['nitrogen_rate']))
        weedF.append(weed)
        yearS.append(np.array(df_temp2['year']))
        GY.append(np.array(df_temp2['yield']))
        annotation.append([dd_crop.value.capitalize()+': '+ dd_loc.value])
    source.data['nitrogen_rate']=NR
    source.data['weed_fraction']=weedF
    source.data['year']=yearS
    source.data['yield']=GY
    source.data['annotation']=annotation


#Get the data
global sorghum_data
sorghum_data = pd.read_csv('cycles/sorghum.csv')
global maize_data
maize_data = pd.read_csv('cycles/maize.csv')
# Get a loc to get started
loc = sorghum_data['location'].unique()
#filter a little bit for the first cut
sorghum_data_filter = sorghum_data[(sorghum_data['location']==loc[0]) & \
                                    (sorghum_data['year']==2001) &\
                                    (sorghum_data['planting_date_fixed']==True) &\
                                    (sorghum_data['planting_date']==121)]

# available weed:
weeds = sorghum_data_filter['weed_fraction'].unique()
weeds = np.sort(weeds)
# Pick one location for the default plot
sd = defaultdict(list)

for weed in weeds:
    #calculate unique values
    df_temp = sorghum_data_filter[sorghum_data_filter['weed_fraction']==weed]
    df_temp2 = df_temp.groupby('nitrogen_rate').mean().reset_index()
    #sd['location'].append(np.array(df_temp2['location']))
    sd['nitrogen_rate'].append(np.array(df_temp2['nitrogen_rate']))
    sd['weed_fraction'].append(weed)
    sd['year'].append(np.array(df_temp2['year']))
    sd['yield'].append(np.array(df_temp2['yield']))
    sd['annotation'].append(['Sorghum: '+ str(loc[0])])

sd['color'] = Spectral5
#sd['annotation']='Sorghum: '+ str(loc[0])

source = ColumnDataSource(sd)

p = figure(plot_height=400, toolbar_location=None, y_range=(0, 12))
p.multi_line(xs='nitrogen_rate',ys='yield', legend = 'weed_fraction',line_width=3,
             line_color='color',
             hover_line_color='color', hover_line_alpha=1.0,
             source=source)
glyph = Text(x=100,y=11,text='annotation')
p.add_glyph(source, glyph)
p.add_tools(HoverTool(show_arrow=False, line_policy='next', tooltips=[
    ('Yield', '@yield'),
    ('Weed Fraction', '@weed_fraction')
]))

p.legend.location = "bottom_right"
    
xaxis = LinearAxis()
#p.add_layout(xaxis, 'below')
p.xaxis.axis_label = 'Nitrogen Rate (kgN/ha)'

yaxis = LinearAxis()
#p.add_layout(yaxis, 'left')
p.yaxis.axis_label = 'Grain Yield (Mg/ha)'

p.add_layout(Grid(dimension=0, ticker=xaxis.ticker))
p.add_layout(Grid(dimension=1, ticker=yaxis.ticker))

# Start adding call backs
# dropdown menu to choose crop
menu_crop = [("Sorghum", "sorghum"), ("Maize", "maize")]
dd_crop = Dropdown(label="Crop", button_type="primary", menu=menu_crop,
                   value = 'sorghum')
dd_crop.on_change('value', update_all)

# Dropdown for location
menu_loc = []
for item in loc:
    menu_loc.append(tuple((item,item)))
dd_loc = Dropdown(label="Location", button_type="primary", menu=menu_loc,
                  value = menu_loc[0][1])
dd_loc.on_change('value', update_all)

# Sliders for the year
slider_year = Slider(start=2000, end=2017, value=2000,
                           step=1, title="Year")
slider_year.on_change('value', update_all)

#Slider for planting time
slider_planting = Slider(start=100, end = 142, value =121, 
                         step =7, title="Start of Planting Window (Day of calendar year)")
slider_planting.on_change('value', update_all)



layout = row(p,widgetbox(dd_crop, dd_loc, slider_year,slider_planting))
curdoc().add_root(layout)
#show(layout)