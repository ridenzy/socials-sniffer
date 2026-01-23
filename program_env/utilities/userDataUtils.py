




        
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

    if ("id" in details):
        user_id = details["id"]
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
        frame_Usernames[username] = {
            "username":"",
            "pk":"",
            "user_id":"",
            "full_name":"",
            "is_private":"",
            "is_verified":"",
            "is_business":"",
            "follower_count":"",
            "following_count":"",
            "biography":"",
            "media_count":"",
            "comments":[],
            "email":""

        }
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

    if (frame_Usernames[username]["user_id"] == ""):
        frame_Usernames[username]["user_id"] = user_id
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
    

    return frame_Usernames
