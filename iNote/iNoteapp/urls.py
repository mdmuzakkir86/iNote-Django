from django.urls import  path
from . import views

urlpatterns = [
    path('', views.add_notes),
    path('getnotes', views.get_notes),
    path('edit/<str:id>', views.edit_note),
    path('update', views.update_note)
]
