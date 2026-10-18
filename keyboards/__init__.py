from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from menu_config import get_menu_labels


# Custom-emoji icons for buttons. slot -> (button label, fallback emoji).
ICON_SLOTS = {
    "catalog": ("Каталог", "📁"),
    "withdraw": ("Вывести Gold", "📤"),
    "profile": ("Профиль", "👤"),
    "info": ("Информация", "ℹ️"),
    "buy": ("Купить Gold", "💎"),
    "bonus": ("Бонус", "🪬"),
}
# slot -> custom emoji id; filled at startup and when the admin changes an icon.
ICONS: dict[str, str] = {}


def _label(slot: str) -> tuple[str, dict]:
    """Return (text, extra kwargs). With a custom icon the icon replaces the plain emoji."""
    name, emoji = ICON_SLOTS[slot]
    icon = ICONS.get(slot)
    if icon:
        return name, {"icon_custom_emoji_id": icon}
    return f"{emoji} {name}", {}


def _reply_button(slot: str) -> KeyboardButton:
    text, extra = _label(slot)
    return KeyboardButton(text=text, **extra)


def _inline_button(slot: str, callback_data: str) -> InlineKeyboardButton:
    text, extra = _label(slot)
    return InlineKeyboardButton(text=text, callback_data=callback_data, **extra)


def user_home() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [_reply_button("catalog"), _reply_button("withdraw")],
            [_reply_button("profile")],
            [_reply_button("info")],
        ],
        resize_keyboard=True,
        is_persistent=True,
        input_field_placeholder="Выберите раздел меню",
    )


def admin_home() -> InlineKeyboardMarkup:
    rows = [
        [("📊 Статистика", "adm:stats"), ("👥 Пользователи", "adm:users")],
        [("🛒 Товары", "adm:products"), ("📦 Заказы", "adm:orders")],
        [("💳 Платежи", "adm:payments"), ("🎁 Бонусы", "adm:bonuses")],
        [("🏆 Розыгрыши", "adm:giveaways"), ("📤 Выдача голды", "adm:withdrawals")],
        [("🧩 Задания", "adm:tasks"), ("👥 Рефералы", "adm:referrals")],
        [("📢 Рассылка", "adm:broadcast"), ("⚙️ Настройки", "adm:settings")],
        [("🏪 Магазин", "adm:shop"), ("🎮 Скины", "adm:skins")],
        [("🎨 Значки кнопок", "adm:icons"), ("📜 Журнал действий", "adm:logs")],
    ]
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=label, callback_data=data) for label, data in row]
            for row in rows
        ]
    )


def back_admin() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="← Админ-меню", callback_data="adm:home")]]
    )


def back_user() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="← Главное меню", callback_data="u:home")]]
    )


def catalog_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [_inline_button("buy", "u:buygold")],
            [_inline_button("bonus", "u:claim")],
        ]
    )
