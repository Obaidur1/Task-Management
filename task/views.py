from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.authtoken.models import Token

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .models import Image, Task
from .serializers import TaskSerializer
from django.shortcuts import get_object_or_404

# imports for django template views
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import TaskEditForm

# API Views.


class Handle_Registration(APIView):
    def post(self, request):
        data = request.data
        username = data.get("username")
        password = data.get("password")
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        try:
            user = User.objects.create_user(username=username, password=password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            return Response("User is created")
        except:
            return Response("Something went wrong")

        return Response("User Created", status=201)


class Handle_Login(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key})
        else:
            return Response("Wrong credentials")


class HandleTask(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        print(user)
        title = request.data.get("title")
        description = request.data.get("description")
        due_date = request.data.get("due_date")
        priority = request.data.get("priority")
        task = Task.objects.create(
            user=user,
            title=title,
            description=description,
            due_date=due_date,
            priority=priority,
        )
        images = request.FILES.getlist("images")
        BulkImage = [Image(task=task, image=image) for image in images]
        if BulkImage:
            Image.objects.bulk_create(BulkImage)
        return Response("received", status=201)


class TaskViewSet(viewsets.ViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request):
        tasks = Task.objects.prefetch_related("images").filter(user=request.user)
        serializer = TaskSerializer(tasks, many=True, context={"request": request})
        return Response(serializer.data)

    def retrieve(self, request, pk):
        task = Task.objects.prefetch_related("images").get(pk=pk)
        serializer = TaskSerializer(task, context={"request": request})
        return Response(serializer.data)

    def update(self, request, pk):
        task = Task.objects.prefetch_related("images").get(pk=pk)
        print(request.data)
        if task:
            task.title = request.data.get("title")
            task.description = request.data.get("description")
            task.due_date = request.data.get("due_date")
            task.priority = request.data.get("priority")
            task.mark_as_completed = request.data.get("mark_as_completed")
            task.save()
            return Response(TaskSerializer(task, context={"request": request}).data)
        return Response("Task not found!", status=404)

    def destroy(self, request, pk):
        task = Task.objects.prefetch_related("images").get(pk=pk)
        if task:
            task.delete()
            return Response("Task deleted successfully")
        else:
            return Response("Task Not found!", status=404)


# Views for Django Templates


@login_required
def index(request):
    params = request.GET.get("search")
    if params:
        tasks = Task.objects.prefetch_related("images").filter(
            user=request.user, title__contains=params
        )
    else:
        tasks = Task.objects.prefetch_related("images").filter(user=request.user)
    return render(request, "all_task.html", {"tasks": tasks})


def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            return redirect("user_login")
    return render(request, "login.html")


@login_required(login_url="user_login")
def user_logout(request):
    if request.method == "POST":
        logout(request)
        return redirect("user_login")


def user_registration(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        user = User.objects.create_user(username=username, password=password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        return redirect("user_login")
    return render(request, "registration.html")


@login_required(login_url="login")
def view_task(request, id):
    task = Task.objects.prefetch_related("images").get(id=id)
    # images = task.images.all()
    return render(request, "view_task.html", {"task": task})


@login_required(login_url="login")
def edit_task(request, id):
    task = Task.objects.get(id=id)
    if request.method == "POST":
        form = TaskEditForm(data=request.POST, instance=task)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
        return redirect("view_task", id=id)

    form = TaskEditForm(instance=task)
    return render(request, "task_edit.html", {"form": form})


@login_required(login_url="login")
def delete_task(request, id):
    task = Task.objects.prefetch_related("images").get(id=id)
    task.delete()
    return redirect("home")


def add_task(request):
    if request.method == "POST":
        images = request.FILES.getlist("images")
        user = request.user
        title = request.POST.get("title")
        description = request.POST.get("description")
        due_date = request.POST.get("due_date")
        priority = request.POST.get("priority")
        task = Task.objects.create(
            user=user,
            title=title,
            description=description,
            due_date=due_date,
            priority=priority,
        )
        bulk_images = [Image(task=task, image=image) for image in images]
        Image.objects.bulk_create(bulk_images)
        return redirect("view_task", id=task.id)
    return render(request, "add_task.html")
