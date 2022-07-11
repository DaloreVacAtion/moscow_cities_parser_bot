import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def LOGG_SETTINGS(BASE_DIR):
    _dir = str(BASE_DIR)
    if not os.path.isdir(os.path.join(_dir + '/logs')):
        os.mkdir(os.path.join(_dir + '/logs'))
    LOG_DIR = os.path.join(_dir + '/logs')

    return {
        'version': 1,
        'disable_existing_loggers': True,
        'formatters': {
            'console': {
                'format': '%(asctime)s %(levelname)-8s %(name)-12s %(filename)-12s %(funcName)-12s %(lineno)-4s %(message)s'
            },
            'file': {
                'format': '%(asctime)s %(levelname)-8s %(name)-12s %(filename)-12s %(funcName)-12s %(lineno)-4s %(message)s'
            }
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'console',
            },
            'all': {
                'level': 'DEBUG',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': os.path.join(LOG_DIR, 'all.log'),
                'maxBytes': 15728640,  # 1024 * 1024 * 15 = 15mb
                'backupCount': 10,  # 150 mb
                'formatter': 'file',
            },
            'errors': {
                'level': 'ERROR',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': os.path.join(LOG_DIR, 'errors.log'),
                'maxBytes': 15728640,  # 1024 * 1024 * 15 = 15mb
                'backupCount': 10,  # 150 mb
                'formatter': 'file',
            },
            'site': {
                'level': 'DEBUG',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': os.path.join(LOG_DIR, 'site.log'),
                'maxBytes': 15728640,  # 1024 * 1024 * 15 = 15mb
                'backupCount': 10,  # 150 mb
                'formatter': 'file',
            },
            'telebot': {
                'level': 'DEBUG',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': os.path.join(LOG_DIR, 'telebot.log'),
                'maxBytes': 15728640,  # 1024 * 1024 * 15 = 15mb
                'backupCount': 10,  # 150 mb
                'formatter': 'file',
            },
        },
        'loggers': {
            'django': {
                'level': 'INFO',
                'handlers': ['console', 'all', 'errors'],
                'propagate': True,
            },
            'django.db.backends': {
                'handlers': ['console'],
                'level': 'INFO',  # для включения лога бд включить DEBUG
                'propagate': True,
            },
            'telebot': {
                'level': 'DEBUG',
                'handlers': ['console', 'all', 'errors', 'telebot'],
                'propagate': True,
            },
        }
    }
