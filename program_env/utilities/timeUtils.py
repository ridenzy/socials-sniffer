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



def scraping_delay_profile(
    mode: str = "normal",
    aggressiveness: int = 1
) -> tuple[int, int]:
    """
    Generate (min_seconds, max_seconds) for scraping delays.

    mode:
        - "safe"      → very conservative (account longevity)
        - "normal"    → balanced
        - "aggressive"→ faster but riskier

    aggressiveness:
        1 (lowest) → 5 (highest)
    """

    if aggressiveness < 1 or aggressiveness > 5:
        raise ValueError("aggressiveness must be between 1 and 5")

    profiles = {
        "safe": {
            1: (20, 45),
            2: (18, 40),
            3: (15, 35),
            4: (12, 30),
            5: (10, 25),
        },
        "normal": {
            1: (12, 25),
            2: (10, 22),
            3: (8, 18),
            4: (6, 15),
            5: (5, 12),
        },
        "aggressive": {
            1: (8, 15),
            2: (6, 12),
            3: (5, 10),
            4: (4, 8),
            5: (3, 6),
        },
    }

    if mode not in profiles:
        raise ValueError("mode must be: safe, normal, or aggressive")

    return profiles[mode][aggressiveness]



#def human_sleep(min_s=5, max_s=12):
#    delay = random_delay(min_s, max_s)
#    countdown_inline(delay)

def human_sleep(mode="normal", aggressiveness=2):
    min_s, max_s = scraping_delay_profile(mode, aggressiveness)
    delay = random_delay(min_s, max_s)
    countdown_inline(delay)
