from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Line)
admin.site.register(LineCom)
admin.site.register(LineComCom)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Emotion)