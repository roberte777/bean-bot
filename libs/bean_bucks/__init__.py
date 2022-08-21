import discord
from libs.users import User, add_user, save_users
def add_bean_bucks(user: discord.User, amount: int, users: list[User]):
    id = str(user.id)
    user_ids = [user.id for user in users]
    if id not in user_ids:
        add_user(id, user.name, users)
    new_balance = 0
    for user in users:
        if user.id == id:
            user.bean_bucks += amount
            new_balance = user.bean_bucks
            break
    save_users(users)
    return new_balance
