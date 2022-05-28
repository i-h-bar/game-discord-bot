from string import punctuation

poll_regex = fr"(?m)^1.[a-zA-Z {punctuation}]+(?:\n(30|[12][0-9]|[1-9])\.[a-zA-Z {punctuation}]+)+"
x = 0
