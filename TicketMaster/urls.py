from . import views
from django.urls import path

from .views import display_favourite

urlpatterns = [

    path('',views.ticketmaster,name='ticketmaster'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('add_favourite/',views.add_favourite,name='add_favourite'),
    path('display_favorite/',views.display_favourite,name='display_favourite'),
    path('delete/<int:event_id>/', views.delete_favourite, name='delete_favourite'),
    path('ticketmaster/update/<int:event_id>/', views.update_favourite, name='update_favourite'),
    path("ajax/delete/", views.delete_event_with_ajax, name="delete_event_with_ajax"),










]