import os
from datetime import timedelta

# ---------------------------------------------------------
# Basic Configuration
# ---------------------------------------------------------
SECRET_KEY = b"qyf8hay6c6UN7t9oUKXAtyu+HD8IJIoraAO23GZxVvTnTyAByr8vdrSe"

# Database URI
SQLALCHEMY_DATABASE_URI = 'mysql://root:root@localhost/apachesuperset'  # Use a dedicated user

# Enable Superset's meta database
ENABLE_SUPERSET_META_DB = True

WTF_CSRF_ENABLED = False


# SQLAlchemy connection pool settings
SQLALCHEMY_POOL_SIZE = 10
SQLALCHEMY_POOL_TIMEOUT = 30
SQLALCHEMY_MAX_OVERFLOW = 10
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Default configurations
ROW_LIMIT = 50000
SAMPLES_ROW_LIMIT = 1000
NATIVE_FILTER_DEFAULT_ROW_LIMIT = 1000
FILTER_SELECT_ROW_LIMIT = 10000
SUPERSET_WEBSERVER_TIMEOUT = int(timedelta(minutes=1).total_seconds())

# Debug mode
DEBUG = os.environ.get("FLASK_DEBUG", "0") == "1"
FLASK_USE_RELOAD = True

# SQLAlchemy engine options
SQLALCHEMY_ENGINE_OPTIONS = {
    "pool_pre_ping": True
}

# Custom security manager
CUSTOM_SECURITY_MANAGER = None

# Logging configuration
LOGGING_LEVEL = 'DEBUG'  # Change to INFO in production

