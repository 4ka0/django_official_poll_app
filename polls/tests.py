import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

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


def create_question(question_text, days):
    """
    Create a question with the given 'question_text' and published the
    given number of 'days' offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """
        question = create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],
        )

    def test_future_question(self):
        """
        Questions with a pub_date in the future aren't displayed on
        the index page.
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        question = create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],
        )

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        question1 = create_question(question_text="Past question 1.", days=-30)
        question2 = create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question2, question1],
        )
