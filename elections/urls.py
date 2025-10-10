from django.urls import path
from . import views

app_name = 'elections'

urlpatterns = [
    path('', views.resultats_globaux, name='resultats_globaux'),
    path('centres/', views.resultats_par_centre, name='resultats_par_centre'),
    path('bureaux/', views.resultats_par_bureau, name='resultats_par_bureau'),
    path('bureau/<int:bureau_id>/', views.detail_bureau, name='detail_bureau'),
]