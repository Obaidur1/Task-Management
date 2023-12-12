from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.authtoken.models import Token

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import render
from .models import Image, Task
from .serializers import TaskSerializer
from django.shortcuts import get_object_or_404


# Create your views here.
def index(request):
    return render(request, "index.html")


class Handle_Registration(APIView):
    def post(self, request):
        data = request.data
        username = data.get("username")
        password = data.get("password")
        # email = data.get("email")
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
