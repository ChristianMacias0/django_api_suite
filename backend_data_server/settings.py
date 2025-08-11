"""
Django settings for backend_data_server project.
"""

from pathlib import Path
import os  # <--- IMPORTANTE: Añadir este import para las variables de entorno
import firebase_admin
from firebase_admin import credentials

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# --- CONFIGURACIÓN DE SEGURIDAD PARA PRODUCCIÓN ---

# 1. CARGAR LA SECRET_KEY DESDE UNA VARIABLE DE ENTORNO
# En PythonAnywhere, la configurarás en la pestaña "Web".
# El segundo argumento es un valor por defecto para que funcione en tu PC si la variable no existe.
SECRET_KEY = os.environ.get(
    'DJANGO_SECRET_KEY',
    'django-insecure-d5l8_(0y%4t2+kfly$z)ylbrsq$jv3cb%uys4ae9a^awm*qyg*'
)

# 2. DEBUG DEBE SER FALSE EN PRODUCCIÓN
DEBUG = False # <--- CAMBIO CRÍTICO

# 3. ALLOWED_HOSTS YA ESTÁ BIEN PARA PYTHONANYWHERE
ALLOWED_HOSTS = ['cmaciasm.pythonanywhere.com']


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "firebase_admin",
    "rest_framework",
    "homepage",
    'demo_rest_api', # No es necesario el .apps.DemoRestApiConfig, así es más simple
    'landing_api',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend_data_server.urls'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
WSGI_APPLICATION = 'backend_data_server.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation... (sin cambios)
AUTH_PASSWORD_VALIDATORS = [...]

# Internationalization... (sin cambios)
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# --- CONFIGURACIÓN DE ARCHIVOS ESTÁTICOS PARA PRODUCCIÓN ---

STATIC_URL = 'static/'
# 4. Usar una ruta absoluta para STATIC_ROOT
STATIC_ROOT = BASE_DIR / 'staticfiles' # <--- CAMBIO IMPORTANTE


# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --- CONFIGURACIÓN DE FIREBASE DE FORMA ROBUSTA ---

# 5. Usar una ruta absoluta para las credenciales
CERT_PATH = BASE_DIR / 'secrets' / 'landing-key.json'

if not os.path.exists(CERT_PATH):
    raise FileNotFoundError(f"No se encontró el archivo de credenciales de Firebase en: {CERT_PATH}")

FIREBASE_CREDENTIALS = credentials.Certificate(CERT_PATH)
firebase_admin.initialize_app(FIREBASE_CREDENTIALS, {
   'databaseURL': 'https://prueba-18913-default-rtdb.firebaseio.com/'
})