from aiogram.types import Message, ContentType, CallbackQuery, ChatType
from aiogram.dispatcher.filters import Command, ChatTypeFilter

from main import bot,dp
from services import DataBase
from keyboards import adminpanel_kb, adminpanel_menu_kb, adminpanel_cancel_kb



db = DataBase()

admins = list(db.get_admins())


async def getMessageLinks():
    result = "Черный список ссылок\n"
    links = await db.get_links()
    for item in links:
        result +=f"{item[0]} : {item[1]}\n"
    return result

async def getMessageGroup():
    result = "Список групп, обрабатываемые ботом\n"
    groups = await db.get_group()
    for item in groups:
        result +=f"{item[0]} : {item[1]}\n"
    return result

@dp.message_handler(Command('adminpanel'))
async def start(message: Message):
    try:
        if(message.from_id in admins):
            await bot.send_message(message.chat.id, f'Вы успешно авторизовались, {message.chat.full_name}', reply_markup= adminpanel_kb)
            await db.set_stateid(message.from_id,0)
        else:
            await bot.send_message(message.chat.id, "Вы не являетесь администратором!")
    except Exception as e:
        pass

@dp.message_handler(ChatTypeFilter(chat_type=ChatType.PRIVATE), content_types=ContentType.TEXT)
async def state(message: Message):
    if(message.from_id in admins):
            stateid = await db.get_stateid(message.from_id)
            if(stateid == 1):
                try:
                    await db.add_links(message.text)
                    await bot.send_message(message.from_id, f"Ссылка: {message.text}\nуспешно добавлена.", reply_markup=adminpanel_menu_kb)
                except Exception as e:
                    await bot.send_message(message.from_id, "Произошла ошибка [добавление ссылки]: " + e, reply_markup=adminpanel_menu_kb)
                finally:
                    await db.set_stateid(message.from_id, 0)
            elif(stateid == 2):
                if(message.text.isdigit()):
                    try:
                        await db.del_link(int(message.text))
                        await bot.send_message(message.from_id, f"Ссылка под номером: {message.text}\nуспешно удалена.", reply_markup=adminpanel_menu_kb)
                    except Exception as e:
                        await bot.send_message(message.from_id, "Произошла ошибка [удаление ссылки]: " + e, reply_markup=adminpanel_menu_kb)
                    finally:
                        await db.set_stateid(message.from_id, 0)
                else:
                    await bot.send_message(message.from_id, message.text + " не являеться номером ссылки, попробуйте снова.")
            elif(stateid == 3):
                try:
                    await db.add_group(message.text)
                    await bot.send_message(message.from_id, f"Группа: {message.text}\nуспешно добавлена.", reply_markup=adminpanel_menu_kb)
                except Exception as e:
                    await bot.send_message(message.from_id, "Произошла ошибка [добавление группы]: " + e, reply_markup=adminpanel_menu_kb)
                finally:
                    await db.set_stateid(message.from_id, 0)
            elif(stateid == 4):
                if(message.text.isdigit()):
                    try:
                        await db.del_group(int(message.text))
                        await bot.send_message(message.from_id, f"Группа под номером: {message.text}\nуспешно удалена.", reply_markup=adminpanel_menu_kb)
                    except Exception as e:
                        await bot.send_message(message.from_id, "Произошла ошибка [удаление группы]: " + e, reply_markup=adminpanel_menu_kb)
                    finally:
                        await db.set_stateid(message.from_id, 0)
                else:
                    await bot.send_message(message.from_id, message.text + " не являеться номером группы, попробуйте снова.")

@dp.callback_query_handler(text="add_link")
async def add_link(call: CallbackQuery):
    chatid=call.from_user.id
    if(chatid in admins):
      await call.message.delete()
      await db.set_stateid(chatid, 1)
      links_str = await getMessageLinks()
      await bot.send_message(chatid ,links_str+"\nВведите ссылку, которую нужно добавить в черный список.", reply_markup=adminpanel_cancel_kb)

@dp.callback_query_handler(text="del_link")
async def add_link(call: CallbackQuery):
    chatid=call.from_user.id
    if(chatid in admins):
      await call.message.delete()
      await db.set_stateid(chatid, 2)
      links_str = await getMessageLinks()
      await bot.send_message(chatid ,links_str+"\nВведите номер ссылки, которую нужно убрать из черного списка.", reply_markup=adminpanel_cancel_kb)

@dp.callback_query_handler(text="add_group")
async def add_link(call: CallbackQuery):
    chatid=call.from_user.id
    if(chatid in admins):
      await call.message.delete()
      await db.set_stateid(chatid, 3)
      groups_str = await getMessageGroup()
      await bot.send_message(chatid ,groups_str+"\nВведите username группы, которую нужно добавить в обработку.\nБез @, например group_username. Так-же не забудьте добавить бота в администраторы группы (права удаление, управление видеочатами)", reply_markup=adminpanel_cancel_kb)

@dp.callback_query_handler(text="del_group")
async def add_link(call: CallbackQuery):
    chatid=call.from_user.id
    if(chatid in admins):
      await call.message.delete()
      await db.set_stateid(chatid, 4)
      groups_str = await getMessageGroup()
      await bot.send_message(chatid ,groups_str+"\nВведите номер группы, которую нужно удалить из обработки.", reply_markup=adminpanel_cancel_kb)

@dp.callback_query_handler(text="cancel")
async def cancel(call: CallbackQuery):
    chatid=call.from_user.id
    if(chatid in admins):
        await call.message.delete()
        await db.set_stateid(chatid, 0)
        await bot.send_message(chatid, "Меню\nВыберите нужную кнопку.", reply_markup=adminpanel_kb)

@dp.callback_query_handler(text="menu")
async def cancel(call: CallbackQuery):
    chatid=call.from_user.id
    if(chatid in admins):
        await call.message.delete()
        await bot.send_message(chatid, "Меню\nВыберите нужную кнопку.", reply_markup=adminpanel_kb)