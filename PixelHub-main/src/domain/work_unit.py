from .db import Session
class UnitOfWork():
    def __init__(self, Session):
      self.Session= Session
    def __enter__(self):
      self.Session = Session()

      return self
    def __exit__(self, exc_type, exc, tb):
        if exc is not None:
          self.Session.rollback()
        else:
           self.Session.commit()
