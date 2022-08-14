from datetime import datetime, timedelta

from discord import Message


open_feedback_sessions = {}


async def open_feedback_session(message: Message):
    await message.delete()
    author = message.author

    try:
        session = open_feedback_sessions[author.id]
    except KeyError:
        feedback_channel = [channel for channel in message.guild.channels if "feedback-responses" in channel.name]
        if len(feedback_channel) != 1:
            await author.send(
                f"The server '{message.guild.name}' has not properly set up a feedback channel please message a server "
                f"admin asking them to make exactly one channel with 'feedback-responses' in the name"
            )
            return
        feedback_channel = feedback_channel[0]
        session_info = {
            "author": author,
            "feedback_channel": feedback_channel,
            "session_expiry": datetime.now() + timedelta(hours=1),
            "feedback_taken": False
        }
        open_feedback_sessions[author.id] = session_info

        await author.send("Please post your feedback in a DM back to me, Roberto... Beep Boop.")
    else:
        if session["feedback_taken"]:
            await session["author"].send(
                "We have already taken your feedback. If you have more, please try again later."
            )


async def take_feedback(message: Message):
    try:
        session = open_feedback_sessions[message.author.id]
    except KeyError:
        return
    else:
        if not session["feedback_taken"]:
            if session["author"].nick:
                author_name = session["author"].nick
            else:
                author_name = session["author"].name

            feedback_message = f"{author_name}:\n\n{message.content}"
            await session["feedback_channel"].send(feedback_message)
            await session["author"].send("We have successfully taken your feedback :)")
            session["feedback_taken"] = True


async def get_expired_sessions():
    now = datetime.now()
    for user_id, session_info in open_feedback_sessions.items():
        if session_info["session_expiry"] < now:
            yield user_id


async def clear_expired_feedback_sessions():
    expired_sessions = [user_id async for user_id in get_expired_sessions()]

    for user_id in expired_sessions:
        del open_feedback_sessions[user_id]
