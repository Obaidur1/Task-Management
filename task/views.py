from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import render
from .models import Image, Task
from .serializers import TaskSerializer


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

    def get(self, request):
        tasks = Task.objects.prefetch_related("images").filter(user=request.user)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

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
