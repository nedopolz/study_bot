from loader import db


async def user_checker(user_id: int) -> bool:
    already_exists = await db.check_user(user_id)
    already_exists = already_exists.pop(0)
    already_exists = already_exists.get('exists')
    return already_exists