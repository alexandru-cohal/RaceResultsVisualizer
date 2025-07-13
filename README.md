# RaceResultsVisualizer

## [Draft] Requirements
The race_results.csv file shall contain the results of all the races to be included in the app.
* The separator shall be the comma symbol.
* The column names shall be: "name", "distance", "date", "city", "country", "duration", "pace", "gpxfilename".
  * The column "name" shall contain the name of the race.
    * The race name shall be introduced as a string delimited by double quotes.
    * Note: This way, the name can contain comma symbols without affecting the structure of the .csv file.
  * The column "distance" shall contain the official distance of the race.
    * The race distance value shall be introduced as a floating-point number.
    * The fractional part of the race distance value shall be separated with the dot symbol. 
  * The column "date" shall contain the date of the race.
    * The race date value shall be introduced in the format YYYY-MM-DD, where Y represents a digit of the year value, M represents a digit of the month value, D represents a digit of the day value.
  * The column "city" shall contain the name of the city where the race took place.
    * The race city name shall be introduced as a string delimited by double quotes.
  * The column "country" shall contain country where the race took place.
    * The race country name shall be introduced as a string delimited by double quotes.
  * The column "duration" shall contain the official duration needed to finish the race (i.e. the duration between the initial and final moments where the barrier containing the sensors for reading the chips for identifying the participants are crossed).
    * The race duration value shall be introduced in the format H:MM:SS, where H represents a digit of the hour value, M represents a digit of the minute value, S represents a digit of the second value.
  * The column "pace" shall contain the official pace of the race (i.e. average time needed to cover one kilometer).
    * The race pace shall be introduced in the format HH:MM:SS, where H represents a digit of the hour value, M represents a digit of the minute value, S represents a digit of the second value.
  * The column "gpxfilename" shall contain the name of the file containing the logged data during the race (i.e. location, elevation, timestamp).
    * The name of the file shall be introduced as a string delimited by double quotes and shall include the ".gpx" extension.

The plots shall show the following information:
* Plot_1 shall show the evolution of the average time per km for all the races.
* Plot_2 shall show the number of races for each distance.
* Plot_3 shall show the locations of all the races on a map.
* Plot_4 shall show the routes of all the races on a map.
* After selecting one of the races from a dropdown list:
  * Plot_5 shall show the route of the race on a map.
  * Plot_6 shall show the elevation profile.

## To Do:
* Improve time per km plot (set different marker colors for different race lengths, add legend of colors)
  * Solution: Plot firstly the line and then overlap for each type of distance only the markers by using the _add_trace_ function (like it was done in the _plot_route_ function for the start and end points).
* ~~Remove the columns with the starting point location (i.e. "lat" and "lon") from the .CSV file as the same information can be obtained now from the first entry of the .GPX file. Adapt the code.~~
* ~~Rethink the get_lan_lon_elev function and its usage (it is called 2 times, once for latitude and longitude and second time only for elevation).~~
* Check the whole code if the best ways to access the rows and cells of the dataframe (i.e. loc, at) are used.
* ~~Rethink parse_gpx_file function (are 4 lists the best way to keep and return the latitude, longitude, elevation and timestamp data?).~~
* ~~Create a settings.json file and move the GPX_FILEPATH variable in it. Add also the .CSV file path in it. Adapt the code.~~
* ~~Improve the elevation plot~~ (~~continuous line (not only discrete points)~~, ~~axis labels~~, ~~hover display data~~).
* ~~Improve the route plot~~ (~~continuous line (not only discrete points)~~, ~~different markers for start and end points~~, ~~hover display data~~, ~~zoom~~, ~~alignment~~).
* ~~Calculate distance and time since start based on the data from the .GPX file and show it on the route and elevation plots.~~
* ~~Based on the previously calculated distance and time since start, calculate and plot the pace~~
* ~~Add to the .CSV file the average official pace.~~ ~~Calculate the average pace based on the .GPX data. Show the average official pace and the average calculated pace in the pace plot.~~
* ~~Reduce the _from_str_to_timedelta_ and _from_str_to_timedelta_pace_ functions to a single generic one. Adapt the code.~~
* Add combined plot route & elevation (with correlation between hovered point -> hover on subplots).
  * Solution: Use _plotly.graph_object_ and the attributes _hoversubplots_ and _hovermode_ (see https://plotly.com/python/hover-text-and-formatting/#hover-on-subplots).
* Add possibility to select race from the map of starting points and have the same effect as the dropdown list selection.
  * Solution: Use plotly.graph_objects and FigureWidget (see https://plotly.com/python/click-events/). 
* ~~Check if on the X-axis of the elevation plot, the samples is the best choice.~~
* ~~Calculate and display also a percentage of the covered distance.~~
* Create requirements.txt file.
* Clean-up the README.md file, add project description, add installation and setup guideline, mention dependencies (point to the requirements.txt file).
* Create development branch and keep the Jupyter Notebook file only there.
* Create the first release in GitHub. Mention what will be included in the next release.
