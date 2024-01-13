from os import getenv
from googleapiclient.discovery import build


class Video:
    """
    Класс для ютуб-видео.
    """
    api_key = getenv('YT_API_KEY')

    def __init__(self, video_id) -> None:
        """
        Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API.
        """
        self.video_id = video_id
        self.video = Video.get_service().videos().list(
            id=self.video_id, part="snippet,contentDetails,statistics").execute()
        self.title = self.video["items"][0]["snippet"]["title"]
        self.url = f"https://www.youtube.com/watch?v={self.video['items'][0]['id']}"
        self.view_count = self.video["items"][0]["statistics"]["viewCount"]
        self.likes_count = self.video["items"][0]["statistics"]["likeCount"]

    @classmethod
    def get_service(cls):
        """
        Возвращает объект для работы с YouTube API
        """
        youtube = build('youtube', 'v3', developerKey=cls.api_key)
        return youtube

    def __str__(self):
        return self.title


class PLVideo(Video):
    """Второй класс для видео."""
    def __init__(self, video_id, playlist_id) -> None:
        """
        Экземпляр инициализируется id видео и id плейлиста.
        """
        super().__init__(video_id)
        self.playlist_id = playlist_id
