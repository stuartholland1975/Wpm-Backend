from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
                  path('admin/doc/', include('django.contrib.admindocs.urls')),
                  path('admin/', admin.site.urls),
                  path('api/', include('authentication.urls')),
                  path('wpm/', include('work_orders.urls')),
                  path('bulk/', include('bulk_api.urls')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
