from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AssignmentListCreateView, AssignmentDetailView, SubmissionViewSet, SubmissionListCreateView

router = DefaultRouter()
router.register(r'submission-api', SubmissionViewSet, basename='submission')

urlpatterns = [
    path('assignments/', AssignmentListCreateView.as_view(), name='assignment-list'),
    path('assignments/<int:pk>/', AssignmentDetailView.as_view(), name='assignment-detail'),
    path('', include(router.urls)),
]