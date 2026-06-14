# RaceResultsVisualizer

## Project Description
* The purpose of this project is to develop a WebApp in Python for visualizing in different ways the data related to the running races in which I participated.

## How to Use
* The deployed WebApp is available [here](https://alexandru-cohal-raceresultsvisualizer-main-duilkw.streamlit.app/).
* For running the WebApp locally:
  * Clone the repository.
  * Install the dependencies (```pip install -r requirements.txt```).
  * If needed, adjust the race results values stored in the .CSV file (currently the project is using the ```race_results.csv``` file).
  * If needed, adjust the values from the configuration file ```config.json```.
  * Start the Streamlit WebApp (```streamlit run .\main.py```).
 
## Dependencies
* The Python version used for development was 3.13.
* All the used libraries and their versions are listed in the [requirements.txt](https://github.com/alexandru-cohal/RaceResultsVisualizer/blob/master/requirements.txt) file.

## Requirements
* The WebApp shall use as input a .CSV file which contains the results of all the races to be included in the app.
  * The separator of the .CSV file shall be the comma symbol.
  * The column names shall be: "name", "distance", "date", "city", "country", "duration", "pace", "gpxfilename", "validroutepoints".
    * The column "name" shall contain the name of the race.
      * The race name shall be introduced as a string delimited by double quotes.
      * Note: This way, the name can contain comma symbols without affecting the structure of the .csv file.
    * The column "distance" shall contain the official distance of the race.
      * The race distance value shall be introduced as a floating-point number.
      * The fractional part of the race distance value shall be separated with the dot symbol. 
    * The column "date" shall contain the date of the race.
      * The race date value shall be introduced in the format ```YYYY-MM-DD```, where Y represents a digit of the year value, M represents a digit of the month value, D represents a digit of the day value.
    * The column "city" shall contain the name of the city where the race took place.
      * The race city name shall be introduced as a string delimited by double quotes.
    * The column "country" shall contain country where the race took place.
      * The race country name shall be introduced as a string delimited by double quotes.
    * The column "duration" shall contain the official duration needed to finish the race (i.e. the duration between the initial and final moments where the barrier containing the sensors for reading the chips for identifying the participants are crossed).
      * The race duration value shall be introduced in the format ```H:MM:SS```, where H represents a digit of the hour value, M represents a digit of the minute value, S represents a digit of the second value.
    * The column "pace" shall contain the official pace of the race (i.e. average time needed to cover one kilometer).
      * The race pace shall be introduced in the format ```HH:MM:SS```, where H represents a digit of the hour value, M represents a digit of the minute value, S represents a digit of the second value.
    * The column "gpxfilename" shall contain the name of the file containing the logged data during the race (i.e. location, elevation, timestamp).
      * The name of the file shall be introduced as a string delimited by double quotes and shall include the ".gpx" extension.
    * The column "validroutepoints" shall contain the information whether the registered route points from the GPX file are valid and can be used for processing and plotting or not.
      * The value shall be a boolean value as a string: "true" or "false".
* The plots displayed by the WebApp shall show the following information:
  * After selecting a category of races from a dropdown list (i.e. 5 & 6 km, 10 km, all races):
    * Plot_1 shall show the evolution of the pace for all the races from the selected category.
  * Plot_2 shall show the number of races for each race distance and the total number of races.
  * After selecting an area from a dropdown list (i.e. general or Barcelona):
    * Plot_3 shall show the locations of all the races on a map.
      * The starting point shall be used as the location of a race. 
  * After selecting one of the races from a dropdown list:
    * Plot_4 shall show the route of the race on a map.
      * The starting and ending points shall be clearly marked.
    * Plot_5 shall show the elevation profile.
    * Plot_6 shall show the pace for each kilometer of the race and the calculated and official average pace values for the whole race.
* The WebApp shall use as input a configuration file ```config.json```.
  * The configuration file shall contain the key ```csv_race_results_filepath```.
    * The value of the key ```csv_race_results_filepath``` shall be the path of the .CSV file containing the race results.
  * The configuration file shall contain the key ```gpx_race_route_filepath```.
    * The value of the key ```gpx_race_route_filepath``` shall be the path of the folder where all the .GPX files containing the logged race information are stored.

## To Do in the following releases:
| Priority | Topic                                                                                                                                                                                                                                                                                                                |
|----------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 1        | Add race length category of 20-26 km.                                                                                                                                                                                                                                                                                |
| 1        | The route points plot of 20km de Bruxelles race is too much zoomed in. Check the calculations of the zooming factor.                                                                                                                                                                                                 |
| 1        | The location of the starting points plot for Barcelona area doesn't include the point from El Prat de Llobregat for the Estrella Damm race. Check the calculations of the zooming factor.                                                                                                                            |
| 1        | The bins of the Number of Races w.r.t. Distance plot are now for distance intervals, not for specific lengths (it broke after adding the Checkpoints race). Check how the bins are calculated.                                                                                                                       |
| 1        | When selecting the second race from Girona, it shows the plot for the route, elevation and pace of the first race. The reason is that both races have the same name in the .CSV file. There should be a different part in the name, like it is for the Badalona race.                                                |
| 2        | The Leiden race doesn't have official values for duration and pace. Now in the .CSV file were added my measured values. Add the possibility to handle the situation when these values are not available.                                                                                                             |
| 2        | The Checkpoint and the 20km de Bruxelles races doesn't have official value for pace. Now in the .CSV file was added my calculated value. Add the possibility to handle the situation when this value is not available.                                                                                               |
| 2        | Add dropdown list for years (i.e. 2025, 2026, General).                                                                                                                                                                                                                                                              |
| 3        | Check if special characters can be used in the names of the races in the .CSV file and then to be correctly shown in the app.                                                                                                                                                                                        |
| 3        | Check if the race_data folder should have subfolders for years.                                                                                                                                                                                                                                                      |
| 3        | Improve time per km plot (set different marker colors for different race lengths, add legend of colors). Solution: Plot firstly the line and then overlap for each type of distance only the markers by using the _add_trace_ function (like it was done in the _plot_route_ function for the start and end points). |
| 3        | Add combined plot route & elevation (with correlation between hovered point -> hover on subplots). Solution: Use _plotly.graph_object_ and the attributes _hoversubplots_ and _hovermode_ (see https://plotly.com/python/hover-text-and-formatting/#hover-on-subplots).                                              |
| 3        | Add possibility to select race from the map of starting points and have the same effect as the dropdown list selection. Solution: Use plotly.graph_objects and FigureWidget (see https://plotly.com/python/click-events/).                                                                                           |
| 4        | Add separate functions in a separate .py file for filtering the data (depending on the choices from the dropdown menus).                                                                                                                                                                                             |
| 4        | Check the whole code if the best ways to access the rows and cells of the dataframe (i.e. loc, at) are used. Improve if needed.                                                                                                                                                                                      |
| 5        | For each race, add in the .CSV file the possibility to add a note (for mentioning some ideas relevant for that race, for example the number of checkpoints for the Checkpoints race) which will also be displayed.                                                                                                   |
| 5        | For each race, scan the dorsal, add them to the repository, add a new column to the .CSV file and display this image.                                                                                                                                                                                                |
| 5        | Check the possibility of using a database instead of the .CSV file for simplicity and for adding race data without creating a manual commit.                                                                                                                                                                         |