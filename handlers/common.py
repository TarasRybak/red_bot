from aiogram import Router
from aiogram.filters.command import Command
from aiogram.filters.text import Text
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from handlers.flashcards import user_progress, flashcards
from keyboards import localization_manager

router = Router()
user_conf = {}


@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    complex_id = state.key
    default_user_lang = message.from_user.language_code
    user_language = await localization_manager.get_user_language(complex_id, default_user_lang)
    hello_message = await localization_manager.get_localized_message(complex_id, "hello")

    await message.answer(
        text=hello_message,
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(Command("cancel"))
@router.message(Text(text="cancel", ignore_case=True))
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="cancel process",
        reply_markup=ReplyKeyboardRemove()
    )


# Define a command handler for the "/progress" command
@router.message(Command("progress"))
async def view_progress(message: Message, state: FSMContext):
    # Retrieve the user's progress data
    if message.from_user.id not in user_progress:
        progress_mess_not = await localization_manager.get_localized_message(state.key, "progress_mess_not")
        await message.reply(progress_mess_not)
    else:
        progress = user_progress[message.from_user.id]
        num_learned = sum(progress.values())
        total = len(flashcards)
        percent = round(num_learned / total * 100)
        # await message.reply(f"You have learned {num_learned} out of {total} flashcards ({percent}%).")
        progress_mess = await localization_manager.get_localized_message(state.key, "progress_mess", num_learned, total, percent)
        await message.answer(text=progress_mess)#f"You have learned {num_learned} out of {total} flashcards ({percent}%).")
