
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

from program_env.utilities.userDataUtils import (
    runUsernameProfiles,
    cleanUserData,
    standardizeUserData
)

from pathlib import Path
from datetime import date



  

BASE_DIR = Path(__file__).resolve().parents[4]
error_cage = ["ChallengeResolve"]
error_ignore = ["pinned_channels_info","User not found"]

AGENTS_NUMBER_TO_USE_IF_I_WANT_TO = 0   # from 1 upwards



def main() -> None:
    print("Running socials-sniffer userProfile collector")


    criticalCheckpoint1,criticalCheckpoint2 = False,False

    ACCOUNT_USERNAME,ACCOUNT_PASSWORD,lastTimeUsed,timeOutError = "","","",""
    today = date.today() #today # year, month, day




    # All scraped userNames Json data amd assigned variables
    
    storage_UserNames = BASE_DIR / "program_env" / "instagram" / "data_collectors" / "storage" / "raw-data" / "all-scraped-user-data.json"
    create_json_if_not_exists(storage_UserNames)
    frame_Usernames = read_json(storage_UserNames)

    # My agents Json Data and assigned variables
    agents_ = BASE_DIR / "program_env" / "utilities" / "agents" / "agents.json"
    agents = read_json(agents_)
    agentsType = "SCRAPING_AGENTS"



    #"""
    agency = runAgency(AGENTS_NUMBER_TO_USE_IF_I_WANT_TO,agentsType,agents)
    ACCOUNT_USERNAME = agency["ACCOUNT_USERNAME"]
    ACCOUNT_PASSWORD = agency["ACCOUNT_PASSWORD"]
    #lastTimeUsed =  agency["lastTimeUsed"]
    timeOutError =  agency["timeOutError"]
    agentIndex = agency["agentIndex"]
    criticalCheckpoint1 = agency["checkPoint"]
    print(f"\n agency is recorded as: {agency}")


    

    


    settings_path = BASE_DIR / "program_env" / "utilities" / "agents" / "sessions" / f"{ACCOUNT_USERNAME}.json" # Create settings file per agent
    #create_json_if_not_exists(settings_path)

    today = date.today() #today # year, month, day
    userDataDaysRefresh = 5 # Users are re-checked every x days



    print("\n - Action: Scrape for user Profile data with 1\n - Action: Clean scraped user Profile data for inconsistencies with 2\n - Action: Check how many users have been scraped with 3\n - Action: Standardized user profile data keys for conformity with 4\n")
    user_input = input("Enter action number: ")
    
    if(user_input == "2"):
        cleanedUserData = cleanUserData(frame_Usernames)
        write_json(storage_UserNames, cleanedUserData)
        print("\n Scraped user data has been cleaned for inconsistencies")
        return
    
    if(user_input == "3"):
        print(f"\n We have scraped {len(frame_Usernames.keys())} datasets")
        return
    
    if(user_input == "4"):
        standardizedUserData = standardizeUserData(frame_Usernames)
        write_json(storage_UserNames, standardizedUserData)
        print("\n Scraped user data has been standardized for for consistent outlook")
        return
    
    if(user_input == "1"):
        pass
    else:
        print("\nInvalid Action digit ")
        return



    cl = Client()
    if(criticalCheckpoint1):
        print("\n --- Checkpoint 1 passed")

        if settings_path.exists() and settings_path.stat().st_size > 0: # Load settings BEFORE login
            try:
                cl.load_settings(settings_path)
                try:
                    cl.account_info()  # or cl.user_info_v1(cl.user_id)
                    criticalCheckpoint2 = True
                except Exception as errors:
                    # session expired → full login
                    try:
                        cl.login(ACCOUNT_USERNAME, ACCOUNT_PASSWORD) # login to agent account  | Login only if needed
                        print("\n 1 i logged in")
                        cl.dump_settings(settings_path)
                        print("\n 1 i dumped")
                        criticalCheckpoint2 = True
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
                print("\n 3 i logged in")
                cl.dump_settings(settings_path)
                print("\n 3 i dumped")
                criticalCheckpoint2 = True
            except Exception as err:
                print(f"\n -- 3 Log in error at --> {err}")
                timeOutError = str(err)
                for i in error_cage:
                    if i in str(err):
                        timeOutError = i
    else:
        print("---------\n ---- Could not Log into your scraping agent \n--------")
        pass

    if(criticalCheckpoint2): # access user deets
        print("\n --- Checkpoint 2 passed")
        print("\n--- Stalling after  login ---")
        human_sleep("normal",3)
        stop = False

        for keys in frame_Usernames:
            if(stop):
                break
            else:
                pass
            userID = frame_Usernames[keys]["pk"]
            username = frame_Usernames[keys]["username"]
            lastTimeUpdated = frame_Usernames[keys]["lastUpdate"]
            lastTimeUpdated_ = (date.fromisoformat(lastTimeUpdated)) if (lastTimeUpdated != "") else (today)
            delta = today - lastTimeUpdated_ #(lastTimeUpdated if (lastTimeUpdated != "") else today)
            days_between = int(delta.days)
            
            if(userID != ""):
                #print("\n 1: i got here")
                if((today != lastTimeUpdated and (lastTimeUpdated == "")) or (days_between >= userDataDaysRefresh)): # (today != lastTimeUpdated) or 
                    #print("\n 2: i got here")
                    try:
                        userData = cl.user_info(userID).model_dump()
                        frame_Usernames[keys] = runUsernameProfiles(frame_Usernames[keys],userData)
                        frame_Usernames[keys]["lastUpdate"] = str(today)
                        write_json(storage_UserNames,frame_Usernames)
                        print(f"\n--Parsed for user --> {username}")
                    except Exception as err:
                        if (str(err) in error_ignore):
                            stop = False
                            frame_Usernames[keys]["lastUpdate"] = str(today)
                            write_json(storage_UserNames,frame_Usernames)
                        else:
                            stop = True
                        
                        print(f"\n1 Encountered error at user info --> {err}")
                        timeOutError = str(err)
                        for i in error_cage:
                            if i in str(err):
                                timeOutError = i

                    human_sleep("safe",2)
                        
        print("\nEnd program") 



    
    if(criticalCheckpoint1):
        agents[agentsType][agentIndex]["lastTimeUsed"] = str(today)
        agents[agentsType][agentIndex]["timeOutError"] = timeOutError
        write_json(agents_ ,agents)
    else:
        pass

    print("Done with program")



if __name__ == "__main__":
    main()


