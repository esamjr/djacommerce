from django.db import models
from django.contrib.auth.models import User
from PIL import Image
# import datetime
from datetime import datetime, timedelta

class Profile(models.Model):
    user_account_name = models.OneToOneField(User, on_delete=models.CASCADE)
    user_image = models.ImageField(
        default='avatar.svg',
        upload_to='user_image')
    created_date = models.DateTimeField(auto_now_add=True)
    activation_key = models.CharField(max_length=100, blank=True)
    key_expires = models.TextField(default=datetime.now()+timedelta(minutes=1), editable=False, max_length=20)

    def __str__(self):
        return f'{self.user_account_name.username} Profile'


