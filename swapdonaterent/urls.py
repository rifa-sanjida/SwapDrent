from django.contrib import admin  # Import the admin panel
from django.urls import path, include  # Tools for creating website URLs
from django.conf import settings  # Access our project settings
from django.conf.urls.static import static  # Serve files during development

# This list tells Django which URLs go to which pages
urlpatterns = [
    path('admin/', admin.site.urls),          # The admin dashboard lives at /admin/
    path('', include('core.urls', namespace='core')),      # Homepage and basic pages
    path('users/', include('users.urls', namespace='users')),  # All user account pages
    path('items/', include('items.urls', namespace='items')),  # All item-related pages
]

# During development, serve user-uploaded files and static files
if settings.DEBUG:
    # This makes uploaded images available at /media/
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # This makes CSS/JS files available at /static/
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
