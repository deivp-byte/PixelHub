from .db import Session
class UnitOfWork():
    def __init__(self, Session):
      self.session= Session
    def __enter__(self):
      self.session = Session()
      return self

      return self
    def __exit__(self, exc_type, exc, tb):
        if exc is not None:
          self.session.rollback()
          self.session.commit()
        else:
           self.session.commit()
