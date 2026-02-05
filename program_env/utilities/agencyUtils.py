
#import sys
from datetime import date


from instagrapi import Client
from instagrapi.exceptions import ChallengeRequired, LoginRequired

from enum import Enum, auto



class ExitReason(Enum):
    SAFE_TERMINATION = auto()        # intentional, clean exit
    ACCOUNT_SWITCH = auto()          # switching Instagram accounts
    SESSION_EXPIRED = auto()         # LoginRequired, stale cookies
    SESSION_CORRUPTED = auto()       # malformed session / version drift
    NETWORK_FAILURE = auto()         # timeouts, connection errors
    RATE_LIMIT = auto()              # 429-like behavior
    CHALLENGE_REQUIRED = auto()      # checkpoint
    UNKNOWN_ERROR = auto()           # fallback







def resolve_exit_reason(
    timeOutError: str,
    stop: bool,   #  = False
) -> ExitReason:
    """
    Maps runtime error state to logout policy.
    """

    err = (timeOutError or "").lower()



    if err == "session_expired":
        return ExitReason.SESSION_EXPIRED

    if err == "network_failure":
        return ExitReason.NETWORK_FAILURE

    # --- intentional / clean ---
    if not err and not stop:
        return ExitReason.SAFE_TERMINATION

    # --- high risk / freeze ---
    if err in {
        "challengeresolve",
        "challenge_resolve",
        "checkpoint_required",
        "checkpoint",
        "checkpoint required",
    }:
        return ExitReason.CHALLENGE_REQUIRED

    # --- session problems ---
    if err in {
        "login_required",
        "pinned_channels_info",
    }:
        return ExitReason.SESSION_CORRUPTED

    # --- rate / abuse style ---
    if "rate" in err or "429" in err:
        return ExitReason.RATE_LIMIT
    

    # --- unknown but non-clean ---
    return ExitReason.UNKNOWN_ERROR

def is_user_not_found(msg: str) -> bool:
    msg = (msg or "").lower()
    return "user not found" in msg

def in_error_cage(msg: str, cage: list[str]) -> str | None:
    msg = (msg or "").lower()
    for key in cage:
        if key in msg:
            return key
    return None


def login_manager(
    cl: Client,
    username: str,
    password: str,
    settings_path,
):
    """
    Returns:
        (success: bool, state: str, client: Client)

    state ∈ {"ok", "checkpoint", "login_failed"}
    """

    # 1. Try existing session first
    if settings_path.exists() and settings_path.stat().st_size > 0:
        try:
            cl.load_settings(settings_path)
            cl.account_info()  # hard validation
            print("✅ Session valid")
            return True, "ok", cl

        except LoginRequired:
            print("⚠️ Session expired — trying fresh login")
            return False, "session_expired", cl

        except Exception as err:
            print(f"⚠️ Session invalid: {err}")
            settings_path.unlink(missing_ok=True)

            #if err == "session_expired":
            #    return ExitReason.SESSION_EXPIRED

    # 2. Attempt fresh login ONCE
    try:
        cl.login(username, password)
        cl.dump_settings(settings_path)
        print("✅ Fresh login successful")
        return True, "ok", cl

    except ChallengeRequired:
        print("⛔ Checkpoint required — manual verification needed")
        return False, "checkpoint", cl

    except Exception as err:
        print(f"❌ Login failed: {err}")
        return False, "login_failed", cl



def should_delete_session(reason: ExitReason) -> bool:
    """
    Central truth table for session deletion.
    """

    return reason in {
        ExitReason.SESSION_EXPIRED,
        ExitReason.SESSION_CORRUPTED,
        ExitReason.NETWORK_FAILURE,
        ExitReason.SAFE_TERMINATION,
        ExitReason.ACCOUNT_SWITCH,
    }

def logout_manager(
    cl: Client,
    reason: ExitReason,
    settings_path,
    verbose: bool = True,
) -> None:
    """
    Decides whether to call logout() or silently discard session.

    Logout is ONLY used for intentional, human-like exits.
    """

    def log(msg):
        if verbose:
            print(msg)

    # --- SAFE, INTENTIONAL EXITS ---
    if reason in {
        ExitReason.SAFE_TERMINATION,
        ExitReason.ACCOUNT_SWITCH,
    }:
        log("🔐 Safe exit → performing graceful logout")

        try:
            cl.logout()
            log("✅ Logout successful")
        except Exception as err:
            log(f"⚠️ Logout failed (ignored): {err}")

        # Always clear session after logout
        if settings_path.exists():
            settings_path.unlink(missing_ok=True)

        return

    # --- SESSION ROTATION / RECOVERY ---
    if should_delete_session(reason):
        log("♻️ Silent session reset → NO logout")

        if settings_path.exists():
            settings_path.unlink(missing_ok=True)

        return

    # --- HIGH-RISK STATES ---
    if reason in {
        ExitReason.CHALLENGE_REQUIRED,
        ExitReason.RATE_LIMIT,
    }:
        log("⛔ Risk state detected → freezing session (NO logout)")
        log("🧊 Manual intervention required")

        # Do NOT delete session yet — may be needed for recovery
        return

    # --- FALLBACK ---
    log("⚠️ Unknown exit reason → safest path: no logout, no deletion")




