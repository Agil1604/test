import asyncio
import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import select, delete
from models import User_, Video, Playlist, Playlist_User, Playlist_Video, Base
from dotenv import load_dotenv

class DB:
    @staticmethod
    async def create_tables():
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    @staticmethod
    async def select_users():
        async with async_session_factory() as session:
            query = select(User_)
            result = await session.execute(query)
            users = result.scalars().all()

        return users

    @staticmethod
    async def select_videos():
        async with async_session_factory() as session:
            query = select(Video)
            result = await session.execute(query)
            videos = result.scalars().all()
        
        return videos
                
    @staticmethod
    async def add_user(user: int, chat: int):
        async with async_session_factory() as session:
            new_user = User_(user_id = user, chat_id = chat)
            session.add(new_user)
            await session.flush()
            await session.commit()
    
    @staticmethod
    async def add_video(video, file = None):
        async with async_session_factory() as session:
            new_video = Video(video_key = video, file_id = file)
            session.add(new_video)
            await session.flush()
            await session.commit()
    
    @staticmethod
    async def add_playlist_user(user_id, playlist_id):
        async with async_session_factory() as session:
            new_playlist_user = Playlist_User(id_playlist = playlist_id, id_user = user_id)
            session.add(new_playlist_user)
            await session.flush()
            await session.commit()

    @staticmethod
    async def add_playlist_video(video_id, playlist_id):
        async with async_session_factory() as session:
            new_playlist_video = Playlist_Video(id_playlist = playlist_id, id_video = video_id)
            session.add(new_playlist_video)
            await session.flush()
            await session.commit()

    @staticmethod
    async def add_playlist(name):
        async with async_session_factory() as session:
            new_playlist = Playlist(playlist_key = name)
            session.add(new_playlist)
            await session.flush()
            await session.commit()

    @staticmethod
    async def get_subscribed_users(playlist_id):
        async with async_session_factory() as session:
            query = (select(Playlist_User.id_user).select_from(Playlist_User)).where(Playlist_User.id_playlist == playlist_id)
            result = await session.execute(query)
            users = result.scalars().all()
            for i in users:
                print(i)
            # print(f"{users=}")
    
    @staticmethod
    async def get_all_videos(playlist_id):
        async with async_session_factory() as session:
            query = (select(Playlist_Video.id_video).select_from(Playlist_Video)).where(Playlist_Video.id_playlist == playlist_id)
            result = await session.execute(query)
            users = result.scalars().all()
            for i in users:
                print(i)
            # print(f"{users=}")
    
    @staticmethod
    async def delete_user(user, chat):
        async with async_session_factory() as session:
            query = (delete(User_).where(User_.user_id == user).where(User_.chat_id == chat))
            await session.execute(query)
            await session.flush()
            await session.commit()

    @staticmethod
    async def delete_video(video):
        async with async_session_factory() as session:
            query = (delete(Video).where(Video.video_key == video))
            await session.execute(query)
            await session.flush()
            await session.commit()


    @staticmethod
    async def delete_playlist(key):
        async with async_session_factory() as session:
            query = (delete(Playlist).where(Playlist.playlist_key == key))
            await session.execute(query)
            await session.flush()
            await session.commit()

    @staticmethod
    async def get_id_of_user(user, chat):
        async with async_session_factory() as session:
            query = (select(User_.id).select_from(User_)).where(User_.user_id == user).where(User_.chat_id == chat)
            result = await session.execute(query)
            users = result.scalars().all()
            for i in users:
                print(i)
    
    @staticmethod
    async def get_id_of_video(video):
        async with async_session_factory() as session:
            query = (select(Video.id).select_from(Video)).where(Video.video_key == video)
            result = await session.execute(query)
            videos = result.scalars().all()
            for i in videos:
                print(i)
    

    @staticmethod
    async def get_id_of_playlist(name):
        async with async_session_factory() as session:
            query = (select(Playlist.id).select_from(Playlist)).where(Playlist.playlist_key == name)
            result = await session.execute(query)
            playlists = result.scalars().all()
            for i in playlists:
                print(i)
    
    @staticmethod
    async def delete_playlist_video(playlist, video):
        async with async_session_factory() as session:
            query = (delete(Playlist_Video).where(Playlist_Video.id_video == video).where(Playlist_Video.id_playlist == playlist))
            await session.execute(query)
            await session.flush()
            await session.commit()

    @staticmethod
    async def delete_playlist_user(playlist, user):
        async with async_session_factory() as session:
            query = (delete(Playlist_User).where(Playlist_User.id_user == user).where(Playlist_User.id_playlist == playlist))
            await session.execute(query)
            await session.flush()
            await session.commit()

    @staticmethod
    async def update_playlist(id: int, new_name: str):
        async with async_session_factory() as session:
            changable = await session.get(Playlist, id)
            changable.playlist_key = new_name
            await session.commit()

    @staticmethod
    async def update_video(id: int, new_file_id: str, new_video_key: str):
        async with async_session_factory() as session:
            changable = await session.get(Video, id)
            changable.file_id = new_file_id
            changable.video_key = new_video_key
            await session.commit()
    
    @staticmethod
    async def get_video(id: int):
        async with async_session_factory() as session:
            target = await session.get(Video, id)

        return target

    @staticmethod
    async def get_user(id: int):
        async with async_session_factory() as session:
            target = await session.get(User_, id)

        return target

    @staticmethod
    async def get_playlist(id: int):
        async with async_session_factory() as session:
            target = await session.get(Playlist, id)

        return target


if __name__ == '__main__':
    load_dotenv()
    db_host = os.getenv('DB_HOST')
    db_port = os.getenv('DB_PORT')
    db_user = os.getenv('DB_USER')
    db_pass = os.getenv('DB_PASS')
    db_name = os.getenv('DB_NAME')

    async_engine = create_async_engine(
    url = f"postgresql+asyncpg://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}",
    echo=False,
    )
    async_session_factory = async_sessionmaker(async_engine)

