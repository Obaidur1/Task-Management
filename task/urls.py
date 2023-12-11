from django.urls import path
from .views import Handle_Login, Handle_Registration, HandleTask, index

urlpatterns = [
    path("", index, name="home"),
    path("register/", Handle_Registration.as_view(), name="register"),
    path("login/", Handle_Login.as_view(), name="login"),
    path("handletask/", HandleTask.as_view(), name="handletask"),
]
