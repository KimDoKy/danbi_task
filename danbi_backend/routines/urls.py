from django.urls import path
from .views import RoutineView, get_routine, get_routine_list

app_name = 'routines'

urlpatterns = [
    path('', RoutineView.as_view(), name="routine"),
    path('<int:routine_id>/', RoutineView.as_view()),
    path('target/', get_routine, name='target'),
    path('list/', get_routine_list, name="list"),
]
