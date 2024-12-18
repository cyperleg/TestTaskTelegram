import asyncio
import os
from telethon.sync import TelegramClient
from app.schemas import User, APITelegram, DialogSchema, APICode
from typing import Optional, Callable
from telethon.helpers import TotalList
from telegram.schemas import FilterBy, TypeBy, APIException, AuthException
from telethon.errors.rpcerrorlist import FloodWaitError
from config import SESSION_LOCATION


class TelegramAPI:
    def __init__(self, user: User):
        self.__user = user
        self.__client: Optional[TelegramClient] = None

    def __create_client(self) -> TelegramClient:
        if self.__user.api.api_id is None or self.__user.api.api_hash is None:
            raise ValueError(f"User {self.__user.login} doesn't have api")

        return TelegramClient(f"{SESSION_LOCATION}/session_{self.__user.login}", self.__user.api.api_id, self.__user.api.api_hash)

    async def create_new_session(self):
        filepath = f"{SESSION_LOCATION}/session_{self.__user.login}.session"
        if os.path.exists(filepath):
            os.remove(filepath)

        self.__client = self.__create_client()
        await self.__client.connect()
        try:
            phone_code_hash = await self.__client.send_code_request(phone=self.__user.api.phone_number)
        except FloodWaitError as e:
            raise APIException(f"Telegram API cooldown: {e.message}")
        await self.__client.disconnect()
        return phone_code_hash.phone_code_hash

    async def authorise(self, code: APICode):
        self.__client = self.__create_client()
        await self.__client.connect()
        await self.__client.sign_in(phone=self.__user.api.phone_number, code=code.code,
                                    phone_code_hash=self.__user.hash_phone)
        await self.__client.disconnect()

    async def __get_all(self) -> TotalList:
        self.__client = self.__create_client()
        try:
            print(1)
            await self.__client.connect()
            print(2)
            if await self.__client.is_user_authorized():
                result = await self.__client.get_dialogs()
                await self.__client.disconnect()
                return result
            else:
                raise AuthException("This session is not authorised")
        except AuthException as e:
            raise e
        except Exception:
            raise APIException("Telegram API not responding")

    @staticmethod
    def __filter_by(filter_by: FilterBy) -> Callable:
        def __inner_filter(dialog):
            if filter_by == FilterBy.WATCHED:
                return dialog.unread_count == 0
            if filter_by == FilterBy.UNWATCHED:
                return dialog.unread_count > 0
        return __inner_filter

    async def get_dialogs(self, filter_by: Optional[FilterBy] = FilterBy.UNWATCHED,
                          type_by: Optional[TypeBy] = TypeBy.GROUP) -> list:
        dialogs = await self.__get_all()
        if type_by == TypeBy.GROUP:
            dialogs = [d for d in dialogs if d.is_group]
        if type_by == TypeBy.CHANNEL:
            dialogs = [d for d in dialogs if d.is_channel]
        if type_by == TypeBy.CHAT:
            dialogs = [d for d in dialogs if d.is_user]
        return [DialogSchema(name=x.name, identification=x.id) for x in filter(self.__filter_by(filter_by), dialogs)]


if __name__ == "__main__":
    async def main():
        test_user = User(id=1, login="LOlkekocvich", password="QwertY_11233", hash_phone="42d000510614e19bc6",
                         api=APITelegram(api_id=11,
                                         api_hash="test",
                                         phone_number="test")
                         )

        await TelegramAPI(test_user).create_new_session()
        # for test u need to change realisation, maybe mock function?
        await TelegramAPI(test_user).authorise(APICode(code=int(input("set_code: "))), hash_code=input("set_hash: "))
        res = await TelegramAPI(test_user).get_dialogs(FilterBy.WATCHED, TypeBy.CHAT)

        for i in res:
            print(i)

    asyncio.run(main())
