from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Assignment, Submission
from .serializers import AssignmentSerializer, SubmissionSerializer
from .permissions import IsTeacher, IsStudent
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from django.utils import timezone
from rest_framework import viewsets


# Create your views here.

# --- Assignment Views ---
class AssignmentListCreateView(generics.ListCreateAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated(), IsTeacher()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class AssignmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    permission_classes = [permissions.IsAuthenticated, IsTeacher]

# --- Submission Views ---
class SubmissionListCreateView(generics.ListCreateAPIView):
    serializer_class = SubmissionSerializer

    def get_queryset(self):
        if self.request.user.role == "TEACHER":
            return Submission.objects.filter(assignment__created_by=self.request.user)
        return Submission.objects.filter(student=self.request.user)

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated(), IsStudent()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)

class SubmissionViewSet(viewsets.ModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)

    @action(detail=True, methods=['patch'], url_path='grade')
    def grade_submission(self, request, pk=None):
        submission = self.get_object()
        
        if submission.assignment.created_by  != request.user:
            return Response({"detail": "You are not allowed to grade this submission."},
                            status=status.HTTP_403_FORBIDDEN)

        grade = request.data.get("grade")
        feedback = request.data.get("feedback")

        if not grade:
            return Response({"detail": "Grade is required."},
                            status=status.HTTP_400_BAD_REQUEST)

        submission.grade = grade
        submission.feedback = feedback
        submission.graded_at = timezone.now()
        submission.save()

        return Response(SubmissionSerializer(submission).data)