sudo pip install virtualenv
virtualenv env
sudo chmod +x env/bin/activate
source /env/bin/activate

django-admin -> shows list of all django commands

to start an application 
django-admin startproject studybud
-> initializes a folder called stydybud with necessary files and filders inside
-> cd studybud
-> python manage.py runserver
-> sqlite is the default database with django
-> wsgi - web server gateway interface
-> urls.py - all the url routings to our project
    ->  urlpatterns = [
            path('admin/', admin.site.urls),
        ]
        will be a list of all the url patterns
        // urls trigger views
-> settings.py - core configuration of out project

*** creating a new app
python manage.py startapp base
-> models.py - where we configure the database
-> views.py - 

-> add line 'base.apps.BaseConfig' to the INSTALLED_APPS list in studybud/settings.py 
    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',

        'base.apps.BaseConfig',
    ]

-> in studybud/urls.py
    added function called home() and room()
-> cut and paste home() and room() to base/views.py
-> create base/urls.py just to handle all the routes from the base app
-> add "path('', include('base.urls'))," to urlpatterns in studybud/urls.py

-> create a folder templates and files home.html and room.html inside it
-> add  *BASE_DIR / 'templates'* to studybud/TEMPLATES/Dirs list
    to make the app know about the templates directory
-> modify base/views.py/home() by adding the render method
    return render (request, 'home.html')

# template inheritance
we can also inherit templates inside other templates
-> created templates/navbar.html
-> make the nacvar.html file
-> {% include 'navbar.html' %} place this where you want to import navbar
-> created main.html and extended it to room.html and home.html

### learn about django templating engine

-> added rooms [] to base/views.py
-> create a div in home.html to render the rooms[] array

-> create base/templates and then base/templates/base and base/templates/base/home.html
-> copy templates/home.html to base/templates/base/home.html
-> delete templates/home.html 
-> make modifications in home() in base/views.py/home()/render

### dynamic url routing - how to see a specific object on clicking specific links( link the rooms[])
-> added "path('room/<str:pk>/', views.room, name="room")," to base/urls.py/urlpatterns
-> added argument pk to base/views.py/room()
-> added <a href="room/{{room.id}}"> in base/template/base/home.html
-> change the base/views.py/room() function  and base/template/base/room.html accordingly

#### database things
-> python3 manage.py migrate

-> go to base/models.py
-> create class Room() in base/models.py
-> add "from .models import Room" to base/admin.py
-> add "admin.site.register(Room)" to base/admin.py
-> similar for message model

-> changes in base/views.py
    from .models import Room
    home() -> rooms = Room.objects.all()
    room() -> room = Room.objects.get(id=pk)
