"""
Helper functions for safe message operations
"""

import logging
from typing import Optional
from aiogram.types import Message, InlineKeyboardMarkup
from aiogram.exceptions import TelegramBadRequest

logger = logging.getLogger(__name__)


async def safe_edit_message(
    message: Message,
    text: str,
    parse_mode: Optional[str] = None,
    reply_markup: Optional[InlineKeyboardMarkup] = None,
    send_new_on_fail: bool = False
) -> Optional[Message]:
    """
    Safely edit a message with error handling for TelegramBadRequest.
    
    Args:
        message: The message to edit
        text: New text for the message
        parse_mode: Parse mode (HTML, Markdown, etc.)
        reply_markup: New reply markup (can be None to remove)
        send_new_on_fail: If True, send a new message if editing fails
        
    Returns:
        The edited message or new message if sent, None if operation failed
    """
    try:
        return await message.edit_text(
            text=text,
            parse_mode=parse_mode,
            reply_markup=reply_markup
        )
    except TelegramBadRequest as e:
        error_msg = str(e)
        logger.warning(f"Failed to edit message: {error_msg}")
        
        if "message is not modified" in error_msg.lower():
            logger.debug("Message content is identical to current content, skipping edit")
            return message
        elif "message can't be edited" in error_msg.lower():
            logger.debug("Message can't be edited (too old or deleted)")
            if send_new_on_fail:
                try:
                    return await message.answer(
                        text=text,
                        parse_mode=parse_mode,
                        reply_markup=reply_markup
                    )
                except Exception as new_msg_error:
                    logger.error(f"Failed to send new message: {new_msg_error}")
                    return None
        elif "message to edit not found" in error_msg.lower():
            logger.debug("Message was deleted or not found")
            if send_new_on_fail:
                try:
                    return await message.answer(
                        text=text,
                        parse_mode=parse_mode,
                        reply_markup=reply_markup
                    )
                except Exception as new_msg_error:
                    logger.error(f"Failed to send new message: {new_msg_error}")
                    return None
        else:
            logger.error(f"Unexpected TelegramBadRequest: {error_msg}")
            
        return None
    except Exception as e:
        logger.error(f"Unexpected error while editing message: {e}")
        return None


async def safe_delete_message(message: Message) -> bool:
    """
    Safely delete a message with error handling.
    
    Args:
        message: The message to delete
        
    Returns:
        True if deletion was successful, False otherwise
    """
    try:
        await message.delete()
        return True
    except TelegramBadRequest as e:
        logger.warning(f"Failed to delete message: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error while deleting message: {e}")
        return False
