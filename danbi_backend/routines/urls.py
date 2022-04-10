from django.urls import path
from .views import (
    RoutineView, 
    get_routine, 
    get_routine_list,
    update_after_routine
)

app_name = 'routines'

urlpatterns = [
    path('', RoutineView.as_view(), name="routine"),
    path('<int:routine_id>/', RoutineView.as_view()),
    path('target/', get_routine, name="target"),
    path('list/', get_routine_list, name="list"),
    path('update/', update_after_routine, name="update-result")
]
