from django.contrib import admin
from .models import UserAction
import sys
sys.path.append("..") # Adds higher directory to python modules path.
from login.models import User
# Register your models here.


admin.site.register(UserAction)