def parseAgency(agents_,agentsType_,agentsNumber_,agentIndex_,agencyDict_) -> dict:
    agents,agentsNumber,agentIndex,agentsType,agency = agents_,agentsNumber_,agentIndex_,agentsType_,agencyDict_

    if(agentsNumber > len(agents[agentsType])):
        print(f"\n -- Invalid agensNumber was given {agentsNumber} | we have agent range from 1 - {len(agents[agentsType])} --\n -- Exiting program --\n")
        return agency
    
    
    #sys.stdout.write(f"\rtrying agent number {agentsNumber} out of {len(agents[agentsType])}")
    #sys.stdout.flush()


    ACCOUNT_USERNAME = agents[agentsType][agentIndex]["username"]
    ACCOUNT_PASSWORD = agents[agentsType][agentIndex]["password"]
    lastTimeUsed = (date.fromisoformat((agents[agentsType][agentIndex]["lastTimeUsed"]))) if (agents[agentsType][agentIndex]["lastTimeUsed"] != "") else ("")
    timeOutError = (agents[agentsType][agentIndex]["timeOutError"]).lower()
    

    today = date.today() #today # year, month, day
    delta = today - (lastTimeUsed if (lastTimeUsed != "") else today)
    days_between = int(delta.days)
    agentDaysRefresh = 7
    expiredSession = (days_between < agentDaysRefresh)
    #dontDeleteSession = (True) if (timeOutError in {"challengeresolve","challenge_resolve","login_required","checkpoint_required"}) else (False)
    #print(f"\n -- {days_between} --")

    if((timeOutError != "") or ((days_between <= agentDaysRefresh) and (today != lastTimeUsed) and (lastTimeUsed != "")) or ((today == lastTimeUsed) and days_between == 0)):
        if(timeOutError != ""): #prompt user to ask if issue has been resolved , if the issue has beeen resolved,clear the issue string
            print(f"\n --- Unresolved Timeout Error issue in JSON file --> agents.json | for Agent username --> {ACCOUNT_USERNAME}")
        elif(lastTimeUsed != ""): 
            print(f"\nAgent still in it's refresh phase with {days_between} out of {agentDaysRefresh} days left | for Agent username --> {ACCOUNT_USERNAME}")
        criticalCheckpoint1 = False
    else:
        criticalCheckpoint1 = True


    if(criticalCheckpoint1):
        print(f"\nFound adequate agent to use  -->  {ACCOUNT_USERNAME} | {ACCOUNT_PASSWORD}")
        agency = {"ACCOUNT_USERNAME":ACCOUNT_USERNAME, "ACCOUNT_PASSWORD":ACCOUNT_PASSWORD, "lastTimeUsed":lastTimeUsed, "timeOutError":timeOutError,"checkPoint":True,"agentIndex":agentIndex} # ,"expiredSession":expiredSession
        #countdown(10)

    #print("\n\n ---------------------------------------- ")

    return agency
    
            


def runAgency(setAgentsNumberToUse_=0,agentsType_="SCRAPING_AGENTS",agents_={}) -> dict:
    number = setAgentsNumberToUse_ # Set an agent manually based on number not index
    agentsType = agentsType_
    agents = agents_

    # if agents is empty, prompt user to create an instagram agent account , input username, password 

    # My agents Json Data and assigned variables
    

    agency = {"ACCOUNT_USERNAME":"", "ACCOUNT_PASSWORD":"", "lastTimeUsed":"", "timeOutError":"","checkPoint":False,"agentIndex":""}

    if(number >=1):
        agentsNumber = number
        agentIndex = number - 1

        agency = parseAgency(agents,agentsType,agentsNumber,agentIndex,agency)
    else:
        for i in range(0,len(agents[agentsType])):

            # Set agent number to use from agents json
            agentsNumber = i + 1
            agentIndex = i

            agency = parseAgency(agents,agentsType,agentsNumber,agentIndex,agency)

            if(agency["checkPoint"]):
                break


    return agency
