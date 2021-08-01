import pytest

from tests.models import (
                Option,
                Question,
                Test,
                Testrun,
                Answer
                )


@pytest.fixture
def test_session(db):
    option1 = Option.objects.create(text="some option1")
    option2 = Option.objects.create(text="some option2")
    option3 = Option.objects.create(text="some option3")

    question = Question.objects.create(text="Who was...",
                                            right_option=option1)
    question.options.add(option1)
    question.options.add(option2)
    question.options.add(option3)

    answer = Answer.objects.create(question=question,
                                        user_answer=option1)
    
    test = Test.objects.create(title="Test 1", description="bla bla")
    test.questions.add(question)

    test2 = Test.objects.create(title="Bla bla", description="bla bla")
    test2.questions.add(question)

    test_session = Testrun.objects.create(test=test)
    test_session.answers.add(answer)

    return test_session


def test_detail_view(client, test_session):
    resp = client.get('/1/')
    assert 'tests/detail.html' in (t.name for t in resp.templates)

@pytest.mark.django_db
def test_create_session_right_answer(client, test_session):
    resp = client.post('/start/1/', data={'1':'1'})
    assert resp.status_code == 302
    new_test_session = Testrun.objects.get(pk=2)
    assert new_test_session.points == 1

@pytest.mark.django_db
def test_create_session_wrong_answer(client, test_session):
    resp = client.post('/start/1/', data={'1':'3'})
    assert resp.status_code == 302
    new_test_session = Testrun.objects.get(pk=2)
    assert new_test_session.points != 1
    assert new_test_session.points == 0

@pytest.mark.django_db
def test_list_view(client):
    resp = client.get('/')
    assert resp.status_code == 200
    assert 'home.html' in (t.name for t in resp.templates)

@pytest.mark.django_db
def test_list_view_search(client, test_session):
    resp = client.get('/?search=Test 1')
    assert resp.status_code == 200
    assert test_session.test.title in str(resp.content)
    assert test_session.test.description in str(resp.content)
    
def test_list_view_search_blank(client, test_session):
    resp = client.get('/?search=OOOOOORRRR')
    assert resp.status_code == 200
    assert test_session.test.title not in str(resp.content)
    assert test_session.test.description not in str(resp.content)
    assert "Sorry, can not find any matches..." in str(resp.content)
    
def test_session_history_view(client, test_session):
    resp = client.get('/history/1/')
    assert resp.status_code == 200
    assert 'tests/history.html' in (t.name for t in resp.templates)
    assert str(test_session.points) in str(resp.content)
    assert test_session.test.title in str(resp.content)
    assert str(test_session.finished_at)[0:4] in str(resp.content)
