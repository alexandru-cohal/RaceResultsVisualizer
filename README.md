# RaceResultsVisualizer

## [Draft] Requirements
The race_results.csv file shall contain the results of all the races to be included in the app.
* The separator shall be the comma symbol.
* The name shall be a string delimited by double quotes.
  * Note: This way, the name can contain comma symbols without affecting the structure of the .csv file.
* The distance shall be a number which can contain a fractional part.
  * The fractional part shall be separated with a dot symbol.
* The date shall be in the format YYYY-MM-DD, where Y represents a digit of the year, M represents a digit of the month, D represents a digit od  the day.
* The city shall be a string delimited by double quotes.
* The country shall be a string delimited by double quotes.
* The duration shall be in the format H:MM:SS, where H represents a digit of the hour, M represents a digit of the minute, S represents a digit of the second.
* The latitude and longitude shall be floating point values.
* The name of the associated .GPX file shall be a string delimited by double quotes and shall include the ".gpx" extension.

The plots shall show the following information:
* Plot_1 shall show the evolution of the average time per km for all the races.
* Plot_2 shall show the number of races for each distance.
* Plot_3 shall show the locations of all the races on a map.
* Plot_4 shall show the routes of all the races on a map.
* After selecting one of the races from a dropdown list:
  * Plot_5 shall show the route of the race on a map.
  * Plot_6 shall show the elevation profile.

## To Do:
* Improve time per km plot (set different marker colors for different race lengths, add legend of colors).
* Remove the columns with the starting point location (i.e. "lat" and "lon") from the .CSV file as the same information can be obtained now from the first entry of the .GPX file. Adapt the code.
* Rethink the get_lan_lon_elev function and its usage (it is called 2 times, once for latitude and longitude and second time only for elevation).
* Rethink parse_gpx_file function (are 3 lists the best way to keep and return the latitude, longitude and elevation data?).
* Create a settings.json file and move the GPX_FILEPATH variable in it. Add also the .CSV file path in it. Adapt the code.
* ~~Improve the elevation plot~~ (~~continuous line (not only discrete points)~~, ~~axis labels~~, ~~hover display data~~).
* Improve the route plot (~~continuous line (not only discrete points)~~, different markers for start and end points, ~~hover display data~~, ~~zoom~~, ~~alignment~~).
* Calculate distance and time since start based on the data from the .GPX file and show it on the route and elevation plots
* Based on the previously calculated distance and time since start, add plot for the speed
* Add combined plot route & elevation (with correlation between hovered point -> hover on subplots).
* Add possibility to select race from the map of starting points and have the same effect as the dropdown list selection.
