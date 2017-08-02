# movietickets
A cinema booking system made for a school assessment
## Dependencies
Python 3(.6) with PyQt5
## Functions
* User interface provided (tested with Mac only)
* Stores all data with CSV files
* Seat selection
* Movie info including trailers
## Usage
Data is stored in csv files with formats of:
### cinema.csv

ID | Cinema Name | Cinema Description | Phone Number | Address | GMapID
--- | --- | --- | --- | --- | ---

### file.csv

ID | Movie Name | YouTubeID | Rating
--- | --- | --- | ---

### session.csv

CinemaID | MovieID | Date | Time | Seats Taken
--- | --- | --- | --- | ---

### booking.csv

BookingID | SessionID | First Name | Last Name | Phone Number
--- | --- | --- | --- | ---

## License
GNU General Public License v3.0
