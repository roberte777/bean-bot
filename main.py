import os
from datetime import datetime, time, timedelta

import discord
from discord.ext import commands
from dotenv import load_dotenv
from libs.users import load_users, get_sorted_users, User
from libs.bean_bucks import add_bean_bucks


load_dotenv()
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(intents=intents, command_prefix='$')
TOKEN = os.getenv('DISCORD_TOKEN')
BB_CHANNEL = bot.get_channel(1006320141535019118)
BB_TIME = time(18, 0, 0)  # 6:00 PM
REP_ID = int(260576772884529152)
REP_GUILD = None
users = load_users()
active_bets = {}
bet_confirmer = {}


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command()
async def bean(ctx):
    id = str(ctx.message.author.id)
    if id == "182269621020131328":
        await ctx.send('You\'re Fat')
    else:
        await ctx.send('Bean Fat')

@bot.command()
async def ledger(ctx):
    msg = '**Bean Bucks Betting Bodega Balance **\n'
    sorted_users = get_sorted_users(users)
    for user in sorted_users:
        msg = msg + '\t \t **{}**: {} Bean Bucks'.format(
            user.name, user.bean_bucks) + '\n'
    await ctx.send(msg)

bot.remove_command('help')

@bot.command()
async def help(ctx):
    msg = '''**Bean Bucks Bots Bodacious Behavior**
         **$ledger**: Check Balances
         **$bet @person amount**: To place a bet
         **$claim**: claim the bean bucks throne
         **$bean**: secret message
         '''
    await ctx.send(msg)

@bot.command()
async def bet(ctx, user2: discord.User, amount: int):
    if amount <= 5000:
        user1 = ctx.message.author
        msg = await ctx.send('{} bet {} {} BeanBucks'.format(
            user1.name, user2.name, amount))
        await msg.add_reaction('👍')
        await msg.add_reaction('👎')
        active_bets[msg] = (user1, user2, amount)
        bet_confirmer[msg] = [0, 0]
    else:
        await ctx.send("Betting limit of 5k exceed. Broke Bitches.")

async def settle_bet(winner: discord.User, loser: discord.User, amount: int, users: list[User]):
    add_bean_bucks(winner, amount, users)
    add_bean_bucks(loser, -1 * amount, users)
    return '{} won {} BeanBucks from {}'.format(winner.name, amount,
                                                loser.name)

@bot.event
async def on_reaction_add(reaction, user: discord.User):
    if reaction.message in active_bets and user.id != bot.user.id:
        user1, user2, amount = active_bets[reaction.message]

        if user.id == user1.id:
            if str(reaction) == '👍':
                bet_confirmer[reaction.message][0] = 1
            elif str(reaction) == '👎':
                bet_confirmer[reaction.message][0] = -1
        elif user.id == user2.id:
            if str(reaction) == '👍':
                bet_confirmer[reaction.message][1] = 1
            elif str(reaction) == '👎':
                bet_confirmer[reaction.message][1] = -1

        total = sum(bet_confirmer[reaction.message])

        if abs(total) == 2:
            user1, user2, amount = active_bets.pop(reaction.message)
            if total == 2:
                msg = await settle_bet(user1, user2, amount, users)
                await reaction.message.channel.send(msg)
            elif total == -2:
                msg = await settle_bet(user2, user1, amount, users)
                await reaction.message.channel.send(msg)

bot.run(TOKEN)
