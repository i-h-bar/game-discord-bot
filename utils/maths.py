def round_down(n: int | float, nearest: int = 60) -> int | float:
    return n - n % nearest


def round_up(n: int | float, nearest: int = 60) -> int | float:
    return n - n % -nearest
