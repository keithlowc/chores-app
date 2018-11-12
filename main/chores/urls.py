from django.contrib import admin
from django.urls import path
from .views import ChoresCreateView, ChorePostListView, ChorePostDetailedView, ChoresView, ChoresData

from . import views

urlpatterns = [
	path('', ChoresView.as_view(), name='chores'),
	path('about', views.about, name='about'),

    path('chores/update/', ChoresCreateView.as_view(), name='chores-points'),
    path('chores/all/', ChorePostListView.as_view(), name='chores-all'),
    path('chores/<str:username>/', ChorePostDetailedView.as_view(), name='chores-list'),   
    
    path('api/chores/data', ChoresData.as_view(), name='api-data'),    
]
