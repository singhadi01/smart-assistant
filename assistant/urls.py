from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('ask/', views.ask_anything, name='ask'),
    path('reset/', views.reset_chat, name='reset_chat'),
    path('quiz/', views.quiz_view, name="quiz"),
]