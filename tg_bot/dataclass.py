from dataclasses import field

from marshmallow import Schema, EXCLUDE, fields
from marshmallow_dataclass import dataclass
from typing import Optional, ClassVar, Type


@dataclass
class MainData:
    class Meta:
        unknown = EXCLUDE


@dataclass
class MessageFrom(MainData):
    id: int
    first_name: str
    last_name: Optional[str]
    username: str


@dataclass
class Chat(MainData):
    id: int
    type: str
    title: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    username: Optional[str]


@dataclass
class Photo(MainData):
    file_id: str
    file_unique_id: str
    width: int
    height: int
    file_size: Optional[int]


@dataclass
class Message(MainData):
    message_id: int
    from_: MessageFrom = field(metadata={"data_key": "from"})
    chat: Chat
    date: int
    text: Optional[str]
    photo: Optional[Photo]
    reply_markup: Optional[dict] = None


@dataclass
class CallbackQuery(MainData):
    id: str
    from_: MessageFrom = field(metadata={"data_key": "from"})
    message: Message
    data: str


@dataclass
class ChatMemberUpd(MainData):
    date: int


@dataclass
class UpdateObject(MainData):
    update_id: Optional[int] = None
    message: Optional[Message] = None
    callback_query: Optional[CallbackQuery] = None
    my_chat_member: Optional[ChatMemberUpd] = None

    Schema: ClassVar[Type[Schema]] = Schema


@dataclass
class GetUpdatesResponse(MainData):
    ok: bool
    result: list[UpdateObject]

    Schema: ClassVar[Type[Schema]] = Schema


@dataclass
class SendMessageResponse(MainData):
    ok: bool
    result: Message

    Schema: ClassVar[Type[Schema]] = Schema


class PostSchema(Schema):
    user = fields.Str()
    slug = fields.Str()
    title = fields.Str()
    content = fields.Str()

    @staticmethod
    def to_dict(post: dict) -> str:
        return (
            f"Автор: {post.get('user')}\n"
            f"Название: {post.get('title')}\n"
            f"Содержание: {post.get('content')}\n"
            f"Ссылка: https://alman-project.ru/{post.get('slug')}\n"
        )
