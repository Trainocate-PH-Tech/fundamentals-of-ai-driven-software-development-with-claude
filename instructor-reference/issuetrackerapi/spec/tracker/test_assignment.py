from app.models.tracker import Category
from spec.factories import UserFactory


def test_assign_omit_null_invalid(client,auth_headers,user_auth_headers,db_session):
    user=UserFactory();category=Category(name='Bug');db_session.add(category);db_session.commit()
    response=client.post('/issues',headers=auth_headers,json={'title':'Example','category_id':category.id,'assigned_user_id':user.id})
    assert response.status_code==201
    issue=response.json();url='/issues/'+issue['id']
    assert set(issue['assigned_user'])=={'id','full_name'}
    assert client.patch(url,headers=auth_headers,json={'title':'Other'}).json()['assigned_user_id']==user.id
    assert client.patch(url,headers=auth_headers,json={'assigned_user_id':'missing'}).status_code==404
    assert client.get(url,headers=auth_headers).json()['assigned_user_id']==user.id
    assert client.patch(url,headers=auth_headers,json={'assigned_user_id':None}).json()['assigned_user_id'] is None
    assert client.get(url,headers=auth_headers).json()['assigned_user'] is None
    assert client.get('/assignees').status_code==401
    options=client.get('/assignees',headers=user_auth_headers).json()
    assert any(x['id']==user.id for x in options)
    assert all(set(x)=={'id','full_name'} for x in options)
    assert client.get('/users',headers=user_auth_headers).status_code==403
