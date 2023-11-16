import datetime
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy import DATE, VARCHAR, Column, Integer, Text, ForeignKey


class Base(DeclarativeBase):
    pass


class UserScheme(Base):
    __tablename__ = "bot_users"

    id = Column(Integer, unique=True, nullable=False, primary_key=True)
    username = Column(VARCHAR(32), unique=False, nullable=True)
    status = Column(VARCHAR(5), unique=False, nullable=False, default="guest")
    reg_date = Column(DATE, default=datetime.datetime.today())

    playlists = relationship("PlaylistSheme", back_populates='user')
    tracks = relationship("TrackSheme", back_populates='user')

class PlaylistSheme(Base):
    __tablename__ = 'playlists'
    
    id = Column(Integer, unique=True, nullable=False, primary_key=True)
    link = Column(Text, unique=False, nullable=False)
    user_id = Column(Integer, ForeignKey('bot_users.id'))
    reg_date = Column(DATE, default=datetime.datetime.today())

    user = relationship('UserSheme', back_populates='playlists')

class TrackSheme(Base):
    __tablename__ = 'tracks'

    id = Column(Integer, nullable=False, unique=True, primary_key=True)
    playlist_id = Column(Integer, ForeignKey('playlists.id'), nullable=True, unique=False)
    user_id = Column(Integer, ForeignKey('bot_users.id'), nullable=False, unique=False)
    track_link = Column(Text, unique=False, nullable=False)
    track_tg_id = Column(Text, unique=False, nullable=False)
    track_thumbnail = Column(Text, unique=False, nullable=False)
    performer = Column(Text, unique=False, nullable=False)
    title = Column(Text, unique=False, nullable=False)
    reg_date = Column(DATE, default=datetime.datetime.today())

    user = relationship('UserSheme', back_populates='tracks')
