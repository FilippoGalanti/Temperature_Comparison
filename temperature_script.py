import time
import pandas as pd
import plotly.offline as pyo
import plotly.graph_objs as go 
import plotly.subplots as ps 
import requests
import datetime

def date_conversion(date):
    return datetime.datetime.strftime(date, '%b %d, %Y')

key_weather = '#######################'
key_geo = '########################'
unixtime_list = []

print("This script retrieve the last 5 days of hourly temperature for the selected cities.")

for n in range(0, 5):
    day = datetime.date.today() - datetime.timedelta(n)
    unixtime = int(time.mktime(day.timetuple()))
    unixtime_list.append(unixtime)

geo_input1, geo_input2 = False, False

while geo_input1 == False:

    city = input('First city (format is "City Country"):')
    city_list = city.split(' ')
    city_string = '+'.join(city_list)

    geo_url1 = f"https://api.opencagedata.com/geocode/v1/google-v3-json?address={city_string}&pretty=1&key={key_geo}&min_confidence=8"

    feedback = requests.get(geo_url1)

    if feedback.status_code != 200:
        print("\nPlease fix the inputs.\n")
        print(feedback.json())
        continue
    else:
        geo_input1 = True

data_geo1 = requests.get(geo_url1).json()
lat1 = data_geo1['results'][1]['geometry']['location']['lat']
lon1 = data_geo1['results'][1]['geometry']['location']['lng']

while geo_input2 == False:

    city2 = input('Second city (format is "City Country"):')
    city_list2 = city2.split(' ')
    city_string2 = '+'.join(city_list2)

    geo_url2 = f"https://api.opencagedata.com/geocode/v1/google-v3-json?address={city_string2}&pretty=1&key={key_geo}&min_confidence=8"

    feedback = requests.get(geo_url2)

    if feedback.status_code != 200:
        print("\nPlease fix the inputs.\n")
        print(feedback.json())
        continue
    else:
        geo_input2 = True

data_geo2 = requests.get(geo_url2).json()
lat2 = data_geo2['results'][1]['geometry']['location']['lat']
lon2 = data_geo2['results'][1]['geometry']['location']['lng']

def get_data (lat, lon):
    df_weather = pd.DataFrame()
    for time in unixtime_list:
        weather_url = f'https://api.openweathermap.org/data/2.5/onecall/timemachine?lat={lat}&lon={lon}&dt={time}&appid={key_weather}&units=metric'
        data_weather = requests.get(weather_url).json()
        df = pd.DataFrame(pd.json_normalize(data_weather['hourly']))
        # append doesn't happen in-place
        df_weather = df_weather.append(df[['dt', 'temp']])
    return df_weather

df_weather1, df_weather2 = get_data(lat1, lon1), get_data(lat2, lon2)

def adjust_data(df_weather):
    df_weather.set_index('dt', inplace=True)
    df_weather['Date_Time'] = pd.to_datetime(df_weather.index, unit='s')
    df_weather['day'] = df_weather['Date_Time'].dt.date
    df_weather['hour'] = df_weather['Date_Time'].dt.strftime('%H:%M')
    return(df_weather)

df_weather1, df_weather2 = adjust_data(df_weather1), adjust_data(df_weather2)

min_date, max_date = df_weather1['day'].min(), df_weather1['day'].max()
min_temp = min(df_weather1['temp'].min(), df_weather2['temp'].min())
max_temp = max(df_weather1['temp'].max(), df_weather2['temp'].max())

trace1 = go.Heatmap(x=df_weather1['day'], y=df_weather1['hour'],
                    z=df_weather1['temp'].values.tolist(), colorscale='RdYlBu_r', 
                    reversescale=False, hoverinfo='z',
                    zmin=min_temp, zmax=max_temp)

trace2 = go.Heatmap(x=df_weather2['day'], y=df_weather2['hour'],
                    z=df_weather2['temp'].values.tolist(), colorscale='RdYlBu_r',
                    reversescale=False, hoverinfo='z',
                    zmin=min_temp, zmax=max_temp)

fig=ps.make_subplots(rows=1, cols=2, subplot_titles=(f'{city.title()}', f'{city2.title()}'), shared_yaxes=True)

fig.append_trace(trace1, row=1, col=1)
fig.append_trace(trace2, row=1, col=2)

fig.update_layout(
    title_text=f"Hourly Temperature between {date_conversion(min_date)} - {date_conversion(max_date)}.")
pyo.plot(fig)
