from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent


def env_bool(name, default=False):
    value = os.getenv(name, str(default))
    return str(value).strip().lower() in ("1", "true", "yes", "on")


# ================== SEGURANÇA ==================
SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "django-insecure-7ph+q*t=afo72d#2(#x=qrv5&r44af82^$plf8bdcg$ac&!xmx"
)

DEBUG = env_bool("DEBUG", False)

ALLOWED_HOSTS = [
    host.strip()
    for host in os.getenv(
        "ALLOWED_HOSTS",
        ".vercel.app,aprender-django.vercel.app,localhost,127.0.0.1"
    ).split(",")
    if host.strip()
]

CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in os.getenv(
        "CSRF_TRUSTED_ORIGINS",
        "https://*.vercel.app,https://aprender-django.vercel.app"
    ).split(",")
    if origin.strip()
]


# ================== APPS E MIDDLEWARE ==================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # WhiteNoise
    'whitenoise.runserver_nostatic',

    # terceiros
    'rest_framework',
    'drf_spectacular',

    # app local
    'produtos',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# ================== URLS / TEMPLATES ==================
ROOT_URLCONF = 'django_basico.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'django_basico.wsgi.application'


# ================== BANCO ==================
# Mantido SQLite como no seu projeto atual.
# Para produção real, o ideal no Vercel é usar um banco externo/Postgres.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# ================== STATIC FILES ==================
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_DIRS = [
    BASE_DIR / 'templates' / 'static',
]

# Opcional com WhiteNoise
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# ================== MEDIA ==================
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# ================== SEGURANÇA EM PRODUÇÃO ==================
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
SECURE_SSL_REDIRECT = not DEBUG
X_FRAME_OPTIONS = 'DENY'


# ================== INTERNACIONALIZAÇÃO ==================
LANGUAGE_CODE = 'pt-BR'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True


# ================== DEFAULT PK ==================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ================== DRF ==================
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Aprender Django API',
    'DESCRIPTION': 'API para cadastro e consulta de crianças e doadores.',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}