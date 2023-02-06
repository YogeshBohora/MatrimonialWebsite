from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Status(models.Model):
    status = models.CharField(max_length=30,null=True)
    def __str__(self):
        return self.status

class Signup(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    status=models.ForeignKey(Status,on_delete=models.CASCADE,null=True)
    gen = models.CharField(max_length=10,null=True)
    dob = models.DateField(null=True)
    city = models.CharField(max_length=30, null=True)
    address = models.CharField(max_length=50, null=True)
    contact = models.CharField(max_length=10, null=True)
    image = models.FileField(null=True)

    def __str__(self):
        return self.user.username


class Religion(models.Model):
    religion = models.CharField(max_length=50,null=True)
    def __str__(self):
        return self.religion

class Profile(models.Model):
    signup = models.ForeignKey(Signup, on_delete=models.CASCADE, null=True)
    f_name = models.CharField(max_length=100,null=True)
    m_name = models.CharField(max_length=100,null=True)
    religion = models.ForeignKey(Religion,on_delete=models.CASCADE,null=True)
    f_contact = models.CharField(max_length=10,null=True)
    qualification = models.CharField(max_length=50,null=True)
    salary = models.IntegerField(null=True)
    age = models.IntegerField(null=True)
    family_type = models.CharField(max_length=50,null=True)
    hobby = models.CharField(max_length=100,null=True)
    occupation = models.CharField(max_length=100,null=True)
    work_address = models.CharField(max_length=100,null=True)
    def __str__(self):
        return self.signup.user.username

class SendMessage(models.Model):
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE,null=True)
    send_user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    message1 = models.TextField(null=True)

    def __str__(self):
        return self.profile.signup.user.username+" "+"(Send_By)"+self.send_user.username

class Send_Feedback(models.Model):
    signup = models.ForeignKey(Signup, on_delete=models.CASCADE, null=True)
    message1 = models.TextField(null=True)
    date = models.CharField(max_length=30, null=True)

    def __str__(self):
        return self.signup.user.username


