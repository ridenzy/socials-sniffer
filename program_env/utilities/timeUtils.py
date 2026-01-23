import time
import sys


import random



def countdown(seconds: int) -> None:
    """
    Countdown from `seconds` to 0, printing each second.
    """
    if seconds < 0:
        raise ValueError("seconds must be >= 0")

    while seconds > 0:
        print(f"{seconds}...")
        time.sleep(1)
        seconds -= 1

    print("⏰ Time's up!")



def countdown_inline(seconds: int) -> None:
    """
    Countdown that updates in-place in the terminal.
    """
    print(f"\n🕒 Waiting {seconds}s before next request")

    if seconds < 0:
        raise ValueError("seconds must be >= 0")

    for remaining in range(seconds, 0, -1):
        sys.stdout.write(f"\r⏳ {remaining} seconds remaining")
        sys.stdout.flush()
        time.sleep(1)

    sys.stdout.write("\r⏰ Time's up!            \n")


def random_delay(min_seconds: int, max_seconds: int) -> int:
    """
    Generate a random delay between min_seconds and max_seconds (inclusive).
    """
    if min_seconds < 0 or max_seconds < 0:
        raise ValueError("Seconds must be >= 0")
    if min_seconds > max_seconds:
        raise ValueError("min_seconds cannot be greater than max_seconds")

    return random.randint(min_seconds, max_seconds)


def human_sleep(min_s=5, max_s=12):
    delay = random_delay(min_s, max_s)
    countdown_inline(delay)