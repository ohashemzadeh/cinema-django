# cinema-django
Hi. This is cinema project with python and Django. This project contains ticketing and accounts apps. Enjoy.


First install requirements:<br />
pip install -r requirements.txt <br />
Then :
1. py manage.py makemigrations
2. py manage.py migrate
3. py manage.py createsuperuser
4. py manage.py runserver

then add some sample data from django admin panel. 
http://127.0.0.1:8000/admin

Viewing Showtime page needs logging into account: 
http://127.0.0.1:8000/ticketing/showtime/list