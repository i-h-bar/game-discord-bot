
ORDINAL_SUFFIXES = [
    'th',
    'st',
    'nd',
    'rd',
    'th'
]


async def ordinal(num):
    suffix = ORDINAL_SUFFIXES[min(num % 10, 4)]
    if 11 <= (num % 100) <= 12:
        suffix = "th"

    return f"{num}{suffix}"
