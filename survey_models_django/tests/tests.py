from django.test import TestCase
from .models import (
                Option,
                Question,
                Test,
                Testrun,
                Answer
                )

from django.test import Client


class QuizTests(TestCase):
    

    def setUp(self) -> None:
        self.option1 = Option.objects.create(text="some option1")
        self.option2 = Option.objects.create(text="some option2")
        self.option3 = Option.objects.create(text="some option3")

        self.question = Question.objects.create(text="Who was...",
                                                right_option=self.option1)
        self.question.options.add(self.option1)
        self.question.options.add(self.option2)
        self.question.options.add(self.option3)

        self.answer = Answer.objects.create(question=self.question,
                                            user_answer=self.option1)
        
        self.test = Test.objects.create(title="Test 1", description="bla bla")
        self.test.questions.add(self.question)

        self.test2 = Test.objects.create(title="Bla bla", description="bla bla")
        self.test2.questions.add(self.question)

        self.test_session = Testrun.objects.create(test=self.test)
        self.test_session.answers.add(self.answer)

        self.client = Client()

    def test_detail_view(self):
        resp = self.client.get('/1/')
        self.assertTemplateUsed(resp, 'tests/detail.html')
    
    def test_create_session_right_answer(self):
        resp = self.client.post('/start/1/', data={'1':'1'})
        self.assertEqual(resp.status_code, 302)
        new_test_session = Testrun.objects.get(pk=2)
        self.assertEqual(new_test_session.points, 1)
    
    def test_create_session_wrong_answer(self):
        resp = self.client.post('/start/1/', data={'1':'3'})
        self.assertEqual(resp.status_code, 302)
        new_test_session = Testrun.objects.get(pk=2)
        self.assertNotEqual(new_test_session.points, 1)
        self.assertEqual(new_test_session.points, 0)

    def test_list_view(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'home.html')
    
    def test_list_view_search(self):
        resp = self.client.get('/?search=Test 1')
        self.assertEqual(resp.status_code, 200)
        self.assertContains(text=self.test.title, response=resp)
        self.assertContains(text=self.test.description, response=resp)
    
    def test_list_view_search_blank(self):
        resp = self.client.get('/?search=OOOOOORRRR')
        self.assertEqual(resp.status_code, 200)
        self.assertNotContains(text=self.test.title, response=resp)
        self.assertNotContains(text=self.test.description, response=resp)
        self.assertContains(text="Sorry, can not find any matches...", response=resp)
    
    def test_session_history_view(self):
        resp = self.client.get('/history/1/')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'tests/history.html')
        self.assertContains(text=self.test_session.points, response=resp)
        self.assertContains(text=self.test_session.test.title, response=resp)
        self.assertContains(text=str(self.test_session.finished_at)[0:4], response=resp)

        