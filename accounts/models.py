from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Role(models.Model):
    ROLES = (
        ('user', 'user'),
        ('admin', 'admin')
    )
     
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    roleName = models.CharField(max_length=100)


    def __str__(self):
        return self.user.username
    