from bs4 import BeautifulSoup
import html


def _xml_to_kwargs(xml):
    """
    This is to save time.
    Args:
        xml: BeautifulSoap Object

    Returns: dict of kwargs that was after covert xml to dict

    """
    data = {}
    for x in xml:  # it will run each tag and pass down those tag as key then pass value.
        if x.name == "synopsis":
            data[x.name] = html.unescape(x.text.replace(",br / >", ""))
        elif x.name is not None:
            data[x.name] = x.text
    return data

def _covert_data(data,obj,tag = "entry"):
    """
    Saving time again
    Args:
        data: xml
        obj: object claass that will inherits
        tag: string, default entry, reason to use this is due to user list has different tag.

    Returns:
        object that was obj inherits
    """
    data = BeautifulSoup(data,"lxml")
    if len(data.find_all(tag)) == 1:
        return obj(**_xml_to_kwargs(data.find(tag)))
    else:
        object_list = []
        for main in data.find_all(tag):
            object_list.append(obj(**_xml_to_kwargs(main)))
        return object_list


#Those are methods that object will be using.
def verify_user(data):
    return data

def get_anime(data):
    return _covert_data(data,Anime)

def get_manga(data):
    return _covert_data(data,Manga)

def get_anime_user(data):
    anime = _covert_data(data,Anime,tag = "anime")
    return data,anime
def get_manga_user(data):
    manga = _covert_data(data,Manga,tag = "manga")
    return data,manga

def _user_update_list(data):
    return data

def get_user(data_anime,data_manga,anime,manga):
    """

    Args:
        data_anime: raw data from api of user's anime
        data_manga:raw data from api of user's manga
        anime:object of anime or list of anime obj
        manga:object of manga or list of manga obj

    Returns:
        user: User Object

    What I have done here is that
    first thing first, we create user object by giving it data_anime (raw data) for myinfo such as total watch, complete etc
    then I have create BS4 of data_manga(raw data) and update manga from user.update()
    finally, I add anime and manga object/list of object into user.

    """
    user = _covert_data(data_anime,User,"myinfo") #first we will create my user info
    temp = BeautifulSoup(data_manga,"lxml")
    user.update_manga(**_xml_to_kwargs(temp.find("myinfo")))
    user.get_anime_list(anime)
    user.get_manga_list(manga)
    return user
#Those are method that object will be using ^^^^


