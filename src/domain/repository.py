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
        self._validate(v)
        if v.id == None:
            self.session.add(v)
        else:
            raise ValueError("Already implemented")
    def get(self,id: K)-> V:
        obj=self.session.get(self.model,id)
        if obj:
            return obj
        else:
            print("Id not found")
            return None
    def get_all(self)-> Iterable[V]:
        stmt= select(self.model)
        return self.session.scalars(stmt).all()
    def update(self, v:V) -> None:
        self._validate(v)
        self.session.merge(v)
    def _validate(self, k:K)->None:
        ...

    def delete(self,k:K):
        v= self.get(k)
        try:
            self.session.delete(v)
        except:
            print("can't delete Id out of Rang")

class UserRepository(Repository[int,User]):
    def __init__(self, session:Session):
        super().__init__(session, User)
    def _validate(self, user:User)-> None:
        if user.username is None:
            raise ValueError("User name is mandatory")
    def __repr__(self):
        return f"{self.user}"
    def get_by_username(self, username:str):
        stmt= select(self.model).where(self.model.username == username)
        obj= self.session.scalars(stmt).first()
        if obj:
            return obj
        else:
            print("Username not found")
    def get_by_email(self, email:str):
        stmt = select(self.model).where(self.model.email == email)
        obj = self.session.scalars(stmt).first()
        if obj:
            return obj
        else:
            print("Email not found")
class RoleRepository(Repository[int,Role]):
    def __init__(self, session:Session):
        super().__init__(session, Role)
    def _validate(self, role:Role)->None:
        if role.name is None:
            raise ValueError("Name is mandatory")

class ProfileRepository(Repository[int,Profile]):
    def __init__(self, session:Session):
        super().__init__(session, Profile)
    def _validate(self, profile:Profile)->None:
        if profile.first_name is None:
            raise ValueError("First name is mandatory")
        elif profile.user_id is None:
            raise ValueError("User does not exist")

class PostRepository(Repository[int,Post]):
    def __init__(self, session:Session):
        super().__init__(session,Post)
    def _validate(self, post:Post)->None:
        if post.title is None:
            raise ValueError("Title is mandatory")
    def get_by_category(self,category_id:int)->Iterable[Post]:
        stmt= select(self.model).where(self.model.category_id == category_id)
        return self.session.scalars(stmt).all()
    def get_by_user(self,user_id:int)->Iterable[User]:
        stmt=select(self.model).where(self.model.user_id== user_id)
        return self.session.scalars(stmt).all()
    def get_last(self,limit:int=10)->Iterable[Post]:
        stmt= (select (self.model) .order_by(self.model.creation_date) .limit(limit))
        return self.session.scalars(stmt).all()
    def increment_viewCount(self, post_id:int)->None:
        post=self.get(post_id)
        if post:
            current_view=post.viewCount if post.viewCount is not None else 0
            post.viewCount = current_view + 1
            self.session.add(post)
class CategoryRepository(Repository[int,Category]):
    def __init__(self, session:Session):
        super().__init__(session,Category)
    def _validate(self, category:Category):
        if category.name is None:
            raise ValueError("Name is mandatory")

class TagRepository(Repository[int,Tag]):
    def __init__(self, session:Session):
        super().__init__(session,Tag)
    def _validate(self,post:Post):
        if post.name is None:
            raise ValueError("Name is mandatory")
class PostTagsRepository(Repository[int,PostTags]):
    def __init__(self, session:Session):
        super().__init__(session,PostTags)

        
