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

The plots shall show the following information:
* Plot_1 shall show the evolution of the average time per km for all the races.
* Plot_2 shall show the number of races for each distance.
* Plot_3 shall show the locations of all the races on a map.
* Plot_4 shall show the routes of all the races on a map.
* After selecting one of the races from a dropdown list:
  * Plot_5 shall show the route of the race on a map.
  * Plot_6 shall show the elevation profile. 
