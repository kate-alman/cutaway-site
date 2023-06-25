import logging
from typing import Optional

import aiohttp

from config import Config
from tg_bot.dataclass import GetUpdatesResponse, SendMessageResponse


class TgClient:
    BASE_URL = "https://api.telegram.org/bot"

    def __init__(self, cfg: Config):
        self.token = cfg.bot.token
        self.logger = logging.getLogger(__name__)

    def get_method_url(self, method: str):
        return f"{self.BASE_URL}{self.token}/{method}"

    async def get_updates(self, offset: Optional[int] = None, timeout: int = 0) -> dict:
        """Receives updates (new messages) from telegram."""
        url = self.get_method_url("getUpdates")
        params = {}
        if offset:
            params["offset"] = offset
        if timeout:
            params["timeout"] = timeout
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as resp:
                return await resp.json()

    async def get_update_objects(
        self, offset: Optional[int] = None, timeout: int = 0
    ) -> GetUpdatesResponse:
        """Deserialize updates."""
        updates = await self.get_updates(offset=offset, timeout=timeout)
        try:
            if updates.get("result"):
                logging.info(updates)
                return GetUpdatesResponse.Schema().load(updates)
        except ValueError as e:
            logging.error(f"Failed to load schema {e}")

    async def send_message(
        self, chat_id: int, text: str, force_reply: bool = False
    ) -> SendMessageResponse:
        """Method to send message to user."""
        url = self.get_method_url("sendMessage")
        payload = {
            "chat_id": chat_id,
            "text": text,
            "reply_markup": {"force_reply": force_reply, "selective": True},
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as resp:
                res_dict = await resp.json()
                return SendMessageResponse.Schema().load(res_dict)

    async def send_keyboard(
        self, chat_id: int, text: str = "Click", keyboard: Optional[dict] = None
    ) -> SendMessageResponse:
        """Method to send keyboard to user."""
        url = self.get_method_url("sendMessage")
        payload = {"chat_id": chat_id, "text": text, "reply_markup": keyboard}
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as resp:
                json_res = await resp.json()
                return SendMessageResponse.Schema().load(json_res)

    async def remove_inline_keyboard(
        self, message_id: int, chat_id: int
    ) -> SendMessageResponse:
        """Method to remove keyboard from user."""
        url = self.get_method_url("editMessageReplyMarkup")
        payload = {
            "chat_id": chat_id,
            "message_id": message_id,
            "keyboard": {"inline_keyboard": None},
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as resp:
                json_res = await resp.json()
                return SendMessageResponse.Schema().load(json_res)
