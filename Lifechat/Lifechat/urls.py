"""
URL configuration for Lifechat project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from lifeapp import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/',views.UserRegisterView.as_view()),
    path('login',views.LoginView.as_view()),
    path('connection/send',views.SendConnectionRequestView.as_view()),
    path('connection/accept/<int:pk>',views.AcceptConnectionRequestView.as_view()),
    path('connection/rejected/<int:pk>',views.RejectedConnectionRequestView.as_view()),
    path('connection/pending',views.PendingRequestListView.as_view()),
    path('connection/myconnections',views.MyConnectionListView.as_view()),
    path('profile/my',views.MyProfileView.as_view()),
    path('directory/search',views.DirectorySearchView.as_view()),
    path('donation/submit',views.SubmitDonationView.as_view()),
    path('donation/my',views.MyDonationListView.as_view()),
    path('donation/pending',views.PendingDonationListView.as_view()),
    path('donation/approve/<int:pk>',views.ApproveDonationView.as_view()),
    path('donation/reject/<int:pk>',views.RejectDonationView.as_view())
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
