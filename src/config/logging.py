from os import path

from config.settings import BASE_DIR

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "[%(asctime)s] %(levelname)7s %(module)20s:%(lineno)4d - %(message)s",
            "datefmt": "%d-%m-%Y %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        "file": {
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": path.join(BASE_DIR, "app.log"),
            "formatter": "verbose",
            "maxBytes": 1048576,
            "backupCount": 3,
        },
    },
    "root": {
        "level": "INFO",
        "handlers": ["console", "file"],
    },
}
