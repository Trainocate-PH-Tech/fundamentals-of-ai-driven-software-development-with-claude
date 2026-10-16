import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from app.models.tracker import Category, Issue
from app.seed_tracker import seed_categories


def test_crud_and_case_insensitive_uniqueness(client, auth_headers):
    response = client.post('/categories', headers=auth_headers, json={'name':' Bug '})
    assert response.status_code == 201
    category = response.json()
    assert category['name'] == 'Bug'
    assert client.post('/categories', headers=auth_headers, json={'name':'bUg'}).status_code == 409
    assert client.get('/categories/'+category['id'],headers=auth_headers).json()['name'] == 'Bug'
    response = client.patch('/categories/'+category['id'],headers=auth_headers,json={'name':'Defect','description':'test'})
    assert response.status_code == 200
    assert response.json()['description']=='test'
    assert client.get('/categories',headers=auth_headers).json()['records'][0]['name']=='Defect'
    response = client.delete('/categories/'+category['id'],headers=auth_headers)
    assert response.status_code==204 and response.content==b''
    assert client.get('/categories/'+category['id'],headers=auth_headers).status_code==404


@pytest.mark.parametrize('payload',[{'name':''},{'name':'  '},{'name':None},{'name':'a'*101},{'name':'Bug','description':'x'*501},{}])
def test_validation(client,auth_headers,payload):
    assert client.post('/categories',headers=auth_headers,json=payload).status_code==422


def test_integrity_and_protected_deletion(client,auth_headers,db_session):
    category=Category(name='Bug');db_session.add(category);db_session.commit()
    issue=Issue(title='Example',category_id=category.id);db_session.add(issue);db_session.commit()
    assert client.delete('/categories/'+category.id,headers=auth_headers).status_code==409
    assert db_session.get(Issue,issue.id)
    assert client.patch('/categories/'+category.id,headers=auth_headers,json={'name':'Defect'}).status_code==200
    db_session.expire_all();assert db_session.get(Issue,issue.id).category_id==category.id
    db_session.add(Category(name='DEFECT'))
    with pytest.raises(IntegrityError): db_session.commit()
    db_session.rollback()


def test_auth_pagination_and_seed(client,db_session,auth_headers):
    assert client.get('/categories').status_code==401
    seed_categories(db_session);seed_categories(db_session)
    assert len(db_session.scalars(select(Category)).all())==4
    response=client.get('/categories?per_page=100',headers=auth_headers).json()
    assert [x['name'] for x in response['records']]==['Bug','Documentation','Feature Request','Task']
    assert client.get('/categories?per_page=0',headers=auth_headers).status_code==422
