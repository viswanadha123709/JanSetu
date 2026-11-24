from django.urls import path
from apps.schemes.views import SchemeListView, SchemeDetailView, PolicyListView, PolicyDetailView, CategoryListView, StateListView, StatsView

urlpatterns = [
    path('schemes/', SchemeListView.as_view(), name='schemes_list'),
    path('schemes/<int:pk>/', SchemeDetailView.as_view(), name='scheme_detail'),
    path('policies/', PolicyListView.as_view(), name='policies_list'),
    path('policies/<int:pk>/', PolicyDetailView.as_view(), name='policy_detail'),
    path('categories/', CategoryListView.as_view(), name='categories_list'),
    path('states/', StateListView.as_view(), name='states_list'),
    path('stats/', StatsView.as_view(), name='stats_summary'),
]
