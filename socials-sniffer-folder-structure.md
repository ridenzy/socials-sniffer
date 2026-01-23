
schema: 
<username> <userID> <full name> <followers> <following> <bio> <is_private> <is_business> <is_verified> <location> <outreached_by ("brand1,brand2" etc)>  <media count>  <email> <is_professional>  <category_name> 

[

    {
        "username":"",
        "userID":"",
        "fullName":"",
        "followersCount":"",
        "followingCount":"",
        "mediaCount":"",
        "biography":"",
        "isPrivate":"",
        "isBusiness":"",
        "isProfessional":"",
        "isVerified":"",
        "email":"",
        "categoryName":"",
        "location":"",
        "outreachedBy":"kingsmaking101,trippleafits,concreteroyals"
    }

]




https://subzeroid.github.io/instagrapi/usage-guide/user.html
https://subzeroid.github.io/instagrapi/usage-guide/media.html



socials-sniffer/
    |-program-env/
        |-<social-media-site>/
            |-data-collectors/
                |-collectors/
                    |-<mediaID>.py #scrape media id from posts (likes and comments on a post)
                    |-<userProfile>.py #scrape users username from gotten media IDs 
                |-filters/
                    |-<brand name>.py # rules to follow when filtering users from raw to cleaned for this specific brand, also has its required metadata
                |-raw/
                    |-<all-scraped-users>.json # all scraped users gotten from the scraped users ( liked posts, commented posts, e.t.c )
                    |-<all-scraped-users-media-id>.json # all scraped users media ids .... <user>:[{mediaid:, used_or_not:true/false}]
                |-cleaned/
                    |-<brandname>.json # automatically generated
        
    |-virtual-env/
    
    
    
    
    
    pipeline:(e.g; IG: -->  (scrape a main users media ID) --save to <all-scraped-users-media-id>.json--> (scrape users from the media ID) --save to <all-scraped-users>.json--> ( 


{
    
}


export {
    targetAudience:[
        {
            "username":"",
            "fullName":"",
        }
    ],
    suggestedMessages:{
        intros
        outros
        body ?
    }
}