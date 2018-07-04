from django.contrib import admin

# Register your models here.
from FacebookBackend import models

admin.site.register(models.ProfilePicture)
admin.site.register(models.Profile)
admin.site.register(models.CoverPicture)
admin.site.register(models.Languages)
admin.site.register(models.AttachmentLinks)
admin.site.register(models.Comment)
admin.site.register(models.Friends)
admin.site.register(models.Gender)
admin.site.register(models.LinkedAccount)
admin.site.register(models.Post)
admin.site.register(models.Reply)