from django.urls import path

from . import views

urlpatterns = [
    path('shop/', views.home, name='home'),
    path('registration/', views.RegistrationView.as_view(), name='registration'),
    path('login/', views.MyLoginView.as_view(), name='login'),
    path('logout/', views.MyLogoutView.as_view(), name='logout'),
    path('update-profile/<pk>/', views.UpdateProfile.as_view(), name='updateprofile'),
    path(r'activate/<uidb64>/<token>/', views.activate_account, name='activate'),
]
