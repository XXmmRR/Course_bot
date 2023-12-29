from aiogram.fsm.state import State, StatesGroup


def create_dynamic_states_class(class_name, states):
    """
    Создает динамический класс с заданными состояниями.

    :param class_name: Имя создаваемого класса.
    :param states: Список имен состояний.
    :return: Динамически созданный класс.
    """
    states_dict = {state: State() for state in states}
    return type(class_name, (StatesGroup,), states_dict)


# Создаем класс DynamicStates с динамическими состояниями
DynamicStates = create_dynamic_states_class("DynamicStates", ["STATE_1", "STATE_2", "STATE_3"])
print(DynamicStates.STATE_1)


