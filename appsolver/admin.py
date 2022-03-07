from django.contrib import admin

# Register your models here.
from .models import BigDWord, WordleWord, ValidWord
admin.site.register(BigDWord)
admin.site.register(WordleWord)
admin.site.register(ValidWord)