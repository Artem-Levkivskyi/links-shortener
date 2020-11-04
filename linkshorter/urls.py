from django.urls import path
from . import views

app_name = "linkshorter"

urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('get/', views.result_page, name='result_page'),
    path('<key>/', views.redirect),
]
