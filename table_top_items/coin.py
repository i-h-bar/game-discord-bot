import re
import random

from discord.message import Message


async def flip_coin(message: Message):
    channel = message.channel
    reply = f"{message.author.mention} "

    if "until" in message.content:
        fixed_message = message.content.replace("untill", "until")
        loss_condition = fixed_message.split("until")[1].strip().lower()
        with_thumb = False
        if loss_condition not in ["heads", "tails"]:
            if "with thumb" in loss_condition:
                loss_condition = loss_condition.split()[0]
                with_thumb = True
                if loss_condition not in ["heads", "tails"]:
                    reply += "you need to choose 'heads' or 'tails' with 'flip until {}' command."
                    await channel.send(reply)
                else:
                    loss_condition = loss_condition.split()[0], loss_condition.split()[0]
            else:
                reply += "you need to choose 'heads' or 'tails' with 'flip until {}' command."
                await channel.send(reply)

        wins = 0
        flip = random.choice(["heads", "tails"])
        if with_thumb:
            flip = flip, random.choice(["heads", "tails"])

        reply += f"\n`{flip}`"

        while flip != loss_condition:
            wins += 1
            flip = random.choice(["heads", "tails"])
            if with_thumb:
                flip = flip, random.choice(["heads", "tails"])
            reply += f"\n`{flip}`"

        reply += f"\n`wins = {wins}`"
        await channel.send(reply)

    else:
        channel = message.channel
        reply = f"{message.author.mention} "

        try:
            times = int(re.findall(r"\d+", message.content)[0])
        except IndexError:
            times = 1

        for _ in range(times):
            reply += f"\n`{random.choice(['heads', 'tails'])}`"

        await channel.send(reply)
