from instagrapi import Client

from program_env.utilities.jsonUtils import (
    create_json_if_not_exists,
    read_json,
    write_json,
)

from program_env.utilities.timeUtils import (
    human_sleep
)

from program_env.utilities.agencyUtils import (
    runAgency
)

from pathlib import Path
from datetime import date


"""

Note: parents[4] depends on depth:

mediaID.py is at program_env/instagram/data_collectors/collectors/mediaID.py

parents[0] = collectors

parents[1] = data_collectors

parents[2] = instagram

parents[3] = program_env

parents[4] = socials-sniffer root

So parents[4] should be your repo root.

"""

BASE_DIR = Path(__file__).resolve().parents[4]
error_cage = ["ChallengeResolve"]

 # set target account username
TARGET_ACCOUNT = "bootshaus"
SCRAPE_COUNT_BASED_ON_TARGET_ACCOUNT_POSTS = 2000  #Benchmark is 300 posts
AGENTS_NUMBER_TO_USE_IF_I_WANT_TO = 0      # from 1 upwards




def main():
    print("Running socials-sniffer mediaID collector")



    criticalCheckpoint2,criticalCheckpoint3,criticalCheckpoint4,criticalCheckpoint5 = False,False,False,False
    ACCOUNT_USERNAME,ACCOUNT_PASSWORD,lastTimeUsed,timeOutError = "","","",""

    TARGET_USER_ID,user_medias = "",[]
    today = date.today() #today # year, month, day


    # Grab Storage json files
    storage = BASE_DIR / "program_env" / "instagram" / "data_collectors" / "storage" / "raw-data" / "all-scraped-users-media-id.json"
    create_json_if_not_exists(storage)
    frame = read_json(storage)

    agents_ = BASE_DIR / "program_env" / "utilities" / "agents" / "agents.json"
    create_json_if_not_exists(agents_)
    agents = read_json(agents_)
    agentsType = "SCRAPING_AGENTS"

    #settings_path = BASE_DIR / "program_env" / "utilities" / "agents" / "sessions" / f"{ACCOUNT_USERNAME}.json" # Create settings file per agent

   



    

   
    max_mash = 300
    min_mash = 200
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

    if(criticalCheckpoint2):
        print("\n --- Checkpoint 2 passed")


        if settings_path.exists() and settings_path.stat().st_size > 0: # Load settings BEFORE login
            try:
                cl.load_settings(settings_path)
                try:
                    cl.account_info()  # or cl.user_info_v1(cl.user_id)
                    criticalCheckpoint3 = True
                except Exception as errors:
                    # session expired → full login
                    try:
                        cl.login(ACCOUNT_USERNAME, ACCOUNT_PASSWORD) # login to agent account  | Login only if needed
                        #cl.login("armani.styled","@2EH2dEJv9q")
                        print("\n 1 i logged in")
                        cl.dump_settings(settings_path)
                        print("\n 1 i dumped")
                        criticalCheckpoint3 = True
                    except Exception as err:
                        print(f"\n -- 1 Log in error at --> {err}")
                        timeOutError = str(err)
                        for i in error_cage:
                            if i in str(err):
                                timeOutError = i
            except Exception as err:               
                print(f"\n -- 2 Log in error at --> {err}")
                timeOutError = str(err)
                for i in error_cage:
                    if i in str(err):
                        timeOutError = i
        else:
            try:
                cl.login(ACCOUNT_USERNAME, ACCOUNT_PASSWORD) # login to agent account  | Login only if needed
                #cl.login("armani.styled","@2EH2dEJv9q")
                print("\n 3 i logged in")
                cl.dump_settings(settings_path)
                print("\n 3 i dumped")
                criticalCheckpoint3 = True
            except Exception as err:
                print(f"\n -- 3 Log in error at --> {err}")
                timeOutError = str(err)
                for i in error_cage:
                    if i in str(err):
                        timeOutError = i
    else:
        print("---------\n ---- Could not Log into your scraping agent \n--------")
        pass


    if(criticalCheckpoint3):
        print("\n --- Checkpoint 3 passed")
        print("\n--- Stalling after  login ---")
        human_sleep("normal",3)

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
    
    

    if(criticalCheckpoint4):
        print("\n --- Checkpoint 4 passed")

        for media in cl.user_medias(user_id=TARGET_USER_ID,amount=TARGET_AMOUNT):  #cl.user_medias_v1
            try:
                user_medias.append(media)
                criticalCheckpoint5 = True
            except Exception as err:
                print(f"\n -- user_medias partial failure at --> {err}")
                timeOutError = str(err)
                for i in error_cage:
                    if i in str(err):
                        timeOutError = i
    else:
        pass
    

    if(criticalCheckpoint5):
        print("\n --- Checkpoint 5 passed")
        #stop = False
    
        for media in user_medias:
            #if (stop):
            #    break
            #else:
            #    pass
            try:
                code = str(media.code)
                pk_ID = str(media.id)
                if code not in frame:
                    frame[code] = {"sourceAccount":TARGET_ACCOUNT, "mediaid":code, "is_used":False,"id":pk_ID,"error_encountered":""}
                    write_json(storage,frame)
            except Exception as err:
                print("\n ---- ")
                print(err)
                print("\n ---- ")
                timeOutError = str(err)
                for i in error_cage:
                    if i in str(err):
                        timeOutError = i
                #stop = True
                
    else:
        pass
    


    if(criticalCheckpoint2):
        agents[agentsType][agentIndex]["lastTimeUsed"] = str(today)
        agents[agentsType][agentIndex]["timeOutError"] = timeOutError
        write_json(agents_ ,agents)
    else:
        pass

    #cl.logout()

    return

    



    

    print("\n --- Done")





if __name__ == "__main__":
    main()


