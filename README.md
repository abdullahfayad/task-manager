
# Task Manager (should be enhanced on error handling level at least by using try except)

Steps to run the project using Docker:

* run `docker-compose build`
* run `docker-compose up`
* docker-compose exec web flask db init
* docker-compose exec web flask db migrate -m "Initial migration"
* docker-compose exec web flask db upgrade  

go to http://localhost:5000 and register or login into the app
