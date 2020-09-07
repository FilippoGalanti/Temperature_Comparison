# Temperature Comparison

This script allows you to compare the last 5 days hourly temperature of 2 cities. The output is a heatmap put together using plotly (<a href="https://plotly.com/python/heatmaps/">Plotly Documentation</a>). Since OpenWeather requires longitude / latitude to output something this script is using forward (text to lat/long) geocoding using OpenCage API.

img

<b>Prerequisites</b>

Python Libraries:

 <ul>
  <li>Time and Datetime;</li>
  <li>Requests;</li>
  <li>Pandas</li>
  <li>Plotly</li>
</ul>

The script also requires these 2 APIs to properly work (both are free for this limited use:

<ul>
  <li><a href="https://opencagedata.com/api#intro">OpenCage</a> to retrieve latitute and logitude of the selected cities;</li>
  <li><a href="https://openweathermap.org/api/one-call-api#history">OpenWeather</a> to retrieve temperature information for the chosen cities.</li>
</ul>

<b>Output</b>

The output is a Plotly heatmap that display the last 5 days of hourly temperature in Celsius degree. This can be changed to Fahrenheit updating the request to the API.

<b>Future Developments</b>

As of today there are no future developments for this script. It's a straightforward project done to get more familiar with APIs and Plotly so it does not really need any additional work.
