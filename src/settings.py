
from pathlib import Path

# from decouple import config
from datetime import timedelta
import os
from dotenv import load_dotenv
from urllib.parse import urlparse
from django.core.exceptions import ImproperlyConfigured


load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")

PRICE_API_KEY = os.getenv("PRICE_API_KEY")
APP_MANAGEMENT_API_KEY = os.getenv("APP_MANAGEMENT_API_KEY")
ALEXANDER_WEBSITE_URL = os.getenv("ALEXANDER_WEBSITE_URL")

# Application definition
INSTALLED_APPS = [
    # Custom apps
    "user_account",
    "codehub",
    "contact",
    
    "django.contrib.admin",
    "axes",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "drf_yasg",
    "drf_spectacular",
    
    # Third-party apps
    "corsheaders",
    "rest_framework_simplejwt",
    "rest_framework",
    "rest_framework.authtoken",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    "allauth.socialaccount.providers.microsoft",
    "dj_rest_auth",
    "dj_rest_auth.registration",
]

AUTH_USER_MODEL = "user_account.CustomUser"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    # Place CorsMiddleware as high as possible, preferably before any middleware
    # that can generate responses, such as CommonMiddleware or any authentication middleware.
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "axes.middleware.AxesMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    # "user_account.middleware.middleware.NeonKeepAliveMiddleware",
    # "user_account.middleware.ping_render.RenderKeepAlive",
]

ROOT_URLCONF = "src.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / 'templates'],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                'django.template.context_processors.debug',
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "src.wsgi.application"


# SQLite Database ------------------------------------------------------------------
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }


# POSTGRESQL DATABASE ------------------------------------------------------------------

DATABASE_URL = os.getenv("DATABASE_URL")  # From .env
parsed = urlparse(DATABASE_URL)

if DATABASE_URL:
    parsed = urlparse(DATABASE_URL)
    # print(f"Parsed URL: {parsed}") #for debugging
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": parsed.path.lstrip("/"),  # Remove the leading slash
            "USER": parsed.username,
            "PASSWORD": parsed.password,
            "HOST": parsed.hostname,
            "PORT": parsed.port or 5432,  # Use 5432 as default if port is None
            "OPTIONS": {
                "sslmode": "require",  # Ensure SSL is required
            },
        }
    }
else:
    # Handle the case where DATABASE_URL is not set.  This is crucial!
    # DATABASES = {
    #     'default': {
    #         'ENGINE': 'django.db.backends.sqlite3',
    #         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    #     }
    # }
    print("DATABASE_URL is not set. Using SQLite instead.")


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / 'media'
# MEDIA_ROOT = os.path.join(BASE_DIR, "media") 

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Social account settings
SOCIALACCOUNT_STORE_TOKENS = True
SOCIALACCOUNT_EMAIL_AUTHENTICATION = True
SOCIALACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "none"
SOCIALACCOUNT_AUTO_SIGNUP = True

