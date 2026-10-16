"""Exercise Alembic against an isolated disposable PostgreSQL database."""
import os
from uuid import uuid4
import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.engine import make_url


def test_postgres_migration_preserves_users():
    url=make_url(os.environ.get('DATABASE_URL','sqlite://'))
    if url.get_backend_name()!='postgresql':
        pytest.skip('Dedicated PostgreSQL test server required')
    assert url.database.endswith('_test'), 'Use the dedicated test database'
    name='migration_'+uuid4().hex+'_test'
    admin=create_engine(url,isolation_level='AUTOCOMMIT')
    target=url.set(database=name)
    with admin.connect() as connection:
        connection.execute(text(f'CREATE DATABASE "{name}"'))
    engine=create_engine(target)
    import config
    original=config.Config.SQLALCHEMY_DATABASE_URI
    config.Config.SQLALCHEMY_DATABASE_URI=target.render_as_string(hide_password=False)
    cfg=Config('alembic.ini')
    try:
        command.upgrade(cfg,'0002_add_role_to_users')
        with engine.begin() as connection:
            connection.execute(text("INSERT INTO users (id,email,password_hash,first_name,last_name,status,role,created_at,updated_at) VALUES ('existing','keep@example.com','unused','Keep','Me','active','user',now(),now())"))
        command.upgrade(cfg,'head')
        inspector=inspect(engine)
        assert {'users','categories','issues'} <= set(inspector.get_table_names())
        fks={fk['referred_table']:fk['options']['ondelete'] for fk in inspector.get_foreign_keys('issues')}
        assert fks=={'categories':'RESTRICT','users':'SET NULL'}
        with engine.connect() as connection:
            assert connection.scalar(text("SELECT email FROM users WHERE id='existing'"))=='keep@example.com'
        command.downgrade(cfg,'0002_add_role_to_users')
        assert 'issues' not in inspect(engine).get_table_names()
        with engine.connect() as connection:
            assert connection.scalar(text("SELECT count(*) FROM users WHERE id='existing'"))==1
        command.upgrade(cfg,'head')
    finally:
        config.Config.SQLALCHEMY_DATABASE_URI=original
        engine.dispose()
        with admin.connect() as connection:
            connection.execute(text(f'DROP DATABASE "{name}" WITH (FORCE)'))
        admin.dispose()
