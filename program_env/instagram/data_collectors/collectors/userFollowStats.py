
from instagrapi import Client

from program_env.utilities.jsonUtils import (
    create_json_if_not_exists,
    read_json,
    write_json,
)

from program_env.utilities.timeUtils import (
    human_sleep,
    reset_rate_limits
)

from program_env.utilities.agencyUtils import (
    runAgency,
    login_manager,
    logout_manager,
    resolve_exit_reason,
)

from program_env.utilities.userDataUtils import (
    runUsernameFrames,
    standardizeUserData
)

from pathlib import Path
from datetime import date



BASE_DIR = Path(__file__).resolve().parents[4]
error_cage = ["ChallengeResolve"]

 # set target account username
TARGET_ACCOUNT = "germanyfits.de"
SCRAPE_COUNT_BASED_ON_TARGET_ACCOUNT_POSTS = 2000  #Benchmark is 300 posts
AGENTS_NUMBER_TO_USE_IF_I_WANT_TO = 0      # from 1 upwards




def main() -> None:
    def mark_network_failure():
        nonlocal stop, timeOutError
        stop = True
        timeOutError = "network_failure"

    print("Running socials-sniffer user followers and following collector")



    criticalCheckpoint2,criticalCheckpoint3,criticalCheckpoint4,criticalCheckpoint5,criticalCheckpoint6,criticalCheckpoint7 = False,False,False,False,False,False
    ACCOUNT_USERNAME,ACCOUNT_PASSWORD,lastTimeUsed,timeOutError = "","","",""

    TARGET_USER_ID = ""
    today = date.today() #today # year, month, day

    follows = []


    # Grab Storage json files
    storage = BASE_DIR / "program_env" / "instagram" / "data_collectors" / "storage" / "raw-data" / "all-scraped-user-data.json"
    create_json_if_not_exists(storage)
    frame = read_json(storage)

    agents_ = BASE_DIR / "program_env" / "utilities" / "agents" / "agents.json"
    create_json_if_not_exists(agents_)
    agents = read_json(agents_)
    agentsType = "SCRAPING_AGENTS"

    








    max_mash = 200
    min_mash = 150
    mash = min_mash
    TARGET_AMOUNT = (mash) if (SCRAPE_COUNT_BASED_ON_TARGET_ACCOUNT_POSTS > mash) else (SCRAPE_COUNT_BASED_ON_TARGET_ACCOUNT_POSTS)








    # Set and grab agents details

    agency = runAgency(AGENTS_NUMBER_TO_USE_IF_I_WANT_TO,agentsType,agents)
    ACCOUNT_USERNAME = agency["ACCOUNT_USERNAME"]
    ACCOUNT_PASSWORD = agency["ACCOUNT_PASSWORD"]
    lastTimeUsed =  agency["lastTimeUsed"]
    timeOutError =  agency["timeOutError"]
    agentIndex = agency["agentIndex"]
    criticalCheckpoint2 = agency["checkPoint"]
    print(f"\n agency is recorded as: {agency}")

    settings_path = BASE_DIR / "program_env" / "utilities" / "agents" / "sessions" / f"{ACCOUNT_USERNAME}.json" # Create settings file per agent

    cl = Client()
    stop=False
    if(criticalCheckpoint2):
        print("\n --- Checkpoint 2 passed")

        

        success, state, cl = login_manager(
            cl=cl,
            username=ACCOUNT_USERNAME,
            password=ACCOUNT_PASSWORD,
            settings_path=settings_path,
        )

        if not success:
            if state == "checkpoint":
                print("🛑 Resolve checkpoint manually, then rerun.")
                timeOutError = "checkpoint_required"
            elif state == "session_expired":
                print("🛑 Session has expired.")
                timeOutError = "session_expired"
            else:
                print("🛑 Login failed — stopping run.")
                timeOutError = "login_failed"
            stop = True
            criticalCheckpoint3 = False
        else:
            criticalCheckpoint3 = True

        print("🚀 Logged in, continuing scraper...")
    else:
        print("---------\n ---- Could not Log into your scraping agent \n--------")
        pass




    if(criticalCheckpoint3):
        print("\n --- Checkpoint 3 passed")
        print("\n--- Stalling after  login ---")
        human_sleep("normal",3,reset_rate_limits)

        try:
            TARGET_USER_ID = cl.user_id_from_username(TARGET_ACCOUNT)
            criticalCheckpoint4 = True
        except Exception as err:
            print(f"\n -- TARGET_USER_ID error at --> {err}")
            timeOutError = str(err)
            for i in error_cage:
                if i in str(err):
                    timeOutError = i
    else:
        pass
        print("")

    if(criticalCheckpoint4):
        print("\n --- Checkpoint 4 passed")
        human_sleep("normal",2,reset_rate_limits)

        print("\n trying to grab followers")

        for key,values in (cl.user_followers(user_id=TARGET_USER_ID ,amount=TARGET_AMOUNT)).items():
            try:
                #followers = cl.user_followers(user_id=TARGET_USER_ID ,amount=TARGET_AMOUNT)
                follows.append(values.model_dump())
                criticalCheckpoint5 = True
            except Exception as err:
                print(f"\n -- user_followers partial failure at --> {err}")
                timeOutError = str(err)
                for i in error_cage:
                    if i in str(err):
                        timeOutError = i
    else:
        pass

    if(criticalCheckpoint5):
        print("\n --- Checkpoint 5 passed")
        human_sleep("safe",1,reset_rate_limits)

        print("\n trying to grab following")

        for key,values in (cl.user_following(user_id=TARGET_USER_ID ,amount=TARGET_AMOUNT)).items():
            try:
                #following = cl.user_following(user_id=TARGET_USER_ID ,amount=TARGET_AMOUNT)
                follows.append(values.model_dump())
                criticalCheckpoint6 = True
                
            except Exception as err:
                print(f"\n -- user_followers partial failure at --> {err}")
                timeOutError = str(err)
                for i in error_cage:
                    if i in str(err):
                        timeOutError = i
    else:
        pass

    if(criticalCheckpoint5 or criticalCheckpoint6): 
        print("\n --- Checkpoint 4 && 5 passed")

        for data in follows:
            frame = runUsernameFrames(frame,data)

        criticalCheckpoint7 = True
        write_json(storage,frame)
    else:
        pass

    if(criticalCheckpoint7):
        standardizedUserData = standardizeUserData(frame)
        write_json(storage, standardizedUserData)
        print("\n Scraped user data has been standardized for for consistent outlook")
    else:
        pass

    

    if(criticalCheckpoint2):
        agents[agentsType][agentIndex]["lastTimeUsed"] = str(today)
        agents[agentsType][agentIndex]["timeOutError"] = timeOutError
        write_json(agents_ ,agents)
    else:
        pass

    
    exit_reason = resolve_exit_reason(timeOutError=timeOutError,stop=stop)
    logout_manager(cl=cl,reason=exit_reason,settings_path=settings_path,)


    print("\n --- Done with program")

        

if __name__ == "__main__":
    main()



# There's a problem here