import random

from aiogram import Router
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

router = Router()

# Define the flashcards
flashcards = [
    {"word": "hello", "translation": "hola"},
    {"word": "goodbye", "translation": "adios"},
    {"word": "yes", "translation": "si"},
    {"word": "no", "translation": "no"},
    {"word": "thank you", "translation": "gracias"}
]

# Define a data structure to store the user's progress
user_progress = {}


class QuizState(StatesGroup):
    choosing_1 = State()


class AddState(StatesGroup):
    choosing_1 = State()
    choosing_2 = State()


@router.message(Command("quiz"))
async def quiz(message: Message, state: FSMContext):
    # Choose a random flashcard from the list
    flashcard = random.choice(flashcards)
    flashcard = flashcards[0]
    await state.update_data(chosen_word=flashcard)
    # Ask the user to translate the word
    await message.reply(f"Translate the word <b>{flashcard['word']}</b> into Spanish:")
    await state.set_state(QuizState.choosing_2)


@router.message(QuizState.choosing_2)
async def check_answer(message: Message, state: FSMContext):
    user_data = await state.get_data()
    user_data = user_data["chosen_word"]
    # Check if the user's answer is correct
    if message.text.lower() == user_data["translation"]:
        await message.answer("Correct!")
        global user_progress
        user_progress[message.from_user.id] = {user_data["word"]: True}
        pass
    else:
        await message.answer("Incorrect. Please try again.")
        await quiz(message)  # Ask the user the same question again
    await state.clear()


# Define a command handler for the "/progress" command
@router.message(Command("progress"))
async def view_progress(message: Message):
    # Retrieve the user's progress data
    if message.from_user.id not in user_progress:
        await message.reply("You have not started a quiz yet.")
    else:
        progress = user_progress[message.from_user.id]
        num_learned = sum(progress.values())
        total = len(flashcards)
        percent = round(num_learned / total * 100)
        await message.reply(f"You have learned {num_learned} out of {total} flashcards ({percent}%).")


# Define a command handler for the "/addflashcard" command
@router.message(Command("addflashcard"))
async def add_flashcard(message: Message, state: FSMContext):
    # Prompt the user to enter the word and its translation
    await message.reply("Please enter the word you would like to add:")
    await state.set_state(AddState.choosing_1)


# Listen for the user's response
@router.message(AddState.choosing_1)
async def get_word(message: Message, state: FSMContext):
    # Save the word to a variable
    await state.update_data(word=message.text)
    # Prompt the user to enter the translation
    await message.reply("Please enter the translation of the word:")
    await state.set_state(AddState.choosing_2)


# Listen for the user's response
@router.message(AddState.choosing_2)
async def get_translation(message: Message, state: FSMContext):
    # Save the translation to a variable
    user_data = await state.get_data()
    word = user_data["word"]
    translation = message.text
    # Add the flashcard to the list
    flashcards.append({"word": word, "translation": translation})

    # Let the user know that the flashcard has been added
    await message.reply("Flashcard added successfully!")
    await state.clear()
