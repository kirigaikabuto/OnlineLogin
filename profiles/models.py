from django.db import models
from django.contrib.auth.models import User
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    about  = models.TextField()
    avatar = models.FileField(upload_to="user_photos/")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username