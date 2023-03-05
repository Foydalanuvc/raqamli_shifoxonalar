from django.urls import path
from .views import RegistrationView, LoginView, logout_view, ProfileView, ChangePasswordView
app_name = 'account'
urlpatterns = [
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('change-password/', ChangePasswordView.as_view(), name="change-password"),
]
