import time
import sys


import random

"""
🎯 Recommended values (based on the scraper)
---
🟢 Good default
MAX_ALLOWED_GAP = 90
---

Why:

our delays go up to ~45s

Network hiccups can stall for ~10–20s

90s avoids false positives

---
🔵 Conservative (long runs / laptop use)
MAX_ALLOWED_GAP = 120
---
🔴 Aggressive (short, controlled runs)
MAX_ALLOWED_GAP = 45


I do NOT recommend this for your case.
"""

LAST_HEARTBEAT = None
MAX_ALLOWED_GAP = 3600 #( 1 hrs ) #120  # seconds (tune this)

def heartbeat_check(reset_callback=None):
    global LAST_HEARTBEAT

    now = time.time()

    if LAST_HEARTBEAT is None:
        LAST_HEARTBEAT = now
        return False

    gap = now - LAST_HEARTBEAT
    LAST_HEARTBEAT = now

    if gap > MAX_ALLOWED_GAP:
        print(f"\n⚠️ Detected system sleep / suspend (gap: {int(gap)}s)")
        if reset_callback:
            reset_callback()
        return True

    return False


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


"""
def countdown_inline(seconds: int) -> None:
    
    #Countdown that updates in-place in the terminal.
    
    print(f"\n🕒 Waiting {seconds}s before next request")

    if seconds < 0:
        raise ValueError("seconds must be >= 0")

    for remaining in range(seconds, 0, -1):
        sys.stdout.write(f"\r⏳ {remaining} seconds remaining")
        sys.stdout.flush()
        time.sleep(1)

    sys.stdout.write("\r⏰ Time's up!            \n")
"""

def countdown_inline(seconds: int, reset_callback=None, on_suspend=None) -> None:
    if seconds < 0:
        raise ValueError("seconds must be >= 0")

    print(f"\n🕒 Waiting {seconds}s before next request")

    for remaining in range(seconds, 0, -1):
        if heartbeat_check(reset_callback):
            print("🔁 Cooldown reset after suspend")
            if on_suspend:
                on_suspend()
            return
            #return  # exit countdown safely

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

def reset_rate_limits():
    print("♻️ Resetting rate-limit state")
    time.sleep(5)  # short safety buffer

def human_sleep(mode="normal", aggressiveness=2, reset_callback=None, on_suspend=None):
    min_s, max_s = scraping_delay_profile(mode, aggressiveness)
    delay = random_delay(min_s, max_s)
    #countdown_inline(delay)
    countdown_inline(delay, reset_callback, on_suspend)
