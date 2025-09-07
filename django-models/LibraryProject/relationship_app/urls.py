from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    # Registration (custom view)
    path('register/', views.register, name='register'),

    # Login (built-in class-based view)
    path('login/', LoginView.as_view(template_name="relationship_app/login.html"), name='login'),

    # Logout (built-in class-based view)
    path('logout/', LogoutView.as_view(template_name="relationship_app/logout.html"), name='logout'),
]