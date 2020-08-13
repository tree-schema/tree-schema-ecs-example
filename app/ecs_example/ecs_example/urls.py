from django.urls import path

from . import views

app_name = "ecs_example"


urlpatterns = [
    path("", view=views.get_landing_page, name="landing_page"),
    path("email_action/", view=views.manage_email_action, name="manage_email_action"),
]


