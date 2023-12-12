from django.urls import path, include
from .views import Handle_Login, Handle_Registration, HandleTask, index, TaskViewSet
from rest_framework.routers import DefaultRouter

routers = DefaultRouter()
routers.register(r"task", TaskViewSet, basename="task")
urlpatterns = [
    path("", index, name="home"),
    path("register/", Handle_Registration.as_view(), name="register"),
    path("login/", Handle_Login.as_view(), name="login"),
    path("handletask/", HandleTask.as_view(), name="handletask"),
    path("", include(routers.urls)),
]
