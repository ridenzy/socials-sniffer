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
    runUsernameFrames,
    standardizeUserData
)

from pathlib import Path
from datetime import date





BASE_DIR = Path(__file__).resolve().parents[4]
error_cage = ["ChallengeResolve"]

AGENTS_NUMBER_TO_USE_IF_I_WANT_TO = 0   # from 1 upwards








def main() -> None:
    print("Running socials-sniffer userProfile collector")


    criticalCheckpoint1,criticalCheckpoint2,criticalCheckpoint3 = False,False,False

    ACCOUNT_USERNAME,ACCOUNT_PASSWORD,lastTimeUsed,timeOutError = "","","",""
    TARGET_USERMEDIA_PK,TARGET_USERMEDIA_PK_ID = "",""
    today = date.today() #today # year, month, day
    userMediaLikers,userMediaCommenters = [],[]




    # All scraped mediaID Json data amd assigned variables
    storage_MediaID = BASE_DIR / "program_env" / "instagram" / "data_collectors" / "storage" / "raw-data" / "all-scraped-users-media-id.json"
    create_json_if_not_exists(storage_MediaID)
    frame = read_json(storage_MediaID)


    # All scraped userNames Json data amd assigned variables
    storage_UserNames = BASE_DIR / "program_env" / "instagram" / "data_collectors" / "storage" / "raw-data" / "all-scraped-user-data.json"
    create_json_if_not_exists(storage_UserNames)
    frame_Usernames = read_json(storage_UserNames)

    # My agents Json Data and assigned variables
    agents_ = BASE_DIR / "program_env" / "utilities" / "agents" / "agents.json"
    create_json_if_not_exists(agents_)
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
    #"""

    """
    agentIndex = AGENTS_NUMBER_TO_USE_IF_I_WANT_TO - 1
    criticalCheckpoint1 = True
    ACCOUNT_USERNAME,ACCOUNT_PASSWORD = "fabio.styled","Jv9q6!8jx$Gda!!ak"
    """

    


    settings_path = BASE_DIR / "program_env" / "utilities" / "agents" / "sessions" / f"{ACCOUNT_USERNAME}.json" # Create settings file per agent
    #create_json_if_not_exists(settings_path)


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
                        #cl.login("armani.styled","@2EH2dEJv9q")
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
                #cl.login("fabio.styled","Jv9q6!8jx$Gda!!ak")
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


    if(criticalCheckpoint2): # access media  and act for Likers
        print("\n --- Checkpoint 2 passed")
        print("\n--- Stalling after  login ---")
        human_sleep("normal",3)
        stop = False
        
        for keys in frame:
            if(not frame[keys]["is_used"]):
                if(stop):
                    break
                else:
                    pass
                try:
                    if("id" in frame[keys]):
                        TARGET_USERMEDIA_PK_ID = frame[keys]["id"]
                    else:
                        try:
                            TARGET_USERMEDIA_PK = cl.media_pk_from_code(code=keys)
                        except Exception as err:
                            print(f"\n -- 1 ID error at level - TARGET_USERMEDIA_PK --> {err}")
                            timeOutError = str(err)
                            for i in error_cage:
                                if i in str(err):
                                    timeOutError = i
                        
                        if(TARGET_USERMEDIA_PK != ""):
                            try:
                                TARGET_USERMEDIA_PK_ID = cl.media_id(media_pk=TARGET_USERMEDIA_PK)
                            except Exception as err:
                                print(f"\n -- 2 ID error at level- TARGET_USERMEDIA_PK_ID ---> {err}")
                                timeOutError = str(err)
                                for i in error_cage:
                                    if i in str(err):
                                        timeOutError = i
                    
                    if(TARGET_USERMEDIA_PK_ID != ""):
                        for Liker in cl.media_likers(media_id=TARGET_USERMEDIA_PK_ID):
                            try:
                                userMediaLikers.append(Liker)
                            except Exception as err:
                                print(f"\n Error --> Could not add user who Liked post {err} --- ")

                        print("\n--- After checking for likes ---")
                        human_sleep("safe",2)

                        for commenter in cl.media_comments(media_id=TARGET_USERMEDIA_PK_ID):
                            try:
                                userMediaCommenters.append(commenter)
                            except Exception as err:
                                print(f"\n Error --> Could not add user who commented post {err} --- ")



                        for details in userMediaCommenters:
                            details = details.dict()
                            frame_Usernames = runUsernameFrames(frame_Usernames,details)
                            #print(f"\n Commenters info {details}")

                        for details in userMediaLikers:
                            details = details.dict()
                            frame_Usernames = runUsernameFrames(frame_Usernames,details)
                            #print(f"\n Likers info {details}")
                        


                        write_json(storage_UserNames,frame_Usernames)
                        frame[keys]["is_used"] = True
                        write_json(storage_MediaID,frame)
                        criticalCheckpoint3 = True


                        #stop = (True) if (len(userMediaCommenters) != 0) else (False)
                    else:
                        print("\n --no TARGET_USERMEDIA_PK_ID detected")
                        break
                    
                    print("\n--- After checking for comments and likes ---")
                    human_sleep("safe",1)

                            
                    #criticalCheckpoint3 = True
                except Exception as err:
                    print(f"\n --checkpoint 2 error --> {err} -- for {ACCOUNT_USERNAME}")
                    timeOutError = str(err)
                    for i in error_cage:
                        if i in str(err):
                            timeOutError = i
                    stop = True
            else:
                pass
    else:
        pass

    if(criticalCheckpoint3):
        standardizedUserData = standardizeUserData(frame_Usernames)
        write_json(storage_UserNames, standardizedUserData)
        print("\n Scraped user data has been standardized for for consistent outlook")
        #return

        

    if(criticalCheckpoint1):
        agents[agentsType][agentIndex]["lastTimeUsed"] = str(today)
        agents[agentsType][agentIndex]["timeOutError"] = timeOutError
        write_json(agents_ ,agents)
    else:
        pass

    print("Done with program")

    #cl.logout()
    



if __name__ == "__main__":
    main()


