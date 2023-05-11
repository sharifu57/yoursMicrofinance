from django.db import models
from loan.models import MainModel
from django.contrib.auth.models import User, Group
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from viewflow.models import Process, Task

# Create your models here.
class WorkFlow(MainModel):
    name = models.CharField(max_length=200, null=True, blank=True)
    code  = models.CharField(max_length=200, null=True, blank=True)
    
    def __str__(self):
        return self.name
    
class Stage(MainModel):
    flow = models.ForeignKey('workflow.WorkFlow', related_name='stages',null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True, blank=True)
    
    def __str__(self):
        return self.name
    
class Actors(MainModel):
    stage = models.ForeignKey('workflow.Stage', related_name='actors', null=True, blank=True, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, related_name='stage_actors', on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.stage} - {self.group}"
    
class StageHistory(MainModel):
    stage = models.ForeignKey(Stage, related_name='stage_history', on_delete=models.CASCADE, null=True, blank=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey()
    
    def __str__(self):
        return str(self.stage) + str(f"--- {self.content_object}")
    

class FlowProcess(Process):
    code = models.CharField(max_length=200, null=True, blank=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey()
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)
    
    def __str__(self):
        return self.code
    
    
    