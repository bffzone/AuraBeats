"""
# Watermark: @AuraBeatsOfficial | @Vip_Sakil_Bio
AuraBeats - Button Factory
Author: Sakil Anowar (@YO_UR_OFFICIAL_CRUSH)
"""

from pyrogram.types import InlineKeyboardButton


def btn(text: str, callback_data: str, **kwargs) -> InlineKeyboardButton:
    """Create a callback button"""
    return InlineKeyboardButton(text, callback_data=callback_data, **kwargs)


def btn_url(text: str, url: str) -> InlineKeyboardButton:
    """Create a URL button"""
    return InlineKeyboardButton(text, url=url)


def btn_switch(text: str, query: str) -> InlineKeyboardButton:
    """Create a switch inline query button"""
    return InlineKeyboardButton(text, switch_inline_query=query)


def btn_switch_current(text: str, query: str = "") -> InlineKeyboardButton:
    """Switch inline query in current chat"""
    return InlineKeyboardButton(text, switch_inline_query_current_chat=query)
