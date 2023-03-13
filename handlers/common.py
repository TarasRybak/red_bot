from aiogram import Router
from aiogram.filters.command import Command
from aiogram.filters.text import Text
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="Welcome to the flashcard bot! To start a quiz, type /quiz. "
             "To create a flashcard, type /addflashcard. To view your progress, type /progress.",
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
