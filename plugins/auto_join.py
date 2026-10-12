"""
AuraBeats - Auto Join Assistant
Author: Sakil Anowar (@YO_UR_OFFICIAL_CRUSH)
"""
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ChatMemberStatus, ParseMode
from pyrogram.errors import (
    UserAlreadyParticipant,
    ChatAdminRequired,
    UserNotParticipant,
    PeerIdInvalid,
    ChannelInvalid,
)
from config import config, logger


async def is_assistant_in_chat(client: Client, chat_id: int) -> bool:
    """Check if assistant is already a member"""
    try:
        from core import get_calls_manager
        assistant = get_calls_manager().assistant
        if not assistant:
            return False
        me = await assistant.get_me()
        member = await client.get_chat_member(chat_id, me.id)
        return member.status in (
            ChatMemberStatus.MEMBER,
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.OWNER,
        )
    except UserNotParticipant:
        return False
    except Exception as e:
        logger.debug(f"is_assistant check: {e}")
        return False


async def add_assistant_to_chat(client: Client, chat_id: int) -> bool:
    """
    Add assistant to a chat. Tries multiple methods:
    1. Direct add (bot must be admin with Add Users permission)
    2. Create invite link + assistant joins
    Returns True if assistant is in chat after this call.
    """
    try:
        from core import get_calls_manager
        assistant = get_calls_manager().assistant
        if not assistant:
            logger.warning("Assistant not initialized")
            return False

        me = await assistant.get_me()

        # Already member?
        if await is_assistant_in_chat(client, chat_id):
            logger.info(f"✓ Assistant already in {chat_id}")
            return True

        # Method 1: Direct add
        try:
            await client.add_chat_members(chat_id, me.id)
            logger.success(f"✅ Assistant ADDED to {chat_id}")
            return True
        except UserAlreadyParticipant:
            return True
        except ChatAdminRequired:
            logger.warning(f"⚠️ Bot not admin in {chat_id} — trying invite link")
        except Exception as e:
            logger.debug(f"Direct add failed: {e}")

        # Method 2: Create invite link and join
        try:
            invite = await client.create_chat_invite_link(
                chat_id=chat_id,
                member_limit=1,
                name=f"AuraBeats Auto Invite",
            )
            try:
                await assistant.join_chat(invite.invite_link)
                logger.success(f"✅ Assistant JOINED via invite to {chat_id}")
                return True
            except UserAlreadyParticipant:
                return True
            finally:
                try:
                    await client.revoke_chat_invite_link(chat_id, invite.invite_link)
                except Exception:
                    pass
        except ChatAdminRequired:
            logger.warning(f"⚠️ Bot cannot create invite link in {chat_id}")
        except Exception as e:
            logger.debug(f"Invite method failed: {e}")

        return False

    except Exception as e:
        logger.exception(f"add_assistant_to_chat error: {e}")
        return False


# ═══════════════════════════════════════
#   TRIGGER 1: Bot added to group
# ═══════════════════════════════════════
@Client.on_message(filters.new_chat_members)
async def on_bot_added(client: Client, message: Message):
    """When bot is added to a new group, add assistant too"""
    try:
        me = await client.get_me()
        added_bots = [
            m for m in message.new_chat_members
            if m.is_bot and m.id == me.id
        ]
        if not added_bots:
            return

        chat = message.chat
        logger.info(f"🎉 Bot added to: {chat.title} ({chat.id})")

        # Attempt assistant add
        success = await add_assistant_to_chat(client, chat.id)

        if success:
            text = (
                f"<b>✨  AuraBeats  •  Ready!</b>\n\n"
                f"🎧  Music bot is active in this group.\n"
                f"🤖  Assistant joined successfully.\n\n"
                f"<b>🚀  Get Started</b>\n"
                f"◦ <code>/play song</code> — play music\n"
                f"◦ <code>/help</code> — all commands\n\n"
                f"<i>⚠️ Start a voice chat first!</i>"
            )
        else:
            text = (
                f"<b>⚠️  AuraBeats  •  Setup Needed</b>\n\n"
                f"Bot is here but couldn't add assistant.\n\n"
                f"<b>To fix:</b>\n"
                f"1️⃣  Make <b>@AuraBeatsOfficialBot</b> admin\n"
                f"2️⃣  Enable <b>Add Users</b> permission\n"
                f"3️⃣  Send <code>/addassistant</code> to retry"
            )

        try:
            await client.send_message(
                chat.id, text, parse_mode=ParseMode.HTML
            )
        except Exception as e:
            logger.debug(f"Welcome message failed: {e}")

    except Exception as e:
        logger.exception(f"on_bot_added: {e}")


# ═══════════════════════════════════════
#   TRIGGER 2: /addassistant command
# ═══════════════════════════════════════
@Client.on_message(filters.command("addassistant"))
async def add_assistant_cmd(client: Client, message: Message):
    """Manually trigger assistant add"""
    msg = await message.reply_text("⏳ Adding assistant...")

    success = await add_assistant_to_chat(client, message.chat.id)

    if success:
        await msg.edit_text(
            "<b>✅  Assistant added successfully!</b>\n\n"
            "Now you can play music in voice chat.",
            parse_mode=ParseMode.HTML,
        )
    else:
        await msg.edit_text(
            "<b>❌  Failed to add assistant</b>\n\n"
            "<b>Requirements:</b>\n"
            "1️⃣  Bot must be <b>admin</b> in this group\n"
            "2️⃣  Bot must have <b>Add Users</b> permission\n\n"
            "<i>After enabling, send</i> <code>/addassistant</code> <i>again.</i>",
            parse_mode=ParseMode.HTML,
        )


# ═══════════════════════════════════════
#   TRIGGER 3: /assistant status
# ═══════════════════════════════════════
@Client.on_message(filters.command("assistant"))
async def assistant_status(client: Client, message: Message):
    """Check assistant status"""
    try:
        from core import get_calls_manager
        assistant = get_calls_manager().assistant
        if not assistant:
            return await message.reply_text("❌ Assistant not initialized")

        me = await assistant.get_me()
        in_chat = await is_assistant_in_chat(client, message.chat.id)

        status = "✅ <b>In Group</b>" if in_chat else "❌ <b>Not in Group</b>"

        await message.reply_text(
            f"<b>🤖  Assistant Status</b>\n\n"
            f"👤  <b>Name:</b> {me.first_name}\n"
            f"📱  <b>Username:</b> @{me.username}\n"
            f"🆔  <b>ID:</b> <code>{me.id}</code>\n"
            f"📌  <b>Status:</b> {status}",
            parse_mode=ParseMode.HTML,
        )
    except Exception as e:
        await message.reply_text(f"❌ Error: {e}")
