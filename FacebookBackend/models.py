from django.contrib.auth.models import User
from django.db import models


# Create your models here.

# FBClone User Profile
class Profile(models.Model):
    nick_name = models.CharField(max_length=64, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    phonenum = models.CharField(max_length=20, unique=True)
    gender = models.CharField(max_length=20, null=True, blank=True)
    born_place = models.CharField(max_length=128, null=True, blank=True)
    languages_known = models.CharField(max_length=56, null=True, blank=True)
    relationship_status = models.IntegerField(null=True, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)


class ProfilePicture(models.Model):
    image = models.CharField(max_length=256, null=True, blank=True)
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, unique=True)


class CoverPicture(models.Model):
    image = models.CharField(max_length=256, null=True, blank=True)
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, unique=True)


class Languages(models.Model):
    name = models.CharField(max_length=128)


class LinkedAccount(models.Model):
    name = models.CharField(max_length=128)
    link = models.CharField(max_length=256)
    created_time = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)


class Gender(models.Model):
    name = models.CharField(max_length=56)


class Post(models.Model):
    captions = models.CharField(max_length=1024, null=True, blank=True)
    tagged_ids = models.CharField(max_length=128, null=True, blank=True)  # contains the user_ids with coma separated
    likes_ids = models.CharField(max_length=512, null=True, blank=True)  # contains the user_ids with coma separated
    created_time = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


# class AttachmentLinks(models.Model):
#     file = models.FileField(max_length=256, null=True)
#     type = models.CharField(max_length=10)
#     created_time = models.DateTimeField(auto_now_add=True)
#     last_modified = models.DateTimeField(auto_now=True)
#     post = models.ForeignKey(Post, on_delete=models.CASCADE)

class AttachmentLinks(models.Model):
    file = models.CharField(max_length=256)
    type = models.CharField(max_length=10)
    created_time = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    # class Meta:
    #     unique_together = ('file', 'type')
    #     ordering = ['last_modified']
    #
    # def __str__(self):
    #     # return {'file': self.file, 'type': self.type}
    #     return ""+str(self.id)+" : "+str(self.file)+" : "+str(self.type)


class Comment(models.Model):
    comment_text = models.CharField(max_length=256)
    like_ids = models.CharField(max_length=256, null=True, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_by = models.ForeignKey(User, on_delete=models.CASCADE)


class Reply(models.Model):
    reply_text = models.CharField(max_length=256)
    like_ids = models.CharField(max_length=256, null=True, blank=True)
    # contains the Reply table id's because a reply can have one/more replies
    reply_ids = models.CharField(max_length=256, null=True, blank=True)
    replied_by = models.ForeignKey(User,on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)


class Friends(models.Model):
    user = models.ForeignKey(User, models.CASCADE, related_name="user")
    friend = models.ForeignKey(User, models.CASCADE, related_name="friend")
    status = models.IntegerField() # 1 for Request Accepted, 0 for Request under pending...
    # friends_ids = models.CharField(max_length=1024, null=True, blank=True)  # contains the user ids with coma
    # separated.
