import datetime

from django.test import TestCase
from django.utils import timezone

from .models import Question, Choice


class QuestionModelTests(TestCase):

    def test_question_str_representation(self):
        question = Question(question_text='What is your name?', pub_date=timezone.now())
        self.assertEqual(str(question), 'What is your name?')
        self.assertNotEqual(str(question), '')

    def test_was_published_recently_passes_with_recent_question(self):
        recent_date = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        question = Question(pub_date=recent_date)
        self.assertIs(question.was_published_recently(), True)

    def test_was_published_recently_fails_with_future_date(self):
        future_date = timezone.now() + datetime.timedelta(days=30)
        question = Question(pub_date=future_date)
        self.assertIs(question.was_published_recently(), False)

    def test_was_published_recently_fails_with_old_date(self):
        past_date = timezone.now() - datetime.timedelta(days=1, seconds=1)
        question = Question(pub_date=past_date)
        self.assertIs(question.was_published_recently(), False)


class ChoiceModelTests(TestCase):

    def test_question_str_representation(self):
        question = Question(question_text='What is your name?', pub_date=timezone.now())
        choice = Choice(question, choice_text='Bob')
        self.assertEqual(str(choice), 'Bob')
        self.assertNotEqual(str(choice), 'What is your name?')
