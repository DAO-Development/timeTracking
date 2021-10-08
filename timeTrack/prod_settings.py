import django_heroku

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'work24',
        'USER': 'r414216',
        'PASSWORD': 'Koznix-jiwbo5-manjis',
        'HOST': 'localhost',
        'PORT': '5432',
    },
}

django_heroku.settings(locals())
