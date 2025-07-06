from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("", RedirectView.as_view(url='/food/', permanent=False)),
    path("admin/logout/", LogoutView.as_view(next_page='/food/'), name='admin_logout'),
    path("admin/", admin.site.urls),
    path("food/", include("food.urls")),
    path("users/", include("users.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
