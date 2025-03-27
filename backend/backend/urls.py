from django.contrib import admin
from django.urls import path, include, re_path
from api.views import CreateUserView, DeleteUserView, GoogleLoginView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.conf import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/user/register/", CreateUserView.as_view(), name="register"),
    path("api/user/delete/", DeleteUserView.as_view(), name="delete_user"),
    path("api/token/", TokenObtainPairView.as_view(), name="get_token"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="refresh"),
    path("api/google-login/", GoogleLoginView.as_view(), name="google_login"),
    path("api-auth/", include("rest_framework.urls")),
    path("api/", include("api.urls")),
    re_path(r'^(?:.*)/?$', TemplateView.as_view(template_name='index.html')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)