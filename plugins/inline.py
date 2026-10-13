"""
# Watermark: @AuraBeatsOfficial | @Vip_Sakil_Bio
AuraBeats - Inline Query Handler
Author: Sakil Anowar (@YO_UR_OFFICIAL_CRUSH)
"""

from pyrogram import Client
from pyrogram.types import (
    InlineQuery,
    InlineQueryResultArticle,
    InputTextMessageContent,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from config import config, VISIBLE_CREDIT, AUTHOR_TG_LINK


@Client.on_inline_query()
async def inline_handler(client: Client, query: InlineQuery):
    text = query.query.strip()
    if not text:
        return await query.answer([], cache_time=0)
    
    try:
        from services import search_multiple
        results = search_multiple(text, limit=5)
    except Exception:
        results = []
    
    if not results:
        return await query.answer(
            [
                InlineQueryResultArticle(
                    title="No results",
                    description=f"Nothing found for '{text}'",
                    input_message_content=InputTextMessageContent(
                        "😕 Koi result nahi mila."
                    ),
                )
            ],
            cache_time=0,
        )
    
    answers = []
    for r in results:
        title = r["title"][:60]
        desc = f"👤 {r['artist']} | ⏱️ {r['duration']}s"
        answers.append(
            InlineQueryResultArticle(
                title=title,
                description=desc,
                thumb_url=r.get("thumbnail"),
                input_message_content=InputTextMessageContent(
                    f"🎵 **{title}**\n"
                    f"👤 {r['artist']}\n"
                    f"🔗 {r['url']}\n\n"
                    f"{VISIBLE_CREDIT}"
                ),
            )
        )
    
    await query.answer(answers, cache_time=10)
