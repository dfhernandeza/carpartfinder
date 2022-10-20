# CAR PART FINDER
#### Video Demo:  https://youtu.be/I8nQIyukypw
#### Description:
The project is a web application that makes it easy to find car spare parts. It is very helpful for both buyers and especially sellers who do not have online sales systems.
I have noticed a need for a part finder because of the sheer amount of supply out there, and I hope to help people save a great deal of time.

#### Technologies used:

- Pyhton 3, Flask
- Javascript, JQuery, JQueryUi
- CSS
- HTML
- sqlite3
- Microsoft Azure

#### Manual

The application has two types of roles, the master user has permissions to modify the car database to carry out its maintenance. Any new registered customer gets the user role which allows him/her to use the seller or buyer mode.
Seller mode: For car parts dealers, allows them to publish their products specifying compatibility (make, model and year), price, upload pictures, describe and add features.
Buyer mode: For customers offers a search engine which allows them to filter the results by make, model and year according to their needs. Once found the perfect result, the user can get instructions to get to the store being redirected to google maps, get the phone number and email.

Every route is accessible via links in the navigation bar.

#### Registration (necessary for publication only)

It's necessary to be registered to publish items and in order to be locatable via email, phone or address.
The user must provide First Name, Last Name, Address, Phone Number, Email and Password (all fields are required). 

#### Change Password

The user must provide his/hers current password and provide the new one (all fields are required).

#### Account 

Allows the user to update his/hers account information. Click on the right angle will show the update form for every section. Once finished the editing, click the update button.

#### Manage Cars (only visible for master user)

- NEW CAR MAKE FORM: At the upper section is the new make form, enter a car make that is not in the lower list (the system will validate for duplicates) and tap/click on Submit.

Car Makes list (bottom section):

- Tapping/clicking the red garbage can button will display a confirmation modal view to delete the chosen make.
- Tapping/clicking the green right angle button will display a new section.

- UPDATE CAR MAKE FORM: At the upper section is the update make form, edit the content of the text box and tap/click Update.
- NEW CAR MODEL FORM: At the upper section is the new car model form, enter a car model that is not in the lower list (the system will validate for duplicates) and tap/click on Submit.

Car Models list (bottom section):

- Tapping/clicking the red garbage can button will display a confirmation modal view to delete the chosen model.
- Tapping/clicking the green right angle button will display a new section.

Model Years list (bottom section):

- UPDATE MODEL FORM: At the upper section is the update model form, edit the content of the text box and tap/click Update.
- NEW YEAR FORM: At the upper section is the new year form, select a year from the dropdown list that is not in the lower list (the system will validate for duplicates) and 
tap/click on Submit.

Model Years list (bottom section):

- Tapping/clicking the red garbage can button will display a confirmation modal view to delete the chosen model.

#### Manage Users (only visible for master user)

Search form: At the upper section is the search form, enter an email and the user information will be displayed at the lower section. Tapping/clicking the green right angle will show the update form for every section. Once finished the editing, click the update button.

#### Offer 

- The user must provide a name, price and description for his/hers publication (very field is required).
- Pick as many pictures as he/she wants (image type files only).
- Add as many compatibilities as needed using the dropdown list provided (every field is required).
- Add as many features as needed, entering Name, Value and Description (every field is required).
- Once finished, click/tap Submit.

#### My Offers

Displays a list with all the items posted by the user.

- Tapping/clicking the red garbage can button will display a confirmation modal view to delete the chosen item.
- Tapping/clicking the blue pencil button will display edit part page.

#### Edit Part

Works exactly de same as the offer page. The user must edit the fields, delete or add new pictures, delete or add new compatibilities, delete or add new features and finally submit the form.

#### Find

This page displays a search form, the user must enter the key words and pick all or none of the filters from the three dropdown lists availables (make, model, year), finally press enter and a results page will be rendered.

#### Search

Displays a list with all the results that meet the specified query.
- Click on the name of the item will display a page containing all the details for the chosen part.
- Click on the Contact Seller will display a page containing all the details for the seller, allowing the user to get instructions on Google Maps or make a phone call.

### Files

Controllers 
- carsmanager.py: Contains every route that handles the cars manager.
- loginmanager.py: Contains every route that handles login, logout, register, email validation and password change.
- mainmanager.py: Contains every route that handles the search engine.
- partsmanager.py: Contains every route that handles the publication of parts.
- usermanager.py: Contains every route that handles the users management.

Functions
- helpers.py: Contains helper functions.
- blobsaccess.py: Contains functions to access the Azure Blob Storage Service.


#### Database

Stores all the information necessary for the operation of the application. 
 
Tables

- car_makes: id INTEGER PRIMARY KEY, make TEXT.
- car_models: id INTEGER PRIMARY KEY, car_model TEXT, car_make_id INTEGER FOREIGN KEY (car_makes.id).
- features: id INTEGER PRIMARY KEY, name TEXT, value TEXT, description TEXT, idpart INTEGER FOREIGN KEY (parts.id).
- model_year: id INTEGER PRIMARY KEY, id_year INTEGER FOREIGN KEY (years.id), id_model INTEGER FOREIGN KEY (car_models.id).
- part_compatibility: id INTEGER PRIMARY KEY, id_car_make INTEGER FORIGN KEY (car_makes.id), id_car_model INTEGER FOREIGN KEY (car_models.id), 
  id_year INTEGER FOREIGN KEY (years.id), id_part INTEGER FOREIGN KEY (parts.id).
- part_pictures: id INTEGER PRIMARY KEY, idpicture INTEGER FOREIGN KEY (pictures.id), idpart INTEGER FOREIGN KEY (parts.id).
- parts: id INTEGER PRIMARY KEY, part_name TEXT, id_user INTEGER FOREIGN KEY (users.id), price NUMERIC, description TEXT, date TEXT, state INTEGER.
- pictures: id INTEGER PRIMARY KEY, url TEXT, date TEXT, name TEXT.
- users: id INTEGER PRIMARY KEY, hash TEXT, email TEXT, rol TEXT, first_name TEXT, last_name TEXT, phone_number TEXT, address TEXT.
- years: id INTEGER PRIMARY KEY, year INTEGER.






