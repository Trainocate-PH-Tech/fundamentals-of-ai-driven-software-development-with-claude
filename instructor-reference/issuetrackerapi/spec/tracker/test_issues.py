import pytest
from app.models.tracker import Category


@pytest.fixture
def category(db_session):
    item=Category(name='Bug');db_session.add(item);db_session.commit();return item


def test_issue_lifecycle(client,auth_headers,category):
    response=client.post('/issues',headers=auth_headers,json={'title':' Login broken ','category_id':category.id})
    assert response.status_code==201
    issue=response.json();assert issue['title']=='Login broken'
    assert issue['status']=='open' and issue['priority']=='medium' and issue['assigned_user_id'] is None
    assert issue['category']['name']=='Bug'
    url='/issues/'+issue['id']
    assert client.get(url,headers=auth_headers).status_code==200
    for status in ['closed','in_progress','resolved','open']:
        updated=client.patch(url,headers=auth_headers,json={'status':status,'description':'Details'}).json()
        assert updated['status']==status and updated['title']=='Login broken'
    assert client.get('/issues',headers=auth_headers).json()['records'][0]['id']==issue['id']
    assert client.delete('/categories/'+category.id,headers=auth_headers).status_code==409
    deleted=client.delete(url,headers=auth_headers);assert deleted.status_code==204 and deleted.content==b''
    assert client.get(url,headers=auth_headers).status_code==404
    assert client.delete('/categories/'+category.id,headers=auth_headers).status_code==204


@pytest.mark.parametrize('change',[{'title':''},{'title':None},{'title':'x'*201},{'description':'x'*5001},
 {'status':'wrong'},{'priority':'wrong'},{'category_id':None},{'status':None},{'priority':None}])
def test_issue_validation(client,auth_headers,category,change):
    payload={'title':'Example','category_id':category.id}
    assert client.post('/issues',headers=auth_headers,json={**payload,**change}).status_code==422
    issue=client.post('/issues',headers=auth_headers,json=payload).json()
    assert client.patch('/issues/'+issue['id'],headers=auth_headers,json=change).status_code==422


def test_issue_missing_reference_and_auth(client,auth_headers,user_auth_headers,category):
    assert client.get('/issues').status_code==401
    assert client.post('/issues',headers=auth_headers,json={'title':'Example','category_id':'missing'}).status_code==404
    assert client.post('/issues',headers=user_auth_headers,json={'title':'Example','category_id':category.id}).status_code==201
    assert client.patch('/issues/missing',headers=auth_headers,json={'title':'New'}).status_code==404
