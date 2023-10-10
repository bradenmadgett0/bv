To run this project:

Install Python and Django

Open project root

Run python manage.py runserver

Project should come populated with a test user and some orders.


If you delete the DB and migrations and start fresh, you can get back to a testable state by doing the following:

  Open project root
  
  Run python manage.py migrate
  
  Run python manage.py makemigrations bluevoice
  
  Run python manage.py migrate bluevoice
  
  Run python manage.py createsuperuser (username and password should both be test, and email should be test@test.com)
  
  Run python manage.py loaddata menuitems
  
  Run python manage.py runserver
