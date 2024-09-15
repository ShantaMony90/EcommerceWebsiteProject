from django.db import models

# Create your models here.


class Contact(models.Model):
    name = models.CharField(max_length=300)
    email = models.EmailField()
    phone_number = models.CharField(max_length=14, null=True, blank=True)
    subject = models.CharField(max_length=100, null=True, blank=True)
    message = models.TextField()

    def __str__(self):
        return self.name


class Banner(models.Model):
    image = models.ImageField(upload_to="media/")
    name = models.CharField(max_length=100)
    price = models.TextField()

    def __str__(self):
        return self.name


class DashboardInfo(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    display_name = models.TextField(max_length=100)
    email = models.EmailField(default='')
    password = models.CharField(max_length=8)
    new_password = models.CharField(max_length=8, default='')
    confirm_password = models.CharField(max_length=8, default='')

    def __str__(self):
        return self.first_name
