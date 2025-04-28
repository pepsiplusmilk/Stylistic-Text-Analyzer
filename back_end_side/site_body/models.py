from django.db import models

def get_file_upload_path(instance, filename):
    return "requests/{0}".format(filename)

class UserText(models.Model):
    plain_text = models.CharField(max_length=3000) # 3000 max len of user text
    text_file = models.FileField(upload_to=get_file_upload_path)