import os
from .settings import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

ALLOWED_HOSTS = ['*']

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

import dj_database_url
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL')
    )
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Add whitenoise middleware for static files
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

# Static files configuration
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Cloudinary configuration for production
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.environ.get('CLOUDINARY_CLOUD_NAME', 'den3ccjvd'),
    'API_KEY': os.environ.get('CLOUDINARY_API_KEY', '554688635689583'),
    'API_SECRET': os.environ.get('CLOUDINARY_API_SECRET', 'adBQr8y2OHk3L6rqWKmFuQDkFy4'),
    'STATICFILES_MANAGER': 'cloudinary_storage.storage.StaticHashedCloudinaryStorage',
    'STATIC_IMAGES_EXTENSIONS': ['jpg', 'jpe', 'jpeg', 'jpc', 'jp2', 'j2k', 'wdp', 'jxr', 'hdp', 'png', 'gif', 'webp', 'bmp', 'tif', 'tiff', 'ico'],
    'MAGIC_FILE_PATH': 'magic',
    'INVALID_IMAGE_PATH': 'https://res.cloudinary.com/den3ccjvd/image/upload/v1/static/images/invalid_image',
    'DEFAULT_RANGE': 'http_range',
    'IGNORE_FILENAME': False,
    'KEEP_ORIGINAL_NAME': False,
    'STATIC_IMAGES_TRANSFORMATIONS': {
        'jpg': [{'quality': 'auto:good', 'fetch_format': 'auto'}],
        'jpe': [{'quality': 'auto:good', 'fetch_format': 'auto'}],
        'jpeg': [{'quality': 'auto:good', 'fetch_format': 'auto'}],
        'jpc': [{'quality': 'auto:good', 'fetch_format': 'auto'}],
        'jp2': [{'quality': 'auto:good', 'fetch_format': 'auto'}],
        'j2k': [{'quality': 'auto:good', 'fetch_format': 'auto'}],
        'wdp': [{'quality': 'auto:good', 'fetch_format': 'auto'}],
        'jxr': [{'quality': 'auto:good', 'fetch_format': 'auto'}],
        'hdp': [{'quality': 'auto:good', 'fetch_format': 'auto'}],
        'png': [{'quality': 'auto:good', 'fetch_format': 'auto'}],
        'gif': [{'quality': 'auto:good', 'fetch_format': 'auto'}],
        'webp': [{'quality': 'auto:good', 'fetch_format': 'auto'}],
        'bmp': [{'quality': 'auto:good', 'fetch_format': 'auto'}],
        'tif': [{'quality': 'auto:good', 'fetch_format': 'auto'}],
        'tiff': [{'quality': 'auto:good', 'fetch_format': 'auto'}],
        'ico': [{'quality': 'auto:good', 'fetch_format': 'auto'}]
    }
}

# Security settings for production
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
