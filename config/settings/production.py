from .base import *


# Secret Settings

DEBUG = False

ALLOWED_HOSTS = get_secret("ALLOWED_HOSTS")


# Logging

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'handlers': {
        'debug': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(PROJECT_DIR, 'logs/debug.log'),
        },
        'info': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(PROJECT_DIR, 'logs/info.log'),
        },
        'warning': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': os.path.join(PROJECT_DIR, 'logs/warning.log'),
        },
        'error': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': os.path.join(PROJECT_DIR, 'logs/error.log'),
        },
        'critical': {
            'level': 'CRITICAL',
            'class': 'logging.FileHandler',
            'filename': os.path.join(PROJECT_DIR, 'logs/critical.log'),
        },
    },
    'loggers': {
        'django': {
            'handlers': ['debug', 'info', 'warning', 'error', 'critical'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'postman': {
            'handlers': ['info'],
            'level': 'INFO',
            'propagate': False
        }
    }
}