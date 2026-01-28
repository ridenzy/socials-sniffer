
import sys
from datetime import date




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
    timeOutError = agents[agentsType][agentIndex]["timeOutError"]
    

    today = date.today() #today # year, month, day
    delta = today - (lastTimeUsed if (lastTimeUsed != "") else today)
    days_between = int(delta.days)
    agentDaysRefresh = 5
    #print(f"\n -- {days_between} --")

    if((timeOutError != "") or ((days_between <= agentDaysRefresh) and (today != lastTimeUsed) and (lastTimeUsed != "")) or ((today == lastTimeUsed) and days_between == 0)):
        if(timeOutError != ""):
            print(f"\n --- Unresolved Timeout Error issue in JSON file --> agents.json | for Agent username --> {ACCOUNT_USERNAME}")
        elif(lastTimeUsed != ""):
            print(f"\nAgent still in it's refresh phase with {days_between} out of {agentDaysRefresh} days left | for Agent username --> {ACCOUNT_USERNAME}")
        criticalCheckpoint1 = False
    else:
        criticalCheckpoint1 = True


    if(criticalCheckpoint1):
        print(f"\nFound adequate agent to use  -->  {ACCOUNT_USERNAME} | {ACCOUNT_PASSWORD}")
        agency = {"ACCOUNT_USERNAME":ACCOUNT_USERNAME, "ACCOUNT_PASSWORD":ACCOUNT_PASSWORD, "lastTimeUsed":lastTimeUsed, "timeOutError":timeOutError,"checkPoint":True,"agentIndex":agentIndex}
        #countdown(10)

    #print("\n\n ---------------------------------------- ")

    return agency
    
            


def runAgency(setAgentsNumberToUse_=0,agentsType_="SCRAPING_AGENTS",agents_={}) -> dict:
    number = setAgentsNumberToUse_ # Set an agent manually based on number not index
    agentsType = agentsType_
    agents = agents_

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