class Anime:

    """
    https://myanimelist.net/modules.php?go=api#animevalues
    episode. int
    status. int OR string. 1/watching, 2/completed, 3/onhold, 4/dropped, 6/plantowatch
    score. int
    storage_type. int (will be updated to accomodate strings soon) #ingoring this
    storage_value. float #ignoring this
    times_rewatched. int
    rewatch_value. int
    date_start. date. mmddyyyy
    date_finish. date. mmddyyyy
    priority. int
    enable_discussion. int. 1=enable, 0=disable
    enable_rewatching. int. 1=enable, 0=disable
    comments. string
    tags. string. tags separated by commas
    """
    def __init__(self,**kwargs):
        """

        Args:
            **kwargs:
            xml:bs4.element.Tag(usually Entry tag)
            id:int: Anime ID
            title:string: Anime title
            english:string: Anime title in english
            synonyms:string: Anime title in other word
            episodes:int: Anime's total episodes
            type:string: TV,Movie,Ova etc
            status:string: Airing,Finished Airing etc
            start_date:string: yyyy-mm-dd date of anime start airing
            end_date:string: yyyy-mm-dd date of anime end airing
            synopsis: string: description of show
            image:string: url of anime's picture
            score:int: Average score from community

            After this point, this may return None instead, if it not return from user's side

            times_rewatch:int: User's amount of time rewatch it
            rewatch_value
            date_start
            date_finish
            priority
            enable_discussion
            enable_rewatch
            comments
            tag
        """
        self.id = kwargs.get("id") or kwargs.get("series_animedb_id")
        self.title = kwargs.get("title") or kwargs.get("series_title")
        self.english = kwargs.get("english")
        self.synonyms = kwargs.get("synonyms") or kwargs.get("series_synonyms")
        self.episodes = kwargs.get("episodes")
        self.type = kwargs.get("type") or kwargs.get("series_type")
        self.status = kwargs.get("status") or kwargs.get("series_status")
        self.start_date = kwargs.get("start_date") or kwargs.get("series_start")
        self.end_date = kwargs.get("end_date") or kwargs.get("series_end")
        self.synopsis = kwargs.get("synopsis")
        self.image = kwargs.get("image") or kwargs.get("series_image")
        self.score = kwargs.get("score")


        #user relatives
        self.user_id = kwargs.get("my_id")
        self.current_episode = kwargs.get("my_watched_episodes")
        self.date_start = kwargs.get("my_start_date")
        self.date_finish = kwargs.get("my_finish_date")
        self.user_score = kwargs.get("my_score")
        self.user_status = kwargs.get("my_status")
        self.rewatch = kwargs.get("my_rewatching")
        self.rewatch_ep = kwargs.get("my_rewatching_ep")
        self.last_updated = kwargs.get("my_last_updated")


        #TODO Check this part and update it to ensure it is correct
        self.priority = kwargs.get("priority")
        self.enable_discussion = kwargs.get("enable_discussion")
        self.enable_rewatch = kwargs.get("enable_rewatching")
        self.comments = kwargs.get("comments")
        self.tag = kwargs.get("tag")

    def to_xml(self):
        """
        I have looked over bs4 to see how to create one, sadly doc are badly enough and confused to get what I want, so I am gonna be
        doing terrible way cuz i love bad job.
        Returns:
            XML FORMAT string
        """
        data = """<?xml version="1.0" encoding="UTF-8"?>\n<entry>\n"""
        entry = """
            <episode>{0.current_episode}</episode>
            <status>{0.user_status}</status>
            <score>{0.user_score}</score>
            <times_rewatched>{0.rewatch}</times_rewatched>
            <date_start>{0.date_start}</date_start>
            <date_finish>{0.date_finish}</date_finish>
            <priority>{0.priority}</priority>
            <enable_discussion>{0.enable_discussion}</enable_discussion>
            <enable_rewatching>{0.enable_rewatch}</enable_rewatching>
            <comments>{0.comments}</comments>
            <tags>{0.tag}</tags>
        </entry>
        """.format(self)
        return data + entry


