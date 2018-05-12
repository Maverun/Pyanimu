This is Pyanimu, inspired by [Pymoe](https://github.com/ccubed/PyMoe) and [osuapi](https://github.com/khazhyk/osuapi) for their way of structure lib, (osuapi for having sync/async).

This is created to help people like me not dealing with XML anymore. It is not perfect ideal lib. For a better used, I recommend checking out [Pymoe](https://github.com/ccubed/PyMoe)(sync only)

This is my first public library to be share with other, it was created for fun learning educations purpose.
Any feedback are always appreciates, but I may not able to update it often.

I may add more stuff not just myanimelist. This is why I went with this structure way.

I would love to apology in advanced, if there is any thing that was missing from here or inconnect way of doing it.
Please do give me head up about missing document as MAL API doc...is awful.

I am ready to be roast.


## Requirement Libs:
```
BeautifulSoup, LXML
and either Aiohttp or Requests depending on what you need for.
```

___

# Mal
To create an instance.
```python
from pyanimu import Mal, connectors, Userstatus

con = connectors.ReqAnimu() # or AioAnimu() for async

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

##using Async function 
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