# Django AllAuth settings
AUTHENTICATION_BACKENDS = [
    "axes.backends.AxesBackend",
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

# Axes configuration
AXES = {
    # Basic Protection
    "FAILURE_LIMIT": int(os.getenv("AXES_FAILURE_LIMIT", "10")),
    "COOLOFF_TIME": timedelta(hours=int(os.getenv("AXES_COOLOFF_TIME", "1"))),
    # API Response Handling
    "LOCKOUT_CALLABLE": "src.utils.custom_lockout",
    "HTTP_RESPONSE_CODE": 403,
    # Behavior Tuning
    "RESET_ON_SUCCESS": True,
    "NEVER_LOCKOUT_GET": True,
    "LOCKOUT_PARAMETERS": ["ip_address", "username"],
    # Security
    "AXES_HEADERS": ["User-Agent", "X-Forwarded-For"],
    "PROXY_COUNT": 1,
}

SITE_ID = 1

ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_UNIQUE_EMAIL = True

ACCOUNT_EMAIL_VERIFICATION = "none"
# SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_EMAIL_REQUIRED = False
SOCIALACCOUNT_EMAIL_VERIFICATION = "none"
SOCIALACCOUNT_QUERY_EMAIL = True

# Security headers and protections
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"
SECURE_REFERRER_POLICY = "same-origin"

ALLOWED_HOSTS = []

# Production configuration (Render)
if os.environ.get("RENDER"):
    ALLOWED_HOSTS.extend(["alexandercyril.onrender.com", ".onrender.com"])

# Local development
if DEBUG:
    ALLOWED_HOSTS.extend(["localhost", "127.0.0.1", "[::1]"])

# Optional: Keep environment variable override as fallback
env_hosts = os.getenv("ALLOWED_HOSTS")
if env_hosts:
    ALLOWED_HOSTS.extend(host.strip() for host in env_hosts.split(","))

# Ensure no duplicates
ALLOWED_HOSTS = list(set(ALLOWED_HOSTS))

# HTTPS Settings (auto-configure based on environment)
is_development = DEBUG or any(
    host in ["127.0.0.1", "localhost"] for host in ALLOWED_HOSTS
)

if not is_development:
    # Production security settings
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
else:
    # Development settings
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
    SECURE_SSL_REDIRECT = False

# Redirect URL after successful social auth
API_BASE_URL = os.getenv(
    "API_BASE_URL", "alexandercyril.onrender.com"
)  # Default for development
LOGIN_REDIRECT_URL = os.getenv("LOGIN_REDIRECT_URL", "/api/user/profile/")
LOGOUT_REDIRECT_URL = os.getenv("LOGOUT_REDIRECT_URL", "/")

# Dynamic callback URL configuration
if DEBUG:
    # Development settings (localhost)
    SOCIAL_AUTH_GOOGLE_OAUTH2_REDIRECT_URI = (
        "http://localhost:8000/accounts/google/login/callback/"
    )
    API_BASE_URL = "http://localhost:8000"
else:
    # Production settings (Render)
    SOCIAL_AUTH_GOOGLE_OAUTH2_REDIRECT_URI = os.getenv(
        "CALLBACK_URL",
        "http://alexandercyril.onrender.com/accounts/google/login/callback/",
    )
    API_BASE_URL = os.getenv("API_BASE_URL", "https://alexandercyril.onrender.com")



# Core configuration (must come first)
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
API_BASE_URL = (
    "http://localhost:8000" if DEBUG else "https://alexandercyril.onrender.com"
)


def validate_origin(url):
    """Strict origin validation with security checks"""
    parsed = urlparse(url.strip())
    if not (parsed.scheme and parsed.netloc):
        raise ValueError(f"Invalid origin URL: {url}")

    # Security checks
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Invalid scheme in origin: {url}")
    if parsed.path or parsed.query or parsed.fragment:
        raise ValueError(f"Origin should not contain path/query/fragment: {url}")

    return f"{parsed.scheme}://{parsed.netloc}"


def get_cors_origins():
    """Dynamically generates CORS origins based on environment"""
    base_origins = [
        # Local development origins
        "http://localhost:8000",
        "http://localhost:3000",  # Next.js development server
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000",
    ]

    # Add Render production backend URL
    base_origins.append("https://alexandercyril.onrender.com")

    # Add Vercel frontend deployment URL (replace with your actual Vercel URL)
    vercel_frontend_url = os.getenv("VERCEL_FRONTEND_URL")
    if vercel_frontend_url:
        base_origins.append(vercel_frontend_url)

    # Allow all subdomains for Render and Vercel if needed (use with caution in production)
    # This example specifically adds your base Render URL and a Vercel URL.
    # If you need wildcard subdomains, you'd configure CORS_ALLOW_ALL_ORIGINS or a regex.
    # For now, it's safer to list specific production URLs.

    env_origins = os.getenv("EXTRA_CORS_ORIGINS", "").split(",")

    validated_origins = set()
    for origin in base_origins + [eo.strip() for eo in env_origins if eo.strip()]:
        try:
            validated_origins.add(validate_origin(origin))
        except ValueError as e:
            if DEBUG:
                print(f"Warning: {e}")
            continue

    return list(validated_origins)

CORS_ALLOWED_ORIGINS = get_cors_origins()
CORS_ALLOW_ALL_ORIGINS = False 
CORS_ALLOW_CREDENTIALS = True

# CORS Configuration
# When DEBUG is True, CORS_ALLOW_ALL_ORIGINS should be True for easier local development.
# When DEBUG is False (production), CORS_ALLOWED_ORIGINS should be used and explicitly list allowed origins.
CORS_ALLOWED_ORIGINS = get_cors_origins() if not DEBUG else []
CORS_ALLOW_ALL_ORIGINS = DEBUG  # This allows all origins when DEBUG is True.
CORS_ALLOW_CREDENTIALS = True
CORS_EXPOSE_HEADERS = [
    "Content-Type",
    "X-CSRFToken",
    "Authorization",
    "X-Requested-With",
]
CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]
CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]

