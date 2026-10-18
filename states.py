from aiogram.fsm.state import State, StatesGroup


class UserStates(StatesGroup):
    withdrawal_amount = State()
    withdrawal_details = State()
    support_message = State()
    task_proof = State()
    buy_gold_amount = State()


class AdminStates(StatesGroup):
    input = State()
