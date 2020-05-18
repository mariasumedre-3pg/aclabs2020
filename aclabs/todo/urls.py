from django.urls import path

import todo.views

urlpatterns = [
    path("", todo.views.index, name="index")
]