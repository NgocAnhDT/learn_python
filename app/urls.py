from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView
from app.views import LoginUserApi, Logout

router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginUserApi.as_view()),
    path('logout/', Logout.as_view({'delete': 'destroy'})),
    path('token_refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
