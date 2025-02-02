from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.db import models
from django.contrib.auth.models import User


# class Note(models.Model):
#     title = models.CharField(max_length=200)
#     content = models.TextField()
#     created_by = models.ForeignKey(User, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.title



# from django.db import models
# from django.contrib.auth.models import User
# from datetime import datetime

# class Note(models.Model):
#     title = models.CharField(max_length=200)
#     content = models.TextField()
#     created_by = models.ForeignKey(User, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(null=True, blank=True)
#     updated_at = models.DateTimeField(null=True, blank=True)

#     def save(self, *args, **kwargs):
#         if not self.id:
#             self.created_at = datetime.now()
#         self.updated_at = datetime.now()
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return self.title


from django.utils.timezone import now
from django.db import models
from django.contrib.auth.models import User


class Note(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set on creation
    updated_at = models.DateTimeField(auto_now=True)      # Automatically update on save

    def __str__(self):
        return self.title
