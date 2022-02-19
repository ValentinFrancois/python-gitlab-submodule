def lstrip(string: str, pattern: str) -> str:
    if string[:len(pattern)] == pattern:
        return string[len(pattern):]
    else:
        return string


def rstrip(string: str, pattern: str) -> str:
    if string[-len(pattern):] == pattern:
        return string[:-len(pattern)]
    else:
        return string
