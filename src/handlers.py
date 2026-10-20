from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from db.users import get_user, create_user
from db.tasks import add_task, get_tasks, mark_task_done, delete_task, get_task_stats
from src.keyboards import get_task_keyboard

router = Router()

class TaskStates(StatesGroup):
    waiting_for_task_title = State()  
    waiting_for_done_id = State()     
    waiting_for_delete_id = State()   



@router.message(Command("start"))
async def cmd_start(message: types.Message):
    tg_id = message.from_user.id
    username = message.from_user.username or message.from_user.first_name

    user = get_user(tg_id)
    if not user:
        user = create_user(tg_id, username)
        await message.answer(f"Привет, {username}.")
    else:
        await message.answer(f"Рад видеть тебя снова, {username}!")


@router.message(Command("add"))
async def cmd_add(message: types.Message, state: FSMContext):
    await message.answer("Введите название новой задачи:")
    await state.set_state(TaskStates.waiting_for_task_title)

@router.message(TaskStates.waiting_for_task_title)
async def process_add_task(message: types.Message, state: FSMContext):
    user = get_user(message.from_user.id)
    if not user:
        await message.answer("Ошибка: сначала введите /start для регистрации.")
        await state.clear()
        return

    title = message.text
    add_task(user["id"], title) 
    await message.answer(f"Запись добавлена: \"{title}\"")
    await state.clear()


@router.message(Command("tasks"))
async def cmd_tasks(message: types.Message):
    user = get_user(message.from_user.id)
    if not user:
        await message.answer("Пожалуйста, зарегистрируйтесь с помощью /start")
        return

    tasks = get_tasks(user["id"])
    if not tasks:
        await message.answer("У вас пока нет задач.")
        return

    await message.answer(" **Ваш список задач:**", parse_mode="Markdown")
    
    for task in tasks:
        status_emoji = "выполнена" if task["is_done"] == 1 else "не выполнена"
        text = f"Задание №{task['id']}\n {task['title']}\nСтатус: {status_emoji}"
        
        if task["is_done"] == 0:
            reply_markup = get_task_keyboard(task["id"])
            await message.answer(text, reply_markup=reply_markup)
        else:
            await message.answer(text)


@router.message(Command("done"))
async def cmd_done(message: types.Message, state: FSMContext):
    await message.answer("Введите порядковый номер задачи, которую хотите отметить выполненной:")
    await state.set_state(TaskStates.waiting_for_done_id)

@router.message(TaskStates.waiting_for_done_id)
async def process_done_task(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Пожалуйста, введите корректное число (ID задачи):")
        return

    task_id = int(message.text)
    user = get_user(message.from_user.id)
    
    success = mark_task_done(task_id, user["id"])
    if success:
        await message.answer(f"Задача №{task_id} успешно отмечена как выполненная!")
    else:
        await message.answer("Ошибка: задача не найдена или принадлежит другому пользователю.")
    
    await state.clear()


@router.callback_query(lambda c: c.data.startswith("inline_done_"))
async def callback_inline_done(callback: types.CallbackQuery):
    task_id = int(callback.data.split("_")[2])
    user = get_user(callback.from_user.id)

    success = mark_task_done(task_id, user["id"])
    if success:
        current_text = callback.message.text
        updated_text = current_text.replace("не выполнена", "выполнена")
        
        await callback.message.edit_text(text=updated_text, reply_markup=None)
        await callback.answer("Задача выполнена!")
    else:
        await callback.answer("Ошибка выполнения задачи.", show_alert=True)


@router.message(Command("stats"))
async def cmd_stats(message: types.Message):
    user = get_user(message.from_user.id)
    if not user:
        await message.answer("Пожалуйста, зарегистрируйтесь через /start")
        return

    stats = get_task_stats(user["id"])
    
    response = (
        f"**Статистика ваших задач:**\n\n"
        f"Всего задач: {stats['total']}\n"
        f"Выполнено: {stats['done']}\n"
        f"Не выполнено: {stats['not_done']}"
    )
    await message.answer(response, parse_mode="Markdown")


@router.message(Command("delete"))
async def cmd_delete(message: types.Message, state: FSMContext):
    await message.answer("Введите порядковый номер задачи для удаления:")
    await state.set_state(TaskStates.waiting_for_delete_id)

@router.message(TaskStates.waiting_for_delete_id)
async def process_delete_task(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Пожалуйста, введите число:")
        return

    task_id = int(message.text)
    user = get_user(message.from_user.id)

    success = delete_task(task_id, user["id"])
    if success:
        await message.answer(f"Задача №{task_id} успешно удалена.")
    else:
        await message.answer("Ошибка: задача не найдена или принадлежит другому пользователю.")
        
    await state.clear()
