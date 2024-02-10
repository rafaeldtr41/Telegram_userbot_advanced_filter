import os
import django




def load_django_config():

    #Configuring Django ORM
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Django_ORM.settings')
    django.setup()

