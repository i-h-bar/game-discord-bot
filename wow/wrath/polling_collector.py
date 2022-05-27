import re

from discord import Message

from wow.wrath.regex import poll_regex


async def collect_result(message: Message):
    await message.delete()
    content = message.content

    if not re.fullmatch(poll_regex, message.content):
        await message.author.send(
            "Failed to submit choice as message did not follow the required format:"
            "\n\n1. Choice One\n2. Choice Two\n3. Choice Three\netc."
        )

    else:
        nums = [int(num) for num in re.findall(r"[\d]+", message.content)]
        if nums != [num for num in range(1, len(nums) + 1)]:
            await message.author.send(
                f"Your numbers are not in order dingus:\n\n{content}"
            )
        else:
            poll_result_channel = [
                channel for channel in message.guild.channels if channel.name == "wrath-poll-results"
            ][0]

            async for past_message in poll_result_channel.history():
                if str(message.author.id) in past_message.content:
                    await past_message.delete()

            await poll_result_channel.send(
                f"Polling ID: {message.author.id}"
                f"\n{message.author.nick if message.author.nick is not None else message.author.name}:\n{content}"
            )
            await message.author.send(f"Confirmation of choice submission:\n\n{content}\n{nums[-1] + 1}. Giga Chad")
