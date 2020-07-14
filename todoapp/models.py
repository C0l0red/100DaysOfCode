from django.db import models

# Create your models here.
    
class TodoCategory(models.Model):
    name = models.CharField(max_length=30, unique=True)

class TodoListItem(models.Model):
    content = models.TextField()
    category = models.ForeignKey(TodoCategory, on_delete=models.CASCADE, default=1, related_name='items')
    username = models.CharField(max_length=30, default=1)