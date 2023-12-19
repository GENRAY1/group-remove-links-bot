from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


adminpanel_btn1 = InlineKeyboardButton("Добавить ссылку", callback_data="add_link")
adminpanel_btn2 = InlineKeyboardButton("Удалить ссылку", callback_data="del_link")
adminpanel_btn3 = InlineKeyboardButton("Добавить группу", callback_data="add_group")
adminpanel_btn4 = InlineKeyboardButton("Удалить группу", callback_data="del_group")

adminpanel_kb = InlineKeyboardMarkup()
adminpanel_kb.row(adminpanel_btn1, adminpanel_btn2)
adminpanel_kb.row(adminpanel_btn3, adminpanel_btn4)

adminpanel_menu_btn1 = InlineKeyboardButton("Меню", callback_data="menu")
adminpanel_menu_kb = InlineKeyboardMarkup().add(adminpanel_menu_btn1)


adminpanel_cancel_btn1 = InlineKeyboardButton("Отмена", callback_data="cancel")
adminpanel_cancel_kb = InlineKeyboardMarkup().add(adminpanel_cancel_btn1)