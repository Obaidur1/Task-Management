from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
PRIORITY = (("low", "Low"), ("medium", "Medium"), ("high", "High"))

User = get_user_model()


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateField()
    priority = models.CharField(max_length=30, choices=PRIORITY)
    mark_as_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title + " User_id->" + str(self.user.id)


class Image(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="uploads/")

    def __str__(self):
        return self.task.title + " task_id->" + str(self.task.id)
