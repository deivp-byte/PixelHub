from .db import Session
from .models import User,Profile,Role,PostTags,Tag,Category,Post,PostFav,select
from sqlalchemy import inspect
from typing import Generic, TypeVar, Iterable, Type

V = TypeVar("V")
K = TypeVar("K")
class Repository(Generic[K,V]):
    def __init__(self,session:Session, model: Type[V]):
        self.session = session
        self.model=model
    def save(self, v:V):
        # self._validate(v)
        if v.id == None:
            self.session.add(v)
        else:
            raise ValueError("Not implemented yet")
    def get(self,id: K)-> V:
        return self.session.get(self.model,id)
    def get_all(self)-> Iterable[V]:
        stmt= select(self.model)
        return self.session.scalars(stmt).all()
    def update(self, v:V) -> None:
        self._validate(v)
        status = inspect(v)
        if not status.persistent:
            self.session.merge(v)
        else:
            raise ValueError("Not Correct Update")
    def _validate(self, k:K)->None:
        ...

    def delete(self,k:K):
        v= self.get(k)
        if v is None:
            raise ValueError(f"User does not exist")
        # self._validate(v)
        self.session.delete(v)

class UserRepository(Repository[int,User]):
    def __init__(self, session:Session):
        super().__init__(session, User)
    def _validate(self, user:User)-> None:
        if user.username is None:
            raise ValueError("User name is mandatory")
        elif user.id is None:
            raise ValueError("User does not exist")
    def __repr__(self):
        return f"{self.user}"
    
# hacer validacion del update control errores
        
