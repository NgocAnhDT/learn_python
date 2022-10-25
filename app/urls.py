from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView
from app.views import LoginUserApi, Logout, InsuranceView, UpdateView, upload
from django.conf import settings
from django.conf.urls.static import static

router = routers.DefaultRouter()
router.register(r'insurances', InsuranceView)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginUserApi.as_view()),
    path('update-status/', UpdateView.as_view({'get': 'update_status'})),
    path('logout/', Logout.as_view({'delete': 'destroy'})),
    path('token_refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('upload/', upload),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
