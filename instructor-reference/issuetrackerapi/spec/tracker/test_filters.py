from datetime import datetime, timezone
from app.models.tracker import Category, Issue
from spec.factories import UserFactory


def test_combined_filters_order_and_literal_search(client,auth_headers,db_session):
    category=Category(name='Bug');other=Category(name='Task');db_session.add_all([category,other]);db_session.commit()
    user=UserFactory();stamp=datetime(2025,1,1,tzinfo=timezone.utc)
    a=Issue(id='a',title='Login 100% fail',category_id=category.id,status='in_progress',priority='high',assigned_user_id=user.id,updated_at=stamp)
    b=Issue(id='b',title='LOGIN pending',category_id=category.id,status='open',priority='high',updated_at=stamp)
    c=Issue(id='c',title='Other',category_id=other.id,status='in_progress',priority='low',updated_at=stamp)
    db_session.add_all([a,b,c]);db_session.commit()
    def ids(params):
        response=client.get('/issues',headers=auth_headers,params=params);assert response.status_code==200
        return [x['id'] for x in response.json()['records']]
    assert ids({'search':'login'})==['a','b']
    assert ids({'status':'in_progress'})==['a','c']
    assert ids({'priority':'high'})==['a','b']
    assert ids({'category_id':other.id})==['c']
    assert ids({'assigned_user_id':user.id})==['a']
    assert ids({'search':'LOGIN','status':'in_progress','priority':'high','category_id':category.id,'assigned_user_id':user.id})==['a']
    assert ids({'status':'closed','priority':'high'})==[]
    assert ids({'search':'%'})==['a']
    assert ids({})==['a','b','c']
    assert ids({'page':2,'per_page':2})==['c']
    assert client.get('/issues?status=wrong',headers=auth_headers).status_code==422
    assert client.get('/issues?per_page=0',headers=auth_headers).status_code==422
