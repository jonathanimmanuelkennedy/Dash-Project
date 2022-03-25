#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.offline as pyo
import plotly.graph_objs as go
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.io as pio
import flask
from plotly.subplots import make_subplots

server = flask.Flask(__name__) # define flask app.server

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

#Import all the required data files in csv.
df= pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv")
df_rec = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv")
df_confirmed=pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv")
df_daily= pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/05-12-2021.csv")
#df_bed=pd.read_csv("covid_treatment.csv")
df_bed=pd.read_csv("/Users/jonathanimmanuelkennedy/Downloads/data/covid_treatment.csv")
df_vaccine =pd.read_csv("https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations.csv")

#Death Count for India
fig_death = go.Figure()
fig = go.Figure()
df.drop(['Province/State','Lat','Long'],axis=1,inplace=True)
df_new =df.melt(id_vars=["Country/Region"], 
        var_name="Date", 
        value_name="No_of_death")
India = df_new[df_new["Country/Region"]=='India']
#fig = make_subplots(specs=[[{"secondary_y": True}]])

fig_death.add_trace(
    go.Scatter(
    x = India['Date'],
    y = India['No_of_death'],
    mode = 'lines',
    name = 'DeathCount'),
   # secondary_y=True,
)

# Recovered Count for India
df_rec.drop(['Province/State','Lat','Long'],axis=1,inplace=True)
df_rec1=df_rec.melt(id_vars=["Country/Region"], 
        var_name="Date", 
        value_name="Recovered_count")
India_rec = df_rec1[df_rec1["Country/Region"]=='India']

fig.add_trace(
   go.Scatter(
    x = India_rec['Date'],
    y = India_rec['Recovered_count'],
    mode = 'lines',
    name = 'RecoveredCount',
    ),
    #secondary_y=False,
)

# Confirmed Count for India
df_confirmed.drop(['Province/State','Lat','Long'],axis=1,inplace=True)
df_conf=df_confirmed.melt(id_vars=["Country/Region"], 
        var_name="Date", 
        value_name="Confirmed_cases_Count")
India_conf = df_conf[df_conf["Country/Region"]=='India']

fig.add_trace(
   go.Scatter(
    x = India_conf['Date'],
    y = India_conf['Confirmed_cases_Count'],
    mode = 'lines',
    name = 'ConfirmedCount',
    ),
    #secondary_y=False,
)

fig.update_layout(template='plotly_white',title_text="Covid Confirmed/Recovered Count in India")
#fig.update_xaxes(title_text="Date") 
#fig.update_yaxes(title_text="Confirmed/Recovered Count", secondary_y=False)
#fig.update_yaxes(title_text="Death Count", secondary_y=True)
fig_death.update_layout(template='plotly_white',title_text="Death Count in India")
#fig_death.update_xaxes(title_text="Date") 

#Confirmed Cases across the world
world_conf= df_conf.groupby(['Country/Region'])['Country/Region',
                               'Confirmed_cases_Count'].sum().reset_index()
sorted_world_conf = world_conf.sort_values('Confirmed_cases_Count', ascending= False)
sorted_world_conf=sorted_world_conf.head(10)

trace_wc = go.Bar(
    x = sorted_world_conf['Country/Region'],
    y = sorted_world_conf['Confirmed_cases_Count'],
   # mode = 'markers',
    name = 'Covid Confirmed Count',
    marker=dict(
        color='rgba(246, 78, 139, 0.6)',
        line=dict(color='rgba(246, 78, 139, 1.0)', width=3)
   
))

#Recovered Cases across the world -scatter

world_rec= df_rec1.groupby(['Country/Region'])['Country/Region',
                                 'Recovered_count'].sum().reset_index()
sorted_world_rec = world_rec.sort_values('Recovered_count', ascending= False)
sorted_world_rec=sorted_world_rec.head(10)

trace_wr = go.Scatter(
    x = sorted_world_rec['Country/Region'],
    y = sorted_world_rec['Recovered_count'],
    mode = 'markers',
    marker=dict(
        color='rgba(246, 78, 139, 0.6)',
        line=dict(color='rgba(246, 78, 139, 1.0)', width=6)),
    name = 'Covid Recovered Count'
)


#Death count across the World
world_death= df_new.groupby(['Country/Region'])['Country/Region',
                                 'No_of_death'].sum().reset_index()
sorted_world_death = world_death.sort_values('No_of_death', ascending= False)
sorted_world_death=sorted_world_death.head(10)

trace_wd = go.Bar(
    y = sorted_world_death['Country/Region'],
    x = sorted_world_death['No_of_death'],
   # mode = 'markers',
    name = 'Covid Death Count',
    orientation='h',
    marker=dict(
        color='rgba(246, 78, 139, 0.6)',
        line=dict(color='rgba(246, 78, 139, 1.0)', width=3)
))

# Active Covid Cases by States in India
country= df_daily.groupby(['Country_Region','Province_State'])['Country_Region',
                                 'Province_State','Confirmed','Deaths','Recovered','Active'
                                          ].sum().reset_index()
India_daily =country[country['Country_Region']=='India']
#India_daily=India_daily.sort_values(by=['Recovered'],ascending=False)
India_daily=India_daily.drop(index=[211])
fig_pie = px.pie(India_daily, values='Active', names='Province_State',hole=.3,title='Active Covid Cases in Indian States')
fig_pie.update_traces(textposition='inside')
fig_pie.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')

# Death Rate by States in India
fig_pie1 = px.pie(India_daily, values='Deaths', names='Province_State',hole=.3,title='Death Rate By States')
fig_pie1.update_traces(textposition='inside')
fig_pie1.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')