class Manga:
    """
    https://myanimelist.net/modules.php?go=api#mangavalues
    chapter. int
    volume. int
    status. int OR string. 1/reading, 2/completed, 3/onhold, 4/dropped, 6/plantoread
    score. int
    times_reread. int
    reread_value. int
    date_start. date. mmddyyyy
    date_finish. date. mmddyyyy
    priority. int
    enable_discussion. int. 1=enable, 0=disable
    enable_rereading. int. 1=enable, 0=disable
    comments. string
    scan_group. string
    tags. string. tags separated by commas
    retail_volumes. int

    """
    def __init__(self,**kwargs):
        """
        id:int:
        title:string:
        english:string:
        synonyms:string:
        chapters:int:
        volumes:int:
        score:int:
        type:int:
        status:string OR int:
        start_date:string:
        end_date:string:
        synopsis:string:
        image:string:

        After this point, this may return None instead, if it not return from user's side

        times_reread:int:
        reread_value:int:
        priority:int:
        enable_discussion:int:
        enable_rereading:int:
        comments:string:
        scan_group:string:
        tags:string:
        retail_volumes:int:
        """
        self.id = kwargs.get("id") or kwargs.get("series_mangadb_id")
        self.title = kwargs.get("title") or kwargs.get("series_title")
        self.english = kwargs.get("english")
        self.synonyms = kwargs.get("synonyms") or kwargs.get("series_synonyms")
        self.chapters = kwargs.get("chapters") or kwargs.get("series_chapters")
        self.volumes = kwargs.get("volumes") or kwargs.get("series_volumes")
        self.score = kwargs.get("score")
        self.type = kwargs.get("type") or kwargs.get("series_type")
        self.status = kwargs.get("status") or kwargs.get("series_status")
        self.start_date = kwargs.get("start_date") or kwargs.get("series_start")
        self.end_date = kwargs.get("end_date") or kwargs.get("series_end")
        self.synopsis = kwargs.get("synopsis")
        self.image = kwargs.get("image") or kwargs.get("series_image")


        #user_relatives
        self.user_id = kwargs.get("my_id")
        self.read_chapters = kwargs.get("my_read_chapters")
        self.read_volumes = kwargs.get("my_read_volumes")
        self.date_start = kwargs.get("my_start_date")
        self.date_finish = kwargs.get("my_finish_date")
        self.user_score = kwargs.get("my_score")
        self.user_status = kwargs.get("my_status",6)
        self.rereading = kwargs.get("my_rereading")
        self.rereading_chap = kwargs.get("my_rereading_chap")
        self.last_updated = kwargs.get("my_updated")
        self.tags = kwargs.get("my_tags")

        #TODO Check this part and update it to ensure it is correct
        self.priority = kwargs.get("priority")
        self.enable_discussion = kwargs.get("enable_discussion")
        self.enable_reread = kwargs.get("enable_reread")
        self.comments = kwargs.get("comments")
        self.tag = kwargs.get("tag")

    def to_xml(self):
        """
        I have looked over bs4 to see how to create one, sadly doc are badly enough and confused to get what I want, so I am gonna be
        doing terrible way cuz i love bad job.
        Returns:
            XML FORMAT string
        """
        data = """<?xml version="1.0" encoding="UTF-8"?>\n<entry>\n"""
        entry = """
            <chapter>{0.read_chapters}</chapter>
            <volume>{0.read_volumes}</volume>
            <status>{0.user_status}</status>
            <score>{0.user_score}</score>
            <times_reread>{0.rereading}</times_reread>
            <reread_value></reread_value>
            <date_start>{0.date_start}</date_start>
            <date_finish>{0.date_finish}</date_finish>
            <priority>{0.priority}</priority>
            <enable_discussion>{0.enable_discussion}</enable_discussion>
            <enable_rereading>{0.enable_reread}</enable_rereading>
            <comments>{0.comments}</comments>
            <scan_group></scan_group>
            <tags>{0.tags}</tags>
            <retail_volumes></retail_volumes>
            </entry>
        """.format(self)
        return data + entry


class User:
    def __init__(self,**kwargs):
        self.id = kwargs.get("user_id")
        self.name = kwargs.get("user_name")
        self.update_anime(**kwargs)

    def get_anime_list(self,obj):
        self.anime = obj #expecting list or obj

    def get_manga_list(self,obj):
        self.manga = obj #expecting list or obj.

    def update_anime(self,**kwargs):
        #anime relatives
        self.anime_watching = kwargs.get("user_watching")
        self.anime_completed = kwargs.get("user_completed")
        self.anime_onhold = kwargs.get("user_onhold")
        self.anime_dropped  = kwargs.get("user_dropped")
        self.anime_plan_to_watch  = kwargs.get("user_plantowatch")
        self.anime_days = kwargs.get("user_days_spent_watching")


    def update_manga(self,**kwargs):
        #manga relatives
        self.manga_reading = kwargs.get("user_reading")
        self.manga_completed = kwargs.get("user_completed")
        self.manga_onhold = kwargs.get("user_onhold")
        self.manga_dropped = kwargs.get("user_dropped")
        self.manga_plan_to_read = kwargs.get("user_plantoread")
        self.manga_days = kwargs.get("user_days_spent_watching")
