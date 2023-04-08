from django.contrib import admin
from django.urls import path, include
from .views import first
from quiz_10000_uber_mega_super_bot import urls as quiz_10000_uber_mega_super_bot_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', first),
    path('accounts/', include('django.contrib.auth.urls')),
    path('registration/', include('users.urls')),
    path('', include('users.urls')),
    path('quiz_10000_uber_mega_super_bot/', include(quiz_10000_uber_mega_super_bot_urls)),
]