# Recovered Covid Cases by States in India
fig_pie2 = px.pie(India_daily, values='Recovered', names='Province_State',hole=.3,title='Recovered Cases in Indian States')
fig_pie2.update_traces(textposition='inside')
fig_pie2.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')


#Bed Status Availability
district= df_bed.groupby(['Date','District'])['District',
                               'OXYGEN SUPPORTED BEDSOccupied','OXYGEN SUPPORTED BEDSVacant','VENTILATOR Vacant'].sum().reset_index()
district_inst= df_bed.groupby(['District','Institution'])['District','Institution',
                                 'OXYGEN SUPPORTED BEDSOccupied','OXYGEN SUPPORTED BEDSVacant',
                                                      'ICU BEDS Occupied','ICU BEDS Vacant'
                                          ].sum().reset_index()
#chennai_hosp=district_inst[district_inst['District']=='Chennai']
cities_option = df_bed['District'].unique()


#Vaccinations
country= df_vaccine.groupby(['location','iso_code'])['location','people_fully_vaccinated','people_vaccinated'
                                                     ,'iso_code' ].sum().reset_index()
country_index = country.set_index("iso_code")
country_index=country_index.drop(["OWID_WRL","OWID_HIC","OWID_NAM",'OWID_EUR',"OWID_ASI",
                                  "OWID_UMC","OWID_EUN","OWID_SAM","GBR","OWID_AFR","OWID_LMC"])
sorted_country_df = country_index.sort_values('people_fully_vaccinated', ascending= False)
#sorted_country_df = country.sort_values('people_fully_vaccinated', ascending= False)
sorted_country_df=sorted_country_df.head(10)
trace10 = go.Bar(
    x=sorted_country_df['location'],
    y=sorted_country_df['people_fully_vaccinated'],
    name = 'People Fully Vaccinated',
    marker=dict(color='#FFD700')
   )
trace11= go.Bar(
    x = sorted_country_df['location'],
    y = sorted_country_df['people_vaccinated'],
    name='people_vaccinated_with_onedose',
    marker=dict(color='#9EA0A1') 
)
                        
#initializing dash
#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app = dash.Dash(__name__, external_stylesheets=external_stylesheets, server=server)

app.layout = html.Div([
    dcc.Tabs([
        
               
        dcc.Tab(label='COVID STATUS IN INDIA', children=[
            dcc.Graph(figure=fig),
            dcc.Graph(figure=fig_death),
        ]),            

        
        dcc.Tab(label='COVID STATUS BY INDIAN STATES', children=[
            dcc.Graph(figure=fig_pie), 
            dcc.Graph(figure=fig_pie1), 
            dcc.Graph(figure=fig_pie2), 
        ]),
        dcc.Tab(label='BED AVAILABILTY IN TAMILNADU HOSPITALS', children=[
            dcc.Dropdown(
                id="city",
                options=[{
                    'label': i,
                    'value': i
                } for i in cities_option],
                value='SELECT A DISTRICT',
                style=  { 'width': '1200px','background-color': '#D3D3D3',
                                    },

                placeholder="Select a District from the dropdown"),
            
             dcc.Graph(id='funnel-graph'),           
        ]),
        
         dcc.Tab(label='VACCINATION STATUS ACROSS COUNTRIES', children=[
            dcc.Graph(
                figure={
                    'data': [trace10,trace11]
                }           
            )
         ]),
        
         dcc.Tab(label='COVID STATUS ACROSS COUNTRIES', children=[
            dcc.Graph(
                figure={
                    'data': [trace_wc],   
                    'layout' : {
                    'title': 'Confirmed Cases Count in Countries Across the World (Top 10)'                   
                    } }   
            ),
             dcc.Graph(
                figure={
                    'data': [trace_wr],   
                    'layout' : {
                    'title': 'Recovered Cases Count in Countries Across the World (Top 10)'                   
                    } }   
            ),
              dcc.Graph(
                figure={
                    'data': [trace_wd],
                     'layout' : {
                    'title': 'Death Count in Countries Across the World (Top 10)'                  
                    }
                    }
            ),
        ]),
               
    ])
])

@app.callback(
    dash.dependencies.Output('funnel-graph', 'figure'),
    [dash.dependencies.Input('city', 'value')])

def update_graph(city):
    if city == "SELECT A DISTRICT":
        df_plot = df_bed.copy()
    else:
        df_plot = district_inst[district_inst['District'] == city]

    pv = pd.pivot_table(
      df_plot,
          index=['Institution'],
          columns=["District"],
          values=['OXYGEN SUPPORTED BEDSVacant','OXYGEN SUPPORTED BEDSOccupied','ICU BEDS Occupied','ICU BEDS Vacant'],
          aggfunc=sum,
          fill_value=0)

    trace6 = go.Bar(x=pv.index, y=df_plot['OXYGEN SUPPORTED BEDSVacant'] ,name='OXYGEN SUPPORTED BEDSVacant')
    trace7 = go.Bar(x=pv.index, y=df_plot['OXYGEN SUPPORTED BEDSOccupied'], name='OXYGEN SUPPORTED BEDSOccupied')
    trace8 = go.Bar(x=pv.index, y=df_plot[('ICU BEDS Occupied')], name='ICU BEDS Occupied')
    trace9 = go.Bar(x=pv.index, y=df_plot[('ICU BEDS Vacant')], name='ICU BEDS Vacant')
    return {
            'data': [trace6, trace7,trace8,trace9],
            'layout': go.Layout(
            title='Bed Status Availabilty(As of June 2 2021)',
            barmode='stack')
    }

if __name__ == '__main__':
    app.run_server()


# In[ ]:





# In[ ]:




