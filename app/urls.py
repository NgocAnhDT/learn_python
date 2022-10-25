from django.urls import path, include
from rest_framework import routers

from .views import *

router = routers.DefaultRouter()
router.register(r'users', UserView, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('update/<int:pk>/', UpdateUserView.as_view({'put': 'update'})),
]
