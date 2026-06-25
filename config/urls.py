from tracker.views import DeveloperViewSet, ProjectViewSet, BugViewSet, MeView   # MeView add karo

from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/me/', MeView.as_view(), name='me'),   # <-- ye line add karo
    path('api/', include(router.urls)),
]
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from tracker.views import DeveloperViewSet, ProjectViewSet, BugViewSet

router = DefaultRouter()
router.register(r'developers', DeveloperViewSet, basename='developer')
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'bugs', BugViewSet, basename='bug')

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Authentication Endpoints (JWT)
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Main API Endpoints
    path('api/', include(router.urls)),
]