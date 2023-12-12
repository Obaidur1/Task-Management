from django.urls import path, include
from .views import Handle_Login, Handle_Registration, HandleTask, index, TaskViewSet
from rest_framework.routers import DefaultRouter
from task import views

routers = DefaultRouter()
routers.register(r"task", TaskViewSet, basename="task")
urlpatterns = [
    path("", index, name="home"),
    path("api/register/", Handle_Registration.as_view(), name="api_register"),
    path("api/login/", Handle_Login.as_view(), name="api_login"),
    path("api/handletask/", HandleTask.as_view(), name="handletask"),
    path("api/", include(routers.urls)),
    # template views
    path("login", views.user_login, name="user_login"),
    path("logout", views.user_logout, name="user_logout"),
    path("register", views.user_registration, name="user_register"),
    path("task/<int:id>", views.view_task, name="view_task"),
    path("task/<int:id>/edit", views.edit_task, name="edit_task"),
    path("delete/<int:id>", views.delete_task, name="delete_task"),
    path("add-task", views.add_task, name="add_task"),
    path("change-password", views.change_password, name="change_password"),
]
