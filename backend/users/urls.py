# backend/users/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MyTokenObtainPairView, UserViewSet
from rest_framework_simplejwt.views import TokenRefreshView

# Create a router and register our new viewset with it.
router = DefaultRouter()
router.register(r'', UserViewSet, basename='user')

urlpatterns = [
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # The router generates: /users/, /users/<id>/, etc.
    path('', include(router.urls)), 
]