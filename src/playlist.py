from datetime import timedelta
from os import getenv
from googleapiclient.discovery import build


class PlayList:
    """
    Класс для ютуб-плейлиста.
    """
    api_key = getenv('YT_API_KEY')

    def __init__(self, id_playlist):
        """
        Экземпляр инициализируется id плейлиста. Дальше все данные будут подтягиваться по API.
        """
        self.id_playlist = id_playlist
        self.playlist = PlayList.get_service().playlists().list(
            part="snippet", id=self.id_playlist).execute()
        self.title = self.playlist['items'][0]['snippet']['title']
        self.url = f"https://www.youtube.com/playlist?list={self.id_playlist}"

    @classmethod
    def get_service(cls):
        """
        Возвращает объект для работы с YouTube API
        """
        youtube = build('youtube', 'v3', developerKey=cls.api_key)
        return youtube

    @property
    def total_duration(self) -> timedelta:
        """
        Возвращает объект класса datetime.timedelta с суммарной длительность плейлиста.
        """
        videos = PlayList.get_service().playlistItems().list(
            part="contentDetails", playlistId=self.id_playlist).execute()
        total_duration_seconds = 0
        for video in videos['items']:
            video_id = video['contentDetails']['videoId']
            video_info = PlayList.get_service().videos().list(part="contentDetails", id=video_id).execute()
            duration_str = video_info['items'][0]['contentDetails']['duration']
            duration_data = duration_str[2:].split('M')
            minutes = int(duration_data[0]) if duration_data[0] else 0
            seconds = int(duration_data[1][:-1]) if duration_data[1] else 0
            duration_info = timedelta(minutes=minutes, seconds=seconds)
            total_duration_seconds += duration_info.total_seconds()
        return timedelta(seconds=total_duration_seconds)

    def show_best_video(self):
        """
        Возвращает ссылку на самое популярное видео из плейлиста (по количеству лайков).
        """
        videos = PlayList.get_service().playlistItems().list(
            part="contentDetails", playlistId=self.id_playlist).execute()
        likes_dict = {}
        for video in videos['items']:
            video_id = video['contentDetails']['videoId']
            video_info = PlayList.get_service().videos().list(
                part="snippet,contentDetails,statistics", id=video_id).execute()
            likes = int(video_info['items'][0]['statistics']['likeCount'])
            likes_dict.update({video_id: likes})
        max_pair = max(likes_dict.items(), key=lambda item: item[1])
        return f"https://youtu.be/{max_pair[0]}"
