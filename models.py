from typing import Annotated, Optional
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from typing import Annotated
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase

str_256 = Annotated[str, 256]
intpk = Annotated[int, mapped_column(primary_key=True)]

class Base(DeclarativeBase):
    type_annotation_map = {
        str_256: String(256)
    }

    repr_cols_num = 3
    repr_cols = tuple()
    
    def __repr__(self):
        """Relationships не используются в repr(), т.к. могут вести к неожиданным подгрузкам"""
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_cols_num:
                cols.append(f"{col}={getattr(self, col)}")

        return f"<{self.__class__.__name__} {', '.join(cols)}>"

class User_(Base):
    __tablename__ = "user_"

    id: Mapped[intpk]
    user_id: Mapped[int]
    chat_id: Mapped[int]

class Video(Base):
    __tablename__ = "video"

    id: Mapped[intpk]
    file_id: Mapped[Optional[str_256]]
    video_key: Mapped[str_256]

class Playlist(Base):
    __tablename__ = "playlist"

    id: Mapped[intpk]
    playlist_key: Mapped[str_256]

class Playlist_User(Base):
    __tablename__ = "playlist_user"

    id_playlist: Mapped[int] = mapped_column(
        ForeignKey("playlist.id", ondelete="CASCADE"),
        primary_key=True,
    )
    id_user: Mapped[int] = mapped_column(
        ForeignKey("user_.id", ondelete="CASCADE"),
        primary_key=True,
    )

class Playlist_Video(Base):
    __tablename__ = "playlist_video"

    id_video: Mapped[int] = mapped_column(
        ForeignKey("video.id", ondelete="CASCADE"),
        primary_key=True,
    )
    id_playlist: Mapped[int] = mapped_column(
        ForeignKey("playlist.id", ondelete="CASCADE"),
        primary_key=True,
    )


