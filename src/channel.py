from json import dumps, dump
from os import getenv
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""
    api_key = getenv('YT_API_KEY')

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.channel = Channel.get_service().channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        self.title = self.channel['items'][0]['snippet']['title']
        self.description = self.channel['items'][0]['snippet']['description']
        self.subscriber_count = self.channel['items'][0]['statistics']['subscriberCount']
        self.view_count = self.channel['items'][0]['statistics']['viewCount']
        self.video_count = self.channel['items'][0]['statistics']['videoCount']
        self.url = f"https://www.youtube.com/channel/{self.channel['items'][0]['id']}"
        # self.url = f"https://www.youtube.com/channel/{self.channel['items'][0]['snippet']['customUrl']}"

    @property
    def channel_id(self):
        """Геттер для возврата значения приватного атрибута chanel_id"""
        return self.__channel_id

    @classmethod
    def get_service(cls):
        """Возвращает объект для работы с YouTube API"""
        youtube = build('youtube', 'v3', developerKey=cls.api_key)
        return youtube

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(dumps(self.channel, indent=2, ensure_ascii=False))

    def to_json(self):
        """Сохраняет в файл значения атрибутов экземпляра Channel"""
        result = {
            'id': self.__channel_id,
            'title': self.title,
            'description': self.description,
            'url': self.url,
            'subscriber_count': self.subscriber_count,
            'video_count': self.video_count,
            'view_count': self.view_count
        }
        with open("moscowpython.json", "w", encoding="UTF-8") as file:
            dump(result, file, indent=2)
