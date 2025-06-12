from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):
    DIFFICULTY_LEVELS = (
        ('Easy', 'Easy'),
        ('Medium', 'Medium'),
        ('Hard', 'Hard'),
    )
    text = models.TextField()
    option1 = models.CharField(max_length=200)
    option2 = models.CharField(max_length=200)
    option3 = models.CharField(max_length=200)
    option4 = models.CharField(max_length=200)
    correct_option = models.IntegerField()
    category = models.CharField(max_length=100, default="General")
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_LEVELS, default='Easy')  # New difficulty field

    def __str__(self):
        return self.text

class QuizAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()
    time_taken = models.FloatField()
    total_questions = models.IntegerField()
    correct_answers = models.IntegerField()
    wrong_answers = models.IntegerField()
    percentage = models.FloatField()
    attempted_at = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=100, null=True, blank=True)
    difficulty = models.CharField(max_length=10, choices=Question.DIFFICULTY_LEVELS, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s attempt at {self.attempted_at}"