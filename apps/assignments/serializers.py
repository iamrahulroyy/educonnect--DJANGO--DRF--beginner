from rest_framework import serializers
from .models import Assignment, Submission

class AssignmentSerializer(serializers.ModelSerializer):
    teacher = serializers.ReadOnlyField(source='teacher.username')

    class Meta:
        model = Assignment
        fields = '__all__'


class SubmissionSerializer(serializers.ModelSerializer):
    student = serializers.ReadOnlyField(source='student.username')
    graded = serializers.SerializerMethodField()
    grade = serializers.CharField(read_only=True)
    feedback = serializers.CharField(read_only=True)

    class Meta:
        model = Submission
        fields = [
            'id',
            'assignment',
            'student',
            'content',
            'file',
            'submitted_at',
            'grade',
            'feedback',
            'graded_at',
            'graded',
        ]
        read_only_fields = [
            'id',
            'student',
            'submitted_at',
            'graded_at',
            'graded',
        ]

    def get_graded(self, obj):
        return obj.grade is not None

