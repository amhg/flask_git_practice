from app.model.config import db_session
from contextlib import contextmanager

@contextmanager
def get_repo_provider(repo_class):
    with db_session() as sess:
        with sess.begin():
            yield repo_class(sess)