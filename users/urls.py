from django.urls import path

from . import views

urlpatterns = [
    path('user_reg/', views.UserApi.as_view(), name='user_reg'),
    path('user_login/', views.UserLoginApi.as_view(), name='user_login'),
    path('user_verify/', views.VerifyToken.as_view(), name='user_verify')
]
