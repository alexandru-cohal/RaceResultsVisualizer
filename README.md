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
  * The column names shall be: "name", "distance", "date", "city", "country", "duration", "pace", "gpxfilename".
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
* The plots displayed by the WebApp shall show the following information:
  * After selecting a category of races from a dropdown list (i.e. 5 & 6 km, 10 km, all races):
    * Plot_1 shall show the evolution of the pace for all the races from the selected category.
  * Plot_2 shall show the number of races for each race distance.
  * Plot_3 shall show the locations of all the races on a map.
    * The starting point shall be used as the location of a race. 
  * After selecting one of the races from a dropdown list:
    * Plot_4 shall show the route of the race on a map.
    * Plot_5 shall show the elevation profile.
    * Plot_6 shall show the pace for each kilometer of the race and the calculated and official average pace values for the whole race.
* The WebApp shall use as input a configuration file ```config.json```.
  * The configuration file shall contain the key ```csv_race_results_filepath```.
    * The value of the key ```csv_race_results_filepath``` shall be the path of the .CSV file containing the race results.
  * The configuration file shall contain the key ```gpx_race_route_filepath```.
    * The value of the key ```gpx_race_route_filepath``` shall be the path of the folder where all the .GPX files containing the logged race information are stored.

## To Do in the following releases:
* Improve time per km plot (set different marker colors for different race lengths, add legend of colors)
  * Solution: Plot firstly the line and then overlap for each type of distance only the markers by using the _add_trace_ function (like it was done in the _plot_route_ function for the start and end points).
* Check the whole code if the best ways to access the rows and cells of the dataframe (i.e. loc, at) are used. Improve if needed.
* Add combined plot route & elevation (with correlation between hovered point -> hover on subplots).
  * Solution: Use _plotly.graph_object_ and the attributes _hoversubplots_ and _hovermode_ (see https://plotly.com/python/hover-text-and-formatting/#hover-on-subplots).
* Add possibility to select race from the map of starting points and have the same effect as the dropdown list selection.
  * Solution: Use plotly.graph_objects and FigureWidget (see https://plotly.com/python/click-events/).
* ~~Change the categories for the time per km plot. Now the 10 km category doesn't include the 12 km race. Also, the categories shouldn't be strict (e.g. the category of 5 & 6 km shouldn't include only 5 km and 6 km races but everything in between).~~
* ~~Now the time per km plot for 10 km category has only one point but the values from the X axis look strange (i.e. the time is also displayed, not only dates / months). Check and fix this.~~
* ~~The time per km plot doesn't have ticks nor grid lines above and below all the points. This would be useful for visually framing all the points.~~
* ~~The location of the starting points map plot is not including all the races. Check and fix the way how the boundaries are calculated.~~
* ~~As the location of the starting points map plot has to be now pretty zoomed out in order to display all the points, add 2 options for this plot: General - the map will be center and zoomed in order for all the points to be visible, Barcelona - the map will be center and zoomed in order for the points of the races from Barcelona (and Badalona) to be visible, as these are pretty clustered together.~~
* The route map plot for the Madrid race doesn't include the whole route. Check and fix the way how the boundaries are calculated.
* The Leiden race doesn't have official values for duration and pace. Now in the .CSV file were added my measured values. Add the possibility to handle the situation when these values are not available. 
* ~~For the number of races plot, the labels from the X axis are not aligned with the plotted columns. Check why and fix this.~~