
from instagrapi import Client

from program_env.utilities.jsonUtils import (
    create_json_if_not_exists,
    read_json,
    write_json,
    delete_json
)

from program_env.utilities.timeUtils import (
    human_sleep,
    countdown_inline,
    reset_rate_limits
)

from program_env.utilities.agencyUtils import (
    runAgency,
    in_error_cage,
    is_user_not_found,
    login_manager,
    logout_manager,
    resolve_exit_reason,
)

from program_env.utilities.userDataUtils import (
    runUsernameProfiles,
    cleanUserData,
    standardizeUserData,
    normalize_user,
    sanitize_text
)

from pathlib import Path
from datetime import date

#import traceback






  

BASE_DIR = Path(__file__).resolve().parents[4]
error_cage = ["challengeresolve","pinned_channels_info","login_required","checkpoint_required","checkpoint","checkpoint required"]
error_ignore = ["user not found"]
error_cage_with_limit = []

# "ChallengeResolve"--> end program
# "User not found" delete this user data and continue


AGENTS_NUMBER_TO_USE_IF_I_WANT_TO = 0   # from 1 upwards



def main() -> None:


    def mark_network_failure():
        nonlocal stop, timeOutError
        stop = True
        timeOutError = "network_failure"

    
    print("Running socials-sniffer userProfile collector")


    criticalCheckpoint1,criticalCheckpoint2 = False,False

    ACCOUNT_USERNAME,ACCOUNT_PASSWORD,lastTimeUsed,timeOutError = "","","",""
    today = date.today() #today # year, month, day




    # All scraped userNames Json data amd assigned variables
    
    storage_UserNames = BASE_DIR / "program_env" / "instagram" / "data_collectors" / "storage" / "raw-data" / "all-scraped-user-data.json"
    create_json_if_not_exists(storage_UserNames)
    frame_Usernames = read_json(storage_UserNames)

    storage_exterminate = BASE_DIR / "program_env" / "instagram" / "data_collectors" / "storage" / "raw-data" / "exterminate.json"
    create_json_if_not_exists(storage_exterminate)
    users_exterminate = read_json(storage_exterminate)

    premature_ = BASE_DIR / "program_env" / "instagram" / "data_collectors" / "storage" / "raw-data" / "kill.json"
    create_json_if_not_exists(premature_, {"stop": False})
    premature = read_json(premature_)



    if("exterminate" not in users_exterminate):
        users_exterminate = {"exterminate":[]}


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


    

    


    settings_path = BASE_DIR / "program_env" / "utilities" / "agents" / "sessions" / f"{ACCOUNT_USERNAME}.json" # Create settings file per agent
    #create_json_if_not_exists(settings_path)

    today = date.today() #today # year, month, day
    userDataDaysRefresh = 5 # Users are re-checked every x days

    stop = False



    print("\n - Action: Scrape for user Profile data with 1")
    print("\n - Action: Clean scraped user Profile data for inconsistencies with 2")
    print("\n - Action: Check how many users have been scraped with 3")
    print("\n - Action: Standardized user profile data keys for conformity with 4")
    print("\n - Action: Sanitize biography with 5")
    print("\n - Action: Sanitize full name with 6")
    print("\n - Action: Sanitize comments with 7")
    user_input = input("\nEnter action number: ")
    
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
    
    if(user_input == "5"):
        for keys,values  in frame_Usernames.items():
            text = values["biography"]
            sanitizes = sanitize_text(text)
            values["biography"] = sanitizes

        
        write_json(storage_UserNames, frame_Usernames)
        print("\n Scraped user data biography has been sanitized for a consistent outlook")
        return
    
    if(user_input == "6"):
        for keys,values  in frame_Usernames.items():
            text = values["full_name"]
            sanitizes = sanitize_text(text)
            values["full_name"] = sanitizes

        
        write_json(storage_UserNames, frame_Usernames)
        print("\n Scraped user data full name has been sanitized for a consistent outlook")
        return
    
    if(user_input == "7"):
        for keys,values  in frame_Usernames.items():
            comments = values["comments"]
            assign = []
            if(len(comments) >= 1):
                for text in comments:
                    sanitizes = sanitize_text(text)
                    assign.append(sanitizes)
            values["comments"] = assign

        
        write_json(storage_UserNames, frame_Usernames)
        print("\n Scraped user data comments has been sanitized for a consistent outlook")
        return
    
    if(user_input == "1"):
        pass
    else:
        print("\nInvalid Action digit ")
        return



    

    

    cl = Client()
    if(criticalCheckpoint1):
        print("\n --- Checkpoint 1 passed")

        

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
            criticalCheckpoint2 = False
        else:
            criticalCheckpoint2 = True

        print("🚀 Logged in, continuing scraper...")
    else:
        print("---------\n ---- Could not Log into your scraping agent \n--------")
        pass



    if(criticalCheckpoint2): # access user deets
        print("\n --- Checkpoint 2 passed")
        print("\n--- Stalling after  login ---")
        #human_sleep("normal",3)
        human_sleep("normal", 3, reset_callback=reset_rate_limits,on_suspend=mark_network_failure)
        

        # Exterminate nreacheable users
        if(len(users_exterminate["exterminate"]) >= 1):
            for users in users_exterminate["exterminate"]:
                print(f"\n -- purging user {users} from user datasets --- ")
                if(users in frame_Usernames):
                    del frame_Usernames[users]

            print(f"\n -- No more users to exterminate --- ")
            users_exterminate["exterminate"] = []
            write_json(storage_exterminate,users_exterminate)

        for keys in frame_Usernames:
            premature = read_json(premature_)["stop"]
            if(stop) or (premature):
                print("\n -- Ending program due to 'stop' / 'premature' initiation -- ")
                break
            else:
                pass
            userID = frame_Usernames[keys]["pk"]
            username = frame_Usernames[keys]["username"]
            lastTimeUpdated = frame_Usernames[keys]["lastUpdate"]
            lastTimeUpdated_ = (date.fromisoformat(lastTimeUpdated)) if (lastTimeUpdated != "") else (today)
            delta = today - lastTimeUpdated_ #(lastTimeUpdated if (lastTimeUpdated != "") else today)
            days_between = int(delta.days)
            user = ""
            source = ""

            error1 = False
            error2 = False
            error3 = False

            errors = ""
            
            if(userID != ""):
                needrefresh = (today != lastTimeUpdated and (lastTimeUpdated == "")) or (days_between >= userDataDaysRefresh)
                if(needrefresh): # (today != lastTimeUpdated) or 
                    #print("\n 2: i got here")

                    human_sleep("normal",2,reset_callback=reset_rate_limits,on_suspend=mark_network_failure)

                    try:
                        user = cl.user_info(userID)                 # GQL / richest
                        source = "gql"
                    except Exception as e1:
                        errors = (str(e1)).replace("'","").strip(" ").lower()
                        error1 = True
                        print(f"user_info failed for {username}: {errors}")
                        countdown_inline(60, reset_callback=reset_rate_limits,on_suspend=mark_network_failure)

                        hit = in_error_cage(errors, error_cage)
                        if hit:
                            stop = True
                            timeOutError = hit
                            print(f"🛑 Critical error hit: {hit} — stopping run")
                            break

                        if "validation errors" in errors:
                            print(f"⚠️ Partial user object for {username} — skipping user")
                            continue

                    if(is_user_not_found(errors)):
                        users_exterminate["exterminate"].append(username)
                        write_json(storage_exterminate,users_exterminate)


                    if(error1 and not is_user_not_found(errors)): 
                        try:
                            user = cl.user_info_v1(userID)           # legacy / stable
                            source = "v1"
                        except Exception as e2:
                            errors = (str(e2)).replace("'","").strip(" ").lower()
                            error2 = True
                            print(f"user_info_v1 failed for {username}: {errors}")
                            countdown_inline(80, reset_callback=reset_rate_limits,on_suspend=mark_network_failure)

                            hit = in_error_cage(errors, error_cage)
                            if hit:
                                stop = True
                                timeOutError = hit
                                print(f"🛑 Critical error hit: {hit} — stopping run")
                                break

                            if "validation errors" in errors:
                                print(f"⚠️ Partial user object for {username} — skipping user")
                                continue
                    

                    if(error2 and not is_user_not_found(errors)):
                        try:
                            user = cl.user_info_by_username(username)  # last-resort
                            source = "by_username"
                        except Exception as e2:
                            errors = (str(e2)).replace("'","").strip(" ").lower()
                            #error3 = True
                            print(f"user_info_v1 failed for {username}: {errors}")
                            countdown_inline(80, reset_callback=reset_rate_limits,on_suspend=mark_network_failure)

                            hit = in_error_cage(errors, error_cage)
                            if hit:
                                stop = True
                                timeOutError = hit
                                print(f"🛑 Critical error hit: {hit} — stopping run")
                                break

                            if "validation errors" in errors:
                                print(f"⚠️ Partial user object for {username} — skipping user")
                                continue


                    if(user):
                        
                        userDetails = normalize_user(user)
                        #print(f"\n this user: --> {userData}")
                        frame_Usernames[keys] = runUsernameProfiles(frame_Usernames[keys],userDetailsFromApi_=userDetails) # userData
                        frame_Usernames[keys]["lastUpdate"] = str(today)
                        frame_Usernames[keys]["source"] = source
                        write_json(storage_UserNames,frame_Usernames)
                        print(f"\n--Parsed for user --> {username} with source --> {source}")
                    
                        #frame_Usernames[keys]["lastUpdate"] = str(today)
                        #write_json(storage_UserNames,frame_Usernames)


                    human_sleep("safe",1,reset_callback=reset_rate_limits,on_suspend=mark_network_failure)
                    timeOutError = errors


        
                        
        print("\nEnd program") 



    
    if(criticalCheckpoint1):
        agents[agentsType][agentIndex]["lastTimeUsed"] = str(today)
        agents[agentsType][agentIndex]["timeOutError"] = timeOutError
        write_json(agents_ ,agents)
    else:
        pass

    exit_reason = resolve_exit_reason(timeOutError=timeOutError,stop=stop,)
    logout_manager(cl=cl,reason=exit_reason,settings_path=settings_path,)



    print("Done with program")



if __name__ == "__main__":
    main()


