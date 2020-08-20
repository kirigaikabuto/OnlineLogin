from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    about = models.TextField()
    avatar = models.FileField(upload_to="user_photos/")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class OrderToFriend(models.Model):
    from_profile = models.ForeignKey(Profile, on_delete= models.CASCADE, related_name="from_profile")
    to_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="to_profile")
    accept = models.BooleanField(default=False)

    def __str__(self):
        return self.from_profile.user.username + "->" + self.to_profile.user.username