"""
URL configuration for graph_theory project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

from extended_user.views import SignUp, ProfileDetailView
from graph_theory import settings

urlpatterns = [
    path('', RedirectView.as_view(url='/course/')),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('users/', include('extended_user.urls')),
    path('reg/', SignUp.as_view(), name='reg'),
    path('course/', include('course.urls')),
    path('builder/', include('builder.urls')),
    path('sets/', include('sets.urls')),
    path('martor/', include('martor.urls')),
    path("select2/", include("django_select2.urls")),
    path('accounts/profile/', ProfileDetailView.as_view(), name='self-profile-detail')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
              + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
