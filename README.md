# Galleria

<hr>

# Author
[Kelvin-Wepo](https://github.com/Kelvin-Wepo/Galleria)
<hr>

[Live link](https://wepogallery.herokuapp.com/)

## Description
This is a python django application for a personal gallery web app to display photos for others to see.


## User Stories
As a user of the application one should be able to:

1. View different photos that interest me.
1. Click on a single photo to expand it and also view the details of the photo. The photo details must appear on a modal within the same route as the main page.
1. Search for different categories of photos. (ie. Nature, Food)
1. Copy a link to the photo to share with friends.
1. View photos based on the location they were taken.

## Behaviour Driven Development
1. On Loading the homepage - view all pictures from the most recent first.
1. On clicking on a photo, a modal with complete photo details appears i.e. name, description, location, category, time taken and larger image.
1. Search functionality available to search different categories.
1. See photos from a particular location.
1. Navigate to the admin dashboard

### Cloning
* Run $ git clone https://github.com/Kelvin-Wepo/Galleria on your terminal

### Running the Application
After cloning, in the terminal: 
* $ cd to the project directory
* $ python3 -m venv virtual - to create a virtual environment
* $ source virtual/bin/activate - to activate virtual environment
* $ pip install django==4.0.2
* $ pip install psycopg2 to connect to postgres
* $ Install pillow, and other django dependencies
* $ python manage.py test - to run test
* $ Open the application on your browser 127.0.0.1:5000 to view by running 'python manage.py runserver'

### Technologies used
* Python3.8
* Django==4.0.2
* Bootstrap v5
* postgresql
* Heroku

### Contacts
You can reach me through:
* Email: kelvin.wepo@student.moringaschool.com or
* Phone: +254799489045

## License
*MIT License*:
Copyright (c) 2022 *Kelvin wepo*