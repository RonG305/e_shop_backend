from django.urls import path
from accounts import views


urlpatterns = [
    path('signup/', views.signup_user, name='signup'),
    path('signin/', views.signin_user, name='signin'),
    path("logout/", views.logout_user, name="logout")
]