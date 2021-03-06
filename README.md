This is Pyanimu. The structure was inspired by [Pymoe](https://github.com/ccubed/PyMoe) and [Osuapi](https://github.com/khazhyk/osuapi). The sync/async structure is very similar to Osuapi.

This is created to help folk like me who don't want to deal with XML anymore. It is a not perfect, non ideal library. For a more frequently used library I recommend Pymoe, but [Pymoe](https://github.com/ccubed/PyMoe) is sync only.

This is my first public library that I've shared with others. It was created for fun and for learning. Any feedback is always appreciated, but I may not be able to update it often.

When I get the time, I might add more than just myanimelist, this is why it is structured in this modular fashion. Feel free to give me a heads up about missing documentation as the MAL API documentation is...awful.

I apologize in advance if there is anything missing or implemented incorrectly.

I am ready to be roast.

##### Note, MAL is not available at this moment. There been saying that instead of bring it back up, they might bring up new api version. This is unknown sources. So at this moment, Anilist is working.

## Requirement Libs:
```
BeautifulSoup, LXML
and either Aiohttp or Requests depending on what you need for.
```

___

# Mal (unavailable atm)
To create an instance.
```python
from pyanimu import Mal, connectors, Userstatus

con = connectors.ReqAnimu(user_agent = "Pyanimu") # or AioAnimu() for async

# Since every endpoint requires account expect one-two, therefore username/password isn't optional
mal = Mal(username, password,con)  
#it may return an object or list of an object depending on search queue.
manga_obj = mal.search_manga("DN Angel") 

#getting info from this data.
community_score = manga_obj.score #getting community score on it.

#want to update info to user list.
manga_obj.user_score = 7
manga_obj.user_status = UserStatus.completed
mal.update(manga_obj)


#Wanting to add anime to user list.
anime = mal.search_anime("Berserk")
for x in anime:
    if x.title == "Berserk":
        x.user_status = UserStatus.plantowatch #by default it will set plan to watch anyway
        data = mal.add(x)
        break

```

## using Async function
 
It is same as Sync function except search user which is aio_search_user.

```python 

con = connectors.AioAnimu()
mal = MAL(username, password,con)

async def get_data():
	anime_obj = await mal.search_anime("Trigun")
	user_obj = await mal.aio_search_user("Maverun") #Getting anime info about this user.
	#do stuff 
	

results = asyncio.get_event_loop().run_until_complete(get_data())

``` 

## Method to call
```python

verify():return boolean
search_anime(title):return object of an Anime. It may be an individual or list of an Anime Object.
search_manga(title):return object of Manga. It may be an individual or list of Manga object
aio_search_user(name): return User object. This is async function only.
req_search_user(name): return User object. This is sync function only.
add(obj): require Anime/Manga object to add it to their user list.
update(obj): require Anime/Manga object to update it to their user list.
delete(obj): require Anime/Manga object to delete it from their user list.
```

___

### Note: 
search_ prefix method only return itself object where user attributes related will be None, while running search user list
 for anime or manga will only return user fields. Since MAL API does not return both at once.  

<details>
 <summary>Anime</summary>
 
## From Search Anime.
```
id:int:Anime ID
title:string: Anime Title
english:string:Anime Title in English
synonyms:string: Different Anime Title
episodes:int: Anime's total episodes
type:string: TV,Movie,Ova etc
status:string: return either one of those [Airing, Finished Airing, Not yet aired]
start_date:string: yyyy-mm-dd date of first day airing.
end_date:string: yyyy-mm-dd date of finished airing.
synopsis:string: description of show.
image:string: url of anime's picture cover.
score:int: Average score from community.
```

## From User object only.
```
user_id:int: User ID from myanimelist
current_episode:int: current ep that user have watched.
date_start:string:yyyy-mm-dd date that user start watching it
date_finish:string:yyyy-mm-dd date that user have finished watching it.
user_score:int: a score that user give.
user_status: Status that user have put in. prefer accept UserStatus object, as int can be changed any time.
rewatch:int: How many time have user watched this anime already.
rewatch_ep:int: total episode including rewatched.
last_updated:string:
```

</details>

<details>
 <summary>Manga</summary>
 
## From Search Manga.
```
id:int:Manga ID
title:string: Manga Title
english:string:Manga Title in English
synonyms:string: Different Anime Title
chapters:int: Manga's total chapters 
volumes:int: Volume of total capters held.
score:int: Average score from community.
type:string: type of manga it is, [Manga,Novel,One-Shot] etc.
status: Status of this manga if it one of those [Publishing, Finished].
start_date:string: yyyy-mm-dd date of first day publish.
end_date:string: yyyy-mm-dd date of finished publish. 
synopsis:string: description of manga.
image:string:url of manga covered
```

## From User List.
```
user_id:int: User ID from myanimelist
read_chapters:int: current chapter that user is at
read_volumes:int: current volume that user is at
date_start:string:yyyy-mm-dd the date of user start reading
date_finish:string:yyyy-mm-dd the date of user finished reading
user_score:int:Score that user give to
user_status:int:Status that user give, recommend using UserStatus Object.
rereading:int: how many time have user reread it
rereading_chap:int:total chap including rereading time that user have read
last_updated:string: yyyy-mm-dd last update touch by users

```
</details>

<details>
 <summary>User Object</summary>

```
anime:list:Anime object list that you hve seen
manga:list:Manga object list that you hve seen
anime_watching:string: watching tracking 
anime_completed:string: completed tracking 
anime_onhold:string: onhold tracking 
anime_dropped :string: dropped tracking  
anime_plan_to_watch :string: plan_to_read tracking  
anime_days:string: days tracking 
manga_reading:string: reading tracking 
manga_completed:string: completed tracking 
manga_onhold:string: onhold tracking 
manga_dropped:string: dropped tracking 
manga_plan_to_read:string: plan_to_read tracking 
manga_days:string: days tracking 
```
</details>

<details>
 <summary>User Status</summary>
 
```
watching
reading
completed
onhold
dropped
plantowatch
plantoread

```
</details>


## Anilist

Please read guideline here [Anilist Doc](https://anilist.gitbooks.io/anilist-apiv2-docs/) to ensure you are not doing something against it.
This is not for storing or any so reason. This is getting data to be used at a moment.

#### Note: You can do SYNC or ASYNC. all method for async are same expect that you will need to await and use `connectors.AioAnimu()`

To create an instance.
```python
from pyanimu import Anilist, connectors, UserStatus_Anilist

con = connectors.ReqAnimu(user_agent = "Pyanimu") # or AioAnimu() for async


ani = Anilist(con) #doesn't have to give token unless it is for add/delete methods.

ani.search_anime("Trigun")
ani.search_anime(6)
ani.search_manga("Trigun")
ani.search_manga(30703)
ani.search_character("Vash")
ani.search_character(162)
ani.search_user("Maverun")
ani.search_user(88464)
ani.search_studio("MADHOUSE")
ani.search_studio(11)

#IF wish to add list or update it
ani = Anilist(con,token)

#To add or update them, you will need token.
ani.add(6,UserStatus_Anilist.current)
ani.add(6,UserStatus_Anilist.planning)
ani.add(6,UserStatus_Anilist.drop)
ani.add(6,UserStatus_Anilist.pause)
ani.add(6,UserStatus_Anilist.complete,extra = {"score":100})

#in order to delete it. This is a bit tedious method.

ani.toggle_setting(media_list = True)
data = ani.search_anime(6)
entry = data["media"][0]["mediaListEntry"]
ani.delete(entry["id"]) #To delete it. Note This is require token.
```

<details>
 <summary>Method</summary>
 
```
toggle_setting(char = False,airing_date = False,ranking = False,media_list = False)
    this will add extra info about char(character) or airing date or ranking or media list to anime/manga data. This is optional but media_list is require for delete.
search_anime(name)
search_manga(name)
search_character(name)
search_studio(name)
search_user(name)
user()
add(id,status,extra)
delete(id_)
airingSchedules(var)
```
</details>

<details>
 <summary>UserStatus_Anilist</summary>

```
current 
planning 
complete 
drop 
pause 
repeat 
```

</details>

<details>
   <summary>airingSchedules method</summary>
   
```
var: dict, any of those, need to be at least 1
    episode_greater: $eg,
    airingAt:$airAt,
    id_in:$id_in,
    mediaId_in:$mid_in,
    episode:$ep,
    id:$id,
    mediaId:$mid,
    airingAt_greater:$airAtG,
    airingAt_lesser:$airAtL,
    sort:$sort - [ID,ID_DESC,MEDIA_ID,MEDIA_ID_DESC,TIME,TIME_DESC,EPISODE,EPISODE_DESC]

using $name.
for example airing at x and sort from lowest to highest time
{"airAtG": x,"sort": "TIME"}
```
   
</details>