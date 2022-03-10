from django.contrib import admin

# Register your models here.
from .models import BigDWord, WordleWord
admin.site.register(BigDWord)
admin.site.register(WordleWord)