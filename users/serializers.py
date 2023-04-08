from rest_framework import serializers
from .models import Question, Quiz, Answer


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'text', 'is_correct']


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'text', 'answers']

    answers = AnswerSerializer(many=True)


class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Quiz
        fields = ['id', 'title', 'questions']

    def create(self, validated_data):
        questions_data = validated_data.pop('questions')
        quiz = Quiz.objects.create(**validated_data)
        for question_data in questions_data:
            answers_data = question_data.pop('answers')
            question = Question.objects.create(quiz=quiz, **question_data)
            for answer_data in answers_data:
                Answer.objects.create(question=question, **answer_data)
        return quiz

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.save()
        questions_data = validated_data.get('questions', [])
        for question_data in questions_data:
            answers_data = question_data.pop('answers', [])
            question_id = question_data.get('id')
            if question_id:
                question = Question.objects.get(id=question_id)
                question.text = question_data.get('text', question.text)
                question.save()
            else:
                question = Question.objects.create(quiz=instance, **question_data)
            for answer_data in answers_data:
                answer_id = answer_data.get('id')
                if answer_id:
                    answer = Answer.objects.get(id=answer_id)
                    answer.text = answer_data.get('text', answer.text)
                    answer.is_correct = answer_data.get('is_correct', answer.is_correct)
                    answer.save()
                else:
                    Answer.objects.create(question=question, **answer_data)
        return instance