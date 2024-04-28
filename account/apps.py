from django.apps import AppConfig

# Define a class AccountConfig that inherits from AppConfig
class AccountConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'account'
    # Specify the name of the application
