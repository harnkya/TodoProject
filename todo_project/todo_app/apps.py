# uygulamayla alakalı python dosyası, settingse eklenecek

from django.apps import AppConfig


class TodoAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "todo_app"

