import os
import django_heroku

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'd5j18hj8boj3bg',
        'USER': 'xfcyrotabvetaq',
        'PASSWORD': 'e186ab96384accbbfc53be365f0c893350cc0c2266f0ae790362b48304f290bc',
        'HOST': 'ec2-54-147-93-73.compute-1.amazonaws.com',
        'PORT': '5432',
    },
}

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'
STATIC_DIR = os.path.join(BASE_DIR, 'static')
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
# STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'), ]

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# django_heroku.settings(locals())
ALLOWED_HOSTS = ['*']
