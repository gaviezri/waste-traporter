# Tra(cker & Re)porter
a raspberry pi project.
The need is to track office amount of different waste types.
In the office, when disposing trash, it will be first weight on a scale.
To the scale a raspberry pi is connected. 
The pi has a touch screen which will allow the user to specify trash type.
The program stores the data on sqlite server.

Once a month a report is generated and uploaded to sharepoint.
every data the db is backed up via dump to sharepoint.
