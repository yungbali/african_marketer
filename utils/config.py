"""Configuration settings for the application."""

# AWS Configuration
AWS_CONFIG = {
    "region_name": "us-east-1",
    "model_id": "anthropic.claude-3-sonnet-20240229-v1:0",
    "max_tokens": 1000,
    "temperature": 0.7
}

# Logging Configuration
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        },
    },
    "handlers": {
        "file": {
            "class": "logging.FileHandler",
            "filename": "app.log",
            "formatter": "standard"
        },
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard"
        }
    },
    "loggers": {
        "": {
            "handlers": ["console", "file"],
            "level": "INFO",
        }
    }
}

# Streamlit Configuration
STREAMLIT_CONFIG = {
    "page_title": "African Music Marketing Assistant",
    "page_icon": "🎵",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}