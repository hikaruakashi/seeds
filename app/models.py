from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Post(models.Model):
    
    author = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    title = models.CharField(max_length=200,null=False)
    image = models.ImageField(upload_to='images/',null=True,blank=True)
    topic = models.ForeignKey(Topic,on_delete=models.SET_NULL,null=True)
    description = models.TextField(null=False)
    link = models.URLField(null=True)

    
    #class Meta:
        #降順のやつ
        # ordering = ['']
        
    def __str__(self):
        return self.title