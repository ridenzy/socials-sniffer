
import re


frame = {
    "username":"",   # --- 'username'
    "pk":"",         # --- 'pk'
    "full_name":"",  # 'full_name'
    "is_private":"", # 'is_private
    "is_verified":"", # 'is_verified'
    "is_business":"", # 'is_business'
    "follower_count":"", # 'follower_count'
    "following_count":"", # 'following_count'
    "biography":"",        # 'biography'
    "media_count":"", # 'media_count'
    "comments":[],
    "public_email":"", # 'public_email'
    "bio_links_url":[], # 'bio_links' --> open list --> grab {'url','title'}
    "broadcast_channels":[], #  broadcast_channels ! need to see how it is gotten
    "contact_phone_number":"",  # contact_phone_number
    "public_phone_country_code": "",  # public_phone_country_code
    "public_phone_number": "",  # public_phone_number
    "business_contact_method": "", # business_contact_method
    "business_category_name": "", # business_category_name
    "category_name": "", # category_name
    "category": "", # category
    "lastUpdate":"" 

}

standard = ["",None,"UNKNOWN"]



def feedUniqueness(data_: list) -> list:
    # Regex pattern to remove emojis & symbols
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F700-\U0001F77F"
        "\U0001F780-\U0001F7FF"
        "\U0001F800-\U0001F8FF"
        "\U0001F900-\U0001F9FF"
        "\U0001FA00-\U0001FAFF"
        "\u2600-\u26FF"          # misc symbols
        "\u2700-\u27BF"
        "]+",
        flags=re.UNICODE
    )

    cleaned = []
    seen = set()

    for item in data_:
        if not isinstance(item, str):
            continue

        # Remove emojis
        cleaned_item = emoji_pattern.sub("", item).strip()

        # Skip empty strings after cleaning
        if not cleaned_item:
            continue

        # Remove duplicates while preserving order
        if cleaned_item not in seen:
            seen.add(cleaned_item)
            cleaned.append(cleaned_item)

    return cleaned



def cleanUserData(dictionary_:dict) -> dict:
    dictionary = dictionary_

    for userData in dictionary:
        if(len(dictionary[userData]["comments"]) != 0):
            comments = feedUniqueness(dictionary[userData]["comments"])
            dictionary[userData]["comments"] = comments

        #dictionary[userData]["full_name"] = feedUniqueness(list(dictionary[userData]["full_name"]))

    return dictionary



def standardizeUserData(dictionary_:dict) -> dict:
    dictionary = dictionary_

    frame_expected = frame
    keys_to_delete = {}

    # Standardize the frame

    for keys in dictionary:
        keys_to_delete[keys] = []
        
        for frameKeys in frame_expected:
            if frameKeys not in dictionary[keys]:
                dictionary[keys][frameKeys] = frame_expected[frameKeys]

        for frameKeys in dictionary[keys]:
            if frameKeys not in frame_expected:
                keys_to_delete[keys].append(frameKeys)

    for keys in keys_to_delete:
        #print(f"\n Keys to delete: {keys} | Values to delete: {keys_to_delete[keys]}")
        for values in keys_to_delete[keys]:
            del dictionary[keys][values]


    return dictionary



def runUsernameFrames(userData_ = {},mediaDetails_ = {}) -> dict:
    frame_Usernames = userData_
    details = (mediaDetails_["user"]) if ("user" in mediaDetails_) else (mediaDetails_)

    username,pk,user_id,full_name,is_private,is_verified,is_business,follower_count,following_count,biography,media_count = "","","","",False,False,False,0,0,"",0

    comments = ""
    # Start grabbing user details data

    if ("username" in details):
        username = details["username"]
    else:
        pass

    if ("pk" in details):
        pk = details["pk"]
    else:
        pass


    if ("full_name" in details):
        full_name = details["full_name"]
    else:
        pass

    if ("is_private" in details):
        is_private = details["is_private"]
    else:
        pass

    if ("is_verified" in details):
        is_verified = details["is_verified"]
    else:
        pass

    if ("follower_count" in details):
        follower_count = details["follower_count"]
    else:
        pass

    if ("following_count" in details):
        following_count = details["following_count"]
    else:
        pass

    if ("is_business" in details):
        is_business = details["is_business"]
    else:
        pass

    if ("biography" in details):
        biography = details["biography"]
    else:
        pass

    if ("media_count" in details):
        media_count = details["media_count"]
    else:
        pass

    if ("text" in mediaDetails_):
        comments = mediaDetails_["text"]
    else:
        pass







    # Start storage setting 

    if(username not in frame_Usernames):
        frame_Usernames[username] = frame
    else:
        pass

    if (frame_Usernames[username]["username"] == ""):
        frame_Usernames[username]["username"] = username
    else:
        pass

    if (frame_Usernames[username]["pk"] == ""):
        frame_Usernames[username]["pk"] = pk
    else:
        pass

    if (frame_Usernames[username]["full_name"] == ""):
        frame_Usernames[username]["full_name"] = full_name
    else:
        pass
    
    if (frame_Usernames[username]["is_private"] == ""):
        frame_Usernames[username]["is_private"] = is_private
    else:
        pass
    
    if (frame_Usernames[username]["is_verified"] == ""):
        frame_Usernames[username]["is_verified"] = is_verified
    else:
        pass
    
    if (frame_Usernames[username]["follower_count"] == ""):
        frame_Usernames[username]["follower_count"] = follower_count
    else:
        pass
    
    if (frame_Usernames[username]["following_count"] == ""):
        frame_Usernames[username]["following_count"] = following_count
    else:
        pass
    
    if (frame_Usernames[username]["is_business"] == ""):
        frame_Usernames[username]["is_business"] = is_business
    else:
        pass
    
    if (frame_Usernames[username]["biography"] == ""):
        frame_Usernames[username]["biography"] = biography
    else:
        pass
    
    if (frame_Usernames[username]["media_count"] == ""):
        frame_Usernames[username]["media_count"] = media_count
    else:
        pass

    if(len(comments) >= 1):
        frame_Usernames[username]["comments"].append(comments)
    else:
        pass

    frame_Usernames[username]["comments"] = feedUniqueness(frame_Usernames[username]["comments"])

    

    return frame_Usernames




def runUsernameProfiles(userDataFromLocal_:dict = {},userDetailsFromApi_:dict = {}) -> dict:
    userData = userDataFromLocal_ 
    userDetails = userDetailsFromApi_

    for keys in userData:
        if((keys in userDetails) and (keys != "broadcast_channels")):
            userData[keys] = userDetails[keys]
        elif(keys == "bio_links_url"): # 'bio_links' --> open list --> grab {'url','title'}
            for data in list(userDetails["bio_links"]):
                userData[keys].append({"url":data["url"],"title":data["title"]})
        elif(keys == "broadcast_channels"): #  broadcast_channels ! need to see how it is gotten
            for data in list(userDetails["broadcast_channel"]):
                userData[keys].append({"title":data["title"],"subtitle":data["subtitle"],"invite_link":data["invite_link"],"number_of_members":data["number_of_members"]})

    return userData

    