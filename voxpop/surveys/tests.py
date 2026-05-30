import datetime
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from .models import Category, Survey, Question, Choice, Vote

def make_survey(title='Test', status='active', stype='hazir'):
    cat, _ = Category.objects.get_or_create(slug='test', defaults={'name':'Test','icon':'🧪'})
    return Survey.objects.create(title=title, category=cat, status=status, survey_type=stype)

def make_question(survey, text='Soru?'):
    return Question.objects.create(survey=survey, text=text, order=1)

def make_choice(question, text='Seçenek'):
    return Choice.objects.create(question=question, text=text, icon='✅', order=1)

class ModelTests(TestCase):
    def test_is_active_true(self):
        self.assertTrue(make_survey().is_active())
    def test_is_active_false_for_draft(self):
        self.assertFalse(make_survey(status='draft').is_active())
    def test_was_created_recently(self):
        self.assertTrue(make_survey().was_created_recently())
    def test_vote_percentage_zero(self):
        q = make_question(make_survey())
        c = make_choice(q)
        self.assertEqual(c.vote_percentage(), 0)
    def test_total_votes_zero(self):
        s = make_survey()
        self.assertEqual(s.total_votes(), 0)

class ViewTests(TestCase):
    def test_index_200(self):
        self.assertEqual(self.client.get(reverse('surveys:index')).status_code, 200)
    def test_list_200(self):
        self.assertEqual(self.client.get(reverse('surveys:survey_list')).status_code, 200)
    def test_detail_200_active(self):
        s = make_survey()
        self.assertEqual(self.client.get(reverse('surveys:survey_detail', args=[s.pk])).status_code, 200)
    def test_detail_404_draft(self):
        s = make_survey(status='draft')
        self.assertEqual(self.client.get(reverse('surveys:survey_detail', args=[s.pk])).status_code, 404)
    def test_results_200(self):
        s = make_survey()
        self.assertEqual(self.client.get(reverse('surveys:results', args=[s.pk])).status_code, 200)
    def test_create_survey_requires_login(self):
        r = self.client.get(reverse('surveys:create_survey'))
        self.assertRedirects(r, '/giris/?next=/anket-olustur/')

class VoteTests(TestCase):
    def setUp(self):
        self.survey = make_survey()
        self.q = make_question(self.survey)
        self.c = make_choice(self.q)
    def test_vote_success(self):
        r = self.client.post(reverse('surveys:vote', args=[self.survey.pk, self.q.pk]), {'choice': self.c.pk})
        self.assertEqual(r.status_code, 302)
        self.c.refresh_from_db()
        self.assertEqual(self.c.votes, 1)
    def test_duplicate_vote_blocked(self):
        for _ in range(2):
            self.client.post(reverse('surveys:vote', args=[self.survey.pk, self.q.pk]), {'choice': self.c.pk})
        self.c.refresh_from_db()
        self.assertEqual(self.c.votes, 1)
    def test_no_choice_no_vote(self):
        self.client.post(reverse('surveys:vote', args=[self.survey.pk, self.q.pk]), {})
        self.c.refresh_from_db()
        self.assertEqual(self.c.votes, 0)
    def test_closed_survey_rejected(self):
        self.survey.status = 'closed'
        self.survey.save()
        self.client.post(reverse('surveys:vote', args=[self.survey.pk, self.q.pk]), {'choice': self.c.pk})
        self.c.refresh_from_db()
        self.assertEqual(self.c.votes, 0)

class UserSurveyTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('testuser', password='test123')
        self.client.login(username='testuser', password='test123')
    def test_create_survey_get(self):
        r = self.client.get(reverse('surveys:create_survey'))
        self.assertEqual(r.status_code, 200)
    def test_create_survey_post(self):
        cat, _ = Category.objects.get_or_create(slug='test', defaults={'name':'Test','icon':'🧪'})
        r = self.client.post(reverse('surveys:create_survey'), {
            'title': 'Benim Anketim', 'description': 'Test', 'thumbnail': '🎯', 'category': cat.pk
        })
        self.assertEqual(Survey.objects.filter(created_by=self.user).count(), 1)
    def test_my_surveys_200(self):
        r = self.client.get(reverse('surveys:my_surveys'))
        self.assertEqual(r.status_code, 200)
