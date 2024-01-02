from aiogram.fsm.state import State, StatesGroup


class FollowHandlers(StatesGroup):
    first_handler = State()
    second_handler = State()
    third_handler = State()
    work_handler = State()
