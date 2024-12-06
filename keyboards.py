from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
start_kb = ReplyKeyboardMarkup(
            [
                [KeyboardButton(text = 'Цена'),
                KeyboardButton(text = 'О магазине')]
    ], resize_keyboard=True
)

catalog_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Оберег Успешница',callback_data ='Успешница')],
        [InlineKeyboardButton(text='Оберег Подорожница',callback_data ='Подорожница')],
        [InlineKeyboardButton(text='Оберег Ведучка',callback_data ='Ведучка')],
        [InlineKeyboardButton(text='Другие обереги',callback_data ='Другие')]
    ]
)
buy_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Купить куклу", callback_data = "http://ya.ru")]
    ]
)