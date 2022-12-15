from django.urls import path
from . import views

urlpatterns = [
    path('<int:id>', views.detail, name="detail"),
    path('entries/<int:page>', views.entries_list, name="entries"),
    path('new', views.new, name="new"),
    path('delete/<int:id>', views.delete, name='delete'),
    path('calendar', views.calendar_view, name='calendar'),
    path('edit/<int:id>', views.edit, name='edit'),
]