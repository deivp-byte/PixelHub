from sqlalchemy import create_engine, String, Integer, Date, select, Boolean, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker, Session, relationship
from datetime import date
from typing import Optional,List


from .db import Base, engine


class Role(Base):
    __tablename__ = "rol"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(200))
    last_update:Mapped[date] =mapped_column(Date,default=date.today,onupdate=date.today,nullable=True)

    
class User(Base):
    __tablename__="user"
    def __repr__(self):
        return f"id:{self.id} username:{self.username} email:{self.email} created at: {self.created_at}"
    id: Mapped[int]= mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50),nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(100), nullable=True)
    created_at: Mapped[date] = mapped_column(Date, default=date.today,nullable=False)
    role_id: Mapped[int] = mapped_column(Integer, ForeignKey("rol.id"), nullable=False)
    last_update:Mapped[date] =mapped_column(Date,default=date.today,onupdate=date.today,nullable=True)

    role: Mapped[Role] = relationship("Role", backref="user") 

class Profile(Base):
    __tablename__="profile"
    id: Mapped[int]= mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id",ondelete="CASCADE"), unique=True, nullable=False)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    bio: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    avatar_url: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    phone_number: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    location: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    birth_date: Mapped[date] = mapped_column(Date, nullable=False)
    last_update:Mapped[date] =mapped_column(Date,default=date.today,onupdate=date.today,nullable=True)
    user: Mapped[User] = relationship("User", backref="profile", uselist=False)


class PostTags(Base):
    __tablename__="post_tags"
    post_id: Mapped[int] = mapped_column(Integer, ForeignKey("post.id",ondelete="CASCADE"), nullable=False, primary_key=True)
    tag_id: Mapped[int] = mapped_column(Integer, ForeignKey("tag.id",ondelete="CASCADE"), nullable=False, primary_key=True)
    inserted_on: Mapped[date] = mapped_column(Date,nullable=False)
    relevance_score: Mapped[int] = mapped_column(Integer, default=5)
    last_update:Mapped[date] =mapped_column(Date,default=date.today,onupdate=date.today,nullable=True)
    

class Tag(Base):
    __tablename__="tag"
    id: Mapped[int]= mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    last_update:Mapped[date] =mapped_column(Date,default=date.today,onupdate=date.today,nullable=True)

class Category(Base):
    __tablename__="category"
    id: Mapped[int]= mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    last_update:Mapped[date] =mapped_column(Date,default=date.today,onupdate=date.today,nullable=True)

class Post(Base):
    __tablename__="post"
    id: Mapped[int]= mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    img: Mapped[str] = mapped_column(String(250), nullable=True)
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey("category.id",ondelete="CASCADE"), nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id",ondelete="CASCADE"), nullable=False)
    content: Mapped[str] = mapped_column(String(500), nullable=False)
    creation_date: Mapped[date] = mapped_column(Date, default=date.today,nullable=False)
    user: Mapped[User] = relationship("User", backref="post")
    viewCount: Mapped[int] = mapped_column(Integer, default=0, nullable=True)
    last_update:Mapped[date] =mapped_column(Date,default=date.today,onupdate=date.today,nullable=True)

    category: Mapped[Category] = relationship("Category", backref="post")


class PostFav(Base):
    __tablename__="post_fav"
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id",ondelete="CASCADE"), nullable=False, primary_key=True)
    post_id: Mapped[int] = mapped_column(Integer, ForeignKey("post.id",ondelete="CASCADE"), nullable=False, primary_key=True)
    last_update:Mapped[date] =mapped_column(Date,default=date.today,onupdate=date.today,nullable=True)
