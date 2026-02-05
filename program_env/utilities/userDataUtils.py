
import re
import copy



import unicodedata


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

#standard = ["",None,"UNKNOWN"]


def normalize_user(user)-> dict:
    if hasattr(user, "model_dump"):
        return user.model_dump()
    if hasattr(user, "dict"):
        return user.dict()
    if isinstance(user, dict):
        return user
    raise TypeError(f"Unexpected user type: {type(user)}")

"""
def normalize_user(user: Any) -> Dict[str, Any]:
    
    #Normalize any Instagram user object into a safe, frame-compatible dict.
    #Missing fields are filled with defaults from `frame`.
   

    # Step 1: Convert to dict
    if hasattr(user, "model_dump"):
        raw = user.model_dump()
    elif hasattr(user, "dict"):
        raw = user.dict()
    elif isinstance(user, dict):
        raw = user
    else:
        raise TypeError(f"Unexpected user type: {type(user)}")

    # Step 2: Start from a clean frame (guaranteed schema)
    normalized = copy.deepcopy(frame)

    # Step 3: Overlay only known keys
    for key in normalized.keys():
        if key in raw and raw[key] is not None:
            normalized[key] = raw[key]

    return normalized
"""
    
def sanitize_text(text: str) -> str:
    """
    Convert fancy unicode text (fonts, emojis, symbols) into clean readable text.
    Intended for Instagram bios, names, captions, etc.
    """

    if not text:
        return ""

    # 1. Normalize unicode (turn fancy fonts into closest ASCII)
    text = unicodedata.normalize("NFKD", text)

    # 2. Remove emojis & non-text symbols
    text = re.sub(
        r"["
        r"\U0001F300-\U0001F5FF"  # symbols & pictographs
        r"\U0001F600-\U0001F64F"  # emoticons
        r"\U0001F680-\U0001F6FF"  # transport & map
        r"\U0001F700-\U0001F77F"
        r"\U0001F780-\U0001F7FF"
        r"\U0001F800-\U0001F8FF"
        r"\U0001F900-\U0001F9FF"
        r"\U0001FA00-\U0001FAFF"
        r"\u2600-\u26FF"          # misc symbols
        r"\u2700-\u27BF"
        r"]+",
        "",
        text
    )

    # 3. Remove remaining non-ASCII characters
    text = text.encode("ascii", "ignore").decode()

    # 4. Normalize whitespace
    text = re.sub(r"\s+", " ", text)

    return text.strip()





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
    dictionary = copy.deepcopy(dictionary_)

    for userData in dictionary:
        if(len(dictionary[userData]["comments"]) != 0):
            comments = feedUniqueness(dictionary[userData]["comments"])
            dictionary[userData]["comments"] = comments

        #dictionary[userData]["full_name"] = feedUniqueness(list(dictionary[userData]["full_name"]))

    return dictionary



def standardizeUserData(dictionary_:dict) -> dict:
    dictionary = copy.deepcopy(dictionary_)

    frame_expected = copy.deepcopy(frame)
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

    frame_Usernames = copy.deepcopy(userData_)
    details = (copy.deepcopy(mediaDetails_["user"])) if ("user" in mediaDetails_) else (copy.deepcopy(mediaDetails_))
    edge = ["", None]


    
    
    #print(f"\n -- This is what we have in our details: {details}")

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

    if(username in frame_Usernames):
        #print("\n Because it already exists, we skipp it on to the next")
        pass
    elif((username not in frame_Usernames)):
        #print("\n User doesn't exist, creating frame for it")
        frame_Usernames[username] =  copy.deepcopy(frame)



        if (frame_Usernames[username]["username"] == ""):
            frame_Usernames[username]["username"] = username
        else:
            pass

        if (frame_Usernames[username]["pk"] == ""):
            frame_Usernames[username]["pk"] = pk
        else:
            pass

        if (frame_Usernames[username]["full_name"] == ""):
            frame_Usernames[username]["full_name"] = sanitize_text(full_name)
        else:
            pass
        
        if (frame_Usernames[username]["is_private"] in edge):
            frame_Usernames[username]["is_private"] = is_private
        else:
            pass
        
        if (frame_Usernames[username]["is_verified"] in edge):
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
        
        if (frame_Usernames[username]["is_business"] in edge):
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
            # sanitize comment texts then append
            
            if(isinstance(comments, str)):
                santitized_comment = sanitize_text(comments)
                frame_Usernames[username]["comments"].append(santitized_comment)
            elif(isinstance(comments,list)):
                for i in comments:
                    santitized_comment = sanitize_text(i)
                    frame_Usernames[username]["comments"].append(santitized_comment)
        else:
            pass

        frame_Usernames[username]["comments"] = feedUniqueness(frame_Usernames[username]["comments"])

    #print(f"\n -- 2 This is what is in frame[{username}]: {frame_Usernames[username]} | This is  details: {details}")

    #print(f"\n -- 3 This is what is in the new last spot in frame[{list(frame_Usernames)[-1]}]: {frame_Usernames[list(frame_Usernames)[-1]]}")

    

    return frame_Usernames


