from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('__debug__/', include('debug_toolbar.urls')),
    path('giris/', auth_views.LoginView.as_view(template_name='surveys/login.html'), name='login'),
    path('cikis/', auth_views.LogoutView.as_view(), name='logout'),
    path('', include('surveys.urls')),
]

# Özel hata handler'ları
handler400 = 'surveys.error_views.error_400'
handler403 = 'surveys.error_views.error_403'
handler404 = 'surveys.error_views.error_404'
handler500 = 'surveys.error_views.error_500'
