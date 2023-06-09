from django.db import models

class Answer(models.Model):
    question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='answers')
    text = models.TextField()
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text

class Question(models.Model):
    quiz = models.ForeignKey('Quiz', on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()

class Quiz(models.Model):
    title = models.CharField(max_length=255)
