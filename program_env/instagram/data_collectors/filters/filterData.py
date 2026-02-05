

from pathlib import Path

from program_env.utilities.jsonUtils import (
    create_json_if_not_exists,
    read_json,
    write_json,
)

from program_env.utilities.filterUtils import (
    captureDictKeyValues,
    generateKeywordCloud
)


BASE_DIR = Path(__file__).resolve().parents[4]



# Access  the 




def main() -> None:
    # All scraped userNames Json data amd assigned variables
    storage_UserNames = BASE_DIR / "program_env" / "instagram" / "data_collectors" / "storage" / "raw-data" / "all-scraped-user-data.json"
    create_json_if_not_exists(storage_UserNames)
    userData = read_json(storage_UserNames)

    # filter function queries


    # function call to get followers vs following amount
    # Function call to get email
    # Function call to filter for keywords in comments
    # Function calls to filter for public users
    # Function call to  filter for private users
    # Function call to filter for verified users
    # Function call to filter for business users
    # Function call to filter for media count


    # Function call to filter for keywords in biography 
    bio_keywords_list = captureDictKeyValues(userData,"biography")
    bio_keywords_cloud = generateKeywordCloud(bio_keywords_list)




    print("Done with program")








if __name__ == "__main__":
    main()


