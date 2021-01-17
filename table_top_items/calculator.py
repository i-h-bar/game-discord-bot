import re
from typing import Union
from operator import pow, truediv, mul, add, sub

operators = {
    '+': add,
    '-': sub,
    '*': mul,
    '/': truediv,
    '^': pow
}


async def calculate(expression: str) -> Union[float, int, str]:
    while "(" in expression or ")" in expression:
        if expression.count(")") != expression.count("("):
            return "Uneven brackets"

        bracketed_expressions = re.findall(r"\([0-9-*/^+. ]+\)", expression)
        for bracketed_expression in bracketed_expressions:
            expression = expression.replace(
                bracketed_expression,
                str(await calculate(bracketed_expression[1:-1])),
                1
            )

    if expression.replace(".", "", 1).strip().isdigit():
        if expression[-2:] == ".0":
            return int(expression[:-2])
        elif "." not in expression:
            return int(expression)
        else:
            return float(expression)

    for operator_symbol in operators:
        left, operator, right = expression.partition(operator_symbol)

        if operator in operators:
            try:
                return operators[operator](
                    await calculate(left.strip()),
                    await calculate(right.strip())
                )
            except ZeroDivisionError:
                return "Tried to divide by 0"
