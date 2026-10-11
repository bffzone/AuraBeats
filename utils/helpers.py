"""
AuraBeats - General Helpers
Author: Sakil Anowar (@YO_UR_OFFICIAL_CRUSH)
"""

import random
from typing import Iterator, List, Any


def get_readable_time(seconds: int) -> str:
    """Convert seconds to readable format: 1h 23m 45s"""
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "d"]

    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for i in range(len(time_list)):
        time_list[i] = str(time_list[i]) + time_suffix_list[i]

    if len(time_list) == 4:
        ping_time += time_list.pop() + " "

    time_list.reverse()
    ping_time += ":".join(time_list)

    return ping_time


def humanbytes(size: int) -> str:
    """Convert bytes to human readable: 1.5 MB"""
    if not size:
        return "0 B"
    power = 2 ** 10
    n = 0
    dict_power_n = {0: "B", 1: "KB", 2: "MB", 3: "GB", 4: "TB"}
    while size > power:
        size /= power
        n += 1
    return f"{round(size, 2)} {dict_power_n[n]}"


def truncate(text: str, max_length: int = 30, suffix: str = "...") -> str:
    """Truncate text to max length"""
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def chunks(lst: List[Any], n: int) -> Iterator[List[Any]]:
    """Split list into chunks of size n"""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def get_random_emoji() -> str:
    """Get random music emoji"""
    emojis = ["🎵", "🎶", "🎧", "🎤", "🎸", "🎹", "🥁", "🎺", "🎻", "🎼"]
    return random.choice(emojis)


def escape_markdown(text: str) -> str:
    """Escape markdown special characters"""
    special = ["_", "*", "[", "]", "(", ")", "~", "`", ">", "#", "+", "-", "=", "|", "{", "}", ".", "!"]
    for char in special:
        text = text.replace(char, f"\\{char}")
    return text


def clean_filename(name: str) -> str:
    """Remove illegal chars from filename"""
    illegal = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
    for char in illegal:
        name = name.replace(char, '_')
    return name.strip()
