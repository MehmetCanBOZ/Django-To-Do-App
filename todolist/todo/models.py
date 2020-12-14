from django.contrib.auth.models import AbstractUser
from django.db import models


COMPLETE = 'C'
NONCOMPLETE = 'NC'

Item_CHOICES = [
        (COMPLETE, 'Complete'),
        (NONCOMPLETE, 'NonComplete'),
    ]
class User(AbstractUser):
    pass

class Item(models.Model):
    name_item = models.CharField(max_length=1024)
    desciption=models.CharField(max_length=2048)
    create_date=models.DateTimeField(auto_now=True)
    deadline=models.DateTimeField(auto_now=False)
    status=models.CharField(max_length=2,choices=Item_CHOICES,default=NONCOMPLETE)

    def __str__(self):
        return f"{self.id} : {self.name_item} about {self.desciption} created {self.create_date} and deadline {self.deadline}  and status {self.status}"

class Dolist(models.Model):
    user_todo=models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_todos")
    name_list=models.CharField(max_length=1024)
    item=models.ManyToManyField(Item, blank=True, related_name="item_list")

    def __str__(self):
        return f"{self.name_list} created by {self.user_todo} "