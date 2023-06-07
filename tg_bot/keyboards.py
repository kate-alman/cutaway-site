START_KEYBOARD = {
    "keyboard": [
        [
            {"text": "📚 Почитать посты"},
            {"text": "🖥 Посмотреть сайт"},
            {"text": "❤️‍🔥 Получить приятность"},
        ]
    ],
    "resize_keyboard": True,
    "one_time_keyboard": False,
    "selective": True,
    "input_field_placeholder": "Что вам показать?",
}

POST_AMOUNT_KEYBOARD = {
    "inline_keyboard": [
        [
            {"text": "1️⃣", "callback_data": "/1"},
            {"text": "3️⃣", "callback_data": "/3"},
            {"text": "5️⃣", "callback_data": "/5"},
            {"text": "🔟", "callback_data": "/10"},
            {"text": "2️⃣0️⃣", "callback_data": "/20"},
        ]
    ],
    "resize_keyboard": True,
    "one_time_keyboard": True,
    "selective": True,
}