# Production hardening
if not DEBUG:
    CORS_PREFLIGHT_MAX_AGE = 86400  # 1 day
    # It's better to make CORS_URLS_REGEX more specific if possible,
    # or ensure it matches all your API endpoints.
    # CORS_URLS_REGEX = r'^/api/.*$'
    CORS_URLS_REGEX = r"^(/(api|auth)/.*)$"
    CSRF_TRUSTED_ORIGINS = [
        f"https://{urlparse(o).netloc}"
        for o in CORS_ALLOWED_ORIGINS
        if urlparse(o).scheme == "https"
    ]


# Cookie settings
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_SAMESITE = "Lax"
SESSION_COOKIE_AGE = 86400

# CSRF settings (must come after CORS_ALLOWED_ORIGINS is defined)
CSRF_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_HTTPONLY = False  # Required for React/Next.js to read the cookie
CSRF_COOKIE_SAMESITE = "Lax"
CSRF_HEADER_NAME = "X-CSRFToken"
CSRF_FAILURE_VIEW = "user_account.views.csrf_failure"


# ======================== REST Framework Settings ========================
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ],
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
    "DEFAULT_SCHEMA_CLASS": [
        "drf_spectacular.openapi.AutoSchema",
    ],
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.FormParser",
        "rest_framework.parsers.MultiPartParser",
    ],
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "anon": "100/hour",
        "user": "1000/hour",
    },
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
    "DEFAULT_SCHEMA_CLASS": "rest_framework.schemas.coreapi.AutoSchema",
    "TEST_REQUEST_DEFAULT_FORMAT": "json",
}


# Only enable browsable API in development
if DEBUG:
    REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"].append(
        "rest_framework.renderers.BrowsableAPIRenderer"
    )


# JWT settings
# ======================== JWT Settings ========================
SIMPLE_JWT = {
    # Token Lifetimes
    "ACCESS_TOKEN_LIFETIME": timedelta(
        minutes=int(os.getenv("JWT_ACCESS_TOKEN_LIFETIME_MINUTES", "60"))
    ),
    "REFRESH_TOKEN_LIFETIME": timedelta(
        days=int(os.getenv("JWT_REFRESH_TOKEN_LIFETIME_DAYS", "7"))
    ),
    "SLIDING_TOKEN_LIFETIME": timedelta(
        minutes=int(os.getenv("JWT_SLIDING_TOKEN_LIFETIME_MINUTES", "60"))
    ),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(
        days=int(os.getenv("JWT_SLIDING_TOKEN_REFRESH_LIFETIME_DAYS", "1"))
    ),
    # Behavior Flags
    "ROTATE_REFRESH_TOKENS": os.getenv("JWT_ROTATE_REFRESH_TOKENS", "True").lower()
    in ("true", "1", "t"),
    "BLACKLIST_AFTER_ROTATION": os.getenv(
        "JWT_BLACKLIST_AFTER_ROTATION", "True"
    ).lower()
    in ("true", "1", "t"),
    "UPDATE_LAST_LOGIN": os.getenv("JWT_UPDATE_LAST_LOGIN", "True").lower()
    in ("true", "1", "t"),
    # Algorithm and Signing
    "ALGORITHM": os.getenv("JWT_ALGORITHM", "HS256"),
    "SIGNING_KEY": SECRET_KEY,  # From Django's default SECRET_KEY
    # These typically don't need env configuration
    "VERIFYING_KEY": None,
    "AUDIENCE": None,
    "ISSUER": None,
    "JWK_URL": None,
    "LEEWAY": 0,
    # Header configuration
    "AUTH_HEADER_TYPES": ("Bearer", "JWT"),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    # Claims
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",
    "JTI_CLAIM": "jti",
    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
}


REST_AUTH = {
    "USE_JWT": True,  # Enable JWT for dj-rest-auth
    "JWT_AUTH_COOKIE": "jwt-auth",  # Optional: Use cookies for JWT
    "JWT_AUTH_REFRESH_COOKIE": "jwt-refresh-auth",
}


# Social account providers
SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "APP": {
            "client_id": os.getenv("GOOGLE_CLIENT_ID"),
            "secret": os.getenv("GOOGLE_CLIENT_SECRET"),
            "key": "",
        },
        "SCOPE": [
            "profile",
            "email",
            "https://www.googleapis.com/auth/userinfo.profile",
        ],
        "AUTH_PARAMS": {"access_type": "online", "prompt": "select_account"},
    },
    "microsoft": {
        "APP": {
            "client_id": os.getenv("MICROSOFT_CLIENT_ID"),
            "secret": os.getenv("MICROSOFT_CLIENT_SECRET"),
            "key": "",
        },
        "SCOPE": [
            "openid",
            "profile",
            "email",
        ],
        "AUTH_PARAMS": {
            "access_type": "online",
            "prompt": "select_account",
            "response_type": "code",
        },
        "METHOD": "oauth2",
        "VERIFIED_EMAIL": True,
        "EXCHANGE_TOKEN": True,
        "OAUTH_PKCE_ENABLED": True,
    },
}


SOCIALACCOUNT_ADAPTER = "user_account.adapters.CustomSocialAccountAdapter"
ACCOUNT_ADAPTER = "user_account.adapters.CustomAccountAdapter"

SOCIALACCOUNT_LOGIN_ON_GET = True
ACCOUNT_LOGIN_ON_GET = True
ACCOUNT_LOGOUT_ON_GET = True

# Add these settings
ACCOUNT_DEFAULT_HTTP_PROTOCOL = "http"
SOCIALACCOUNT_AUTO_SIGNUP = True


# SEND EMAIL WITH GOOGLE WHEN USERS SUMBIT CONTACT FORM
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'alexander.s.cyril@gmail.com'
# EMAIL_HOST_PASSWORD = 'xxeywujecwfvyycq'  # The 16-character App Password
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = 'alexander.s.cyril@gmail.com'
ADMIN_EMAIL = 'alexander.s.cyril@gmail.com'  # Or same as above


# Site URL Configuration (add these new settings)
# SITE_DOMAIN = 'https://www.alexandercyril.xyz'  
SITE_DOMAIN = os.getenv("FRONTEND_URL")
SITE_PROTOCOL = 'http'  # Use 'https' in production

# DEBUGGING -------------------------------------------------------------------------
# ======================== Logging Configuration ========================
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "verbose"},
        "file": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": BASE_DIR / "logs" / "django.log",
            "formatter": "verbose",
            "maxBytes": 1024 * 1024 * 5,  # 5 MB
            "backupCount": 5,
        },
        "mail_admins": {
            "level": "ERROR",
            "class": "django.utils.log.AdminEmailHandler",
            "include_html": True,
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console", "file", "mail_admins"],
            "level": "INFO",
            "propagate": True,
        },
        "django.request": {
            "handlers": ["mail_admins", "file"],
            "level": "ERROR",
            "propagate": False,
        },
        "apps": {
            "handlers": ["console", "file"],
            "level": "DEBUG" if DEBUG else "INFO",
            "propagate": False,
        },
    },
    "root": {
        "handlers": ["console", "file"],
        "level": "DEBUG" if DEBUG else "INFO",
    },
}

# Ensure logs directory exists
os.makedirs(BASE_DIR / "logs", exist_ok=True)

# Neon Keep-Alive Settings
NEON_KEEPALIVE_ENABLED = True  # Set to False to disable
NEON_PING_INTERVAL = 200  # 4 minutes (less than Neon's 5-minute timeout)
# NEON_PING_INTERVAL = 10  # 10 seconds for testing


# ======================== Cache Configuration ========================
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "unique-snowflake",
    }
}

# In production, switch to Redis if available
if not DEBUG and os.getenv("REDIS_URL"):
    CACHES["default"] = {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.getenv("REDIS_URL"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "SOCKET_CONNECT_TIMEOUT": 5,
            "SOCKET_TIMEOUT": 5,
            "IGNORE_EXCEPTIONS": True,
        },
    }


# ======================== Sentry Configuration ========================
if not DEBUG and os.getenv("SENTRY_DSN"):
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration

    sentry_sdk.init(
        dsn=os.getenv("SENTRY_DSN"),  # Required Sentry Data Source Name
        integrations=[DjangoIntegration()],
        traces_sample_rate=float(os.getenv("SENTRY_TRACES_SAMPLE_RATE", "0.2")),
        send_default_pii=os.getenv("SENTRY_SEND_DEFAULT_PII", "True").lower()
        in ("true", "1", "t"),
        environment=os.getenv("ENVIRONMENT", "production"),
    )


# ======================== Brevo Email Configuration ========================
BREVO_API_KEY = os.getenv("BREVO_API_KEY")
EMAIL_SENDER_NAME = os.getenv("EMAIL_SENDER_NAME")
EMAIL_SENDER_EMAIL = os.getenv("EMAIL_SENDER_EMAIL")
FRONTEND_URL = os.getenv("FRONTEND_URL")


# ======================== Render Ping ========================
RENDER_HEALTHCHECK_URL = "https://alexandercyril.onrender.com/api/user/health/"
RENDER_KEEPALIVE_ENABLED = True  # Optional disable flag


# ============================= SWAGGER DOCUMENTATION =============================

SPECTACULAR_SETTINGS = {
    "TITLE": "Social DM API",
    "DESCRIPTION": "API for Alexander Cyril Portfolio",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    # 👇 Swagger UI Settings (Add Bearer Token Input)
    "SWAGGER_UI_SETTINGS": {
        "deepLinking": True,
        "persistAuthorization": True,  # Saves token even after refresh
        "displayOperationId": True,
        "filter": True,
        "docExpansion": "none",  # Collapses all docs by default
        "defaultModelsExpandDepth": -1,  # Hides schemas by default
        "operationsSorter": "method",
        "tagsSorter": "alpha",
        # 👇 This enables the "Authorize" button for Bearer Token
        "securityDefinitions": {
            "Bearer": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header",
                "description": "Type in the **Value** field: `Bearer <your_token>`",
            }
        },
    },
    # 👇 Security Scheme (Required for OpenAPI 3.0)
    "COMPONENT_SECURITY_SCHEMES": {
        "Bearer": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    },
    # 👇 Apply security globally (if all endpoints require auth)
    "SECURITY": [{"Bearer": []}],
    # Rest of your settings...
    "SCHEMA_PATH_PREFIX": r"/api/",
    "SERVERS": [{"url": "http://localhost:8000/", "description": "Dev Server"}],
}


# -------------------------------
# Warning Suppression Configuration
# -------------------------------

import warnings

# Suppress dj-rest-auth deprecation warnings
warnings.filterwarnings(
    "ignore",
    message="app_settings.USERNAME_REQUIRED is deprecated",
    category=UserWarning,
    module="dj_rest_auth.registration.serializers",
)

warnings.filterwarnings(
    "ignore",
    message="app_settings.EMAIL_REQUIRED is deprecated",
    category=UserWarning,
    module="dj_rest_auth.registration.serializers",
)

# Suppress django-allauth deprecation warnings
warnings.filterwarnings(
    "ignore",
    message="settings.ACCOUNT_AUTHENTICATION_METHOD is deprecated",
    category=UserWarning,
)

warnings.filterwarnings(
    "ignore",
    message="settings.ACCOUNT_EMAIL_REQUIRED is deprecated",
    category=UserWarning,
)

warnings.filterwarnings(
    "ignore",
    message="settings.ACCOUNT_USERNAME_REQUIRED is deprecated",
    category=UserWarning,
)
