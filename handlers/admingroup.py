from aiogram.types import Message, ContentType, CallbackQuery, ChatType
from aiogram.dispatcher.filters import Command, ChatTypeFilter, BoundFilter
from main import bot,dp
from services import DataBase

db = DataBase()

class IsGroup(BoundFilter):
    async def check(self, message: Message) -> bool:
        return message.chat.type in (
            ChatType.SUPERGROUP,
        )
    
class IsOurGroup(BoundFilter):
    async def check(self, message: Message) -> bool:
        return message.chat.username in await db.get_only_groups()


def is_part_in_list(str_, words):
    for word in words:
        if word[0].lower() in str_.lower():
            return True
    return False

async def GetGroupAdmins(chatid_group):
    result = []
    admins = await bot.get_chat_administrators(chatid_group)
    for a in admins:
        result.append(a.user.id)
    return result

@dp.message_handler(IsGroup(), IsOurGroup(), content_types=[ContentType.PHOTO, ContentType.TEXT, ContentType.VIDEO, ContentType.DOCUMENT])
async def checklink (message:Message):
    if(message.from_id in await GetGroupAdmins(message.chat.id)):
        return
    #if (message.entities or message.caption_entities):
    black_links = await db.get_only_links()
    if(is_part_in_list(message.html_text, black_links) ):
        await bot.delete_message(message.chat.id, message.message_id)

@dp.edited_message_handler(IsGroup(), IsOurGroup(), content_types=[ContentType.PHOTO, ContentType.TEXT, ContentType.VIDEO, ContentType.DOCUMENT])
async def checklink (message:Message):
    if(message.from_id in await GetGroupAdmins(message.chat.id)):
        return
    #if (message.entities or message.caption_entities):
    black_links = await db.get_only_links()
    if(is_part_in_list(message.html_text, black_links) ):
        await bot.delete_message(message.chat.id, message.message_id)
    