def channelsAndLinksUniqueness(mainData_:list,subData_:list, key1="", key2="", key3="",typeD="channel")-> list:
    mainData = copy.deepcopy(mainData_)
    subData = copy.deepcopy(subData_)


    existing_keys = set()

    if(typeD == "channel"):
        for ch in mainData:
            title = ch.get(key1, "")
            subtitle = ch.get(key2, "")
            invite = ch.get(key3, "")
            existing_keys.add((title, subtitle, invite))

        for data in subData:
            new_key = (
                data.get(key1, ""),
                data.get(key2, ""),
                data.get(key3, ""),
            )
            if new_key not in existing_keys:
                mainData.append({key1:data.get(key1, ""),key2:data.get(key2, ""),key3:data.get(key3, ""),"number_of_members":data.get("number_of_members", 0)})
                existing_keys.add(new_key)

    elif (typeD == "bioLinks"):
        for ch in mainData:
            url = ch.get(key1, "")
            title = ch.get(key2, "")
            existing_keys.add((url, title))

        for data in subData:
            new_key = (
                data.get(key1, ""),
                data.get(key2, "")
            )
            if new_key not in existing_keys:
                mainData.append({key1:data.get(key1, ""),key2:data.get(key2, "")})
                existing_keys.add(new_key)


    return mainData



def runUsernameProfiles(    userDataFromLocal_: dict, userDetailsFromApi_: dict,)-> dict:

    userData = copy.deepcopy(userDataFromLocal_)  or {} # my own schema
    userDetails = copy.deepcopy(userDetailsFromApi_)  or {}# the data from instagram
    


    for keys in userData:

        if keys == "pinned_channels_info":
            continue
        

 
        if keys in userDetails and keys not in {"broadcast_channels","pinned_channels_info","source"}:
            if(keys in {"biography","full_name"}):
                userData[keys] = sanitize_text(userDetails[keys])
            else:
                userData[keys] = userDetails[keys]


        if(keys == "bio_links_url"): # 'bio_links' --> open list --> grab {'url','title'}
            if("bio_links" in userDetails):
                bio_links = userDetails.get("bio_links",[])
                if((isinstance(bio_links, list))):
                    bio = channelsAndLinksUniqueness(userData["bio_links_url"],bio_links, "url", "title", typeD="bioLinks")
                    userData["bio_links_url"] = bio
                else:
                    pass


        if(keys == "broadcast_channels"): #  broadcast_channels ! need to see how it is gotten
            channelData = []
            

            if("broadcast_channel" in userDetails):
                bc = userDetails.get("broadcast_channel",{})
                if(isinstance(bc, dict)):
                    if ("channels" in bc) and (isinstance(bc["channels"],list)):
                        channelData = bc.get("channels",[])
                elif isinstance(bc, list):
                    channelData = bc
            elif ("pinned_channels_info" in userDetails):
                pci = userDetails.get("pinned_channels_info",{})
                if isinstance(pci, dict):
                    if ("channels" in pci) and isinstance(pci["channels"], list):
                        channelData = pci["channels"]
                    elif "broadcast_channel" in pci and isinstance(pci["broadcast_channel"], list):
                        channelData = pci["broadcast_channel"]
                elif isinstance(pci, list):
                    channelData = pci



            if((len(channelData) != 0) and (isinstance(channelData, list))):
                broadcast = channelsAndLinksUniqueness(userData["broadcast_channels"],channelData,  "title", "subtitle", "invite_link", typeD="channel")
                userData["broadcast_channels"] = broadcast
            else:
                pass


    return userData


    