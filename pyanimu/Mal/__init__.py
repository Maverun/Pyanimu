from . import endpoint,object
from .. import error

class UserStatus:
    watching = 1
    reading = 1
    completed = 2
    onhold = 3
    dropped = 4
    plantowatch = 6
    plantoread = 6

class Mal:
    """
    Myanimelist

    It will give empty object unless call for anime/manga

    Given that MAL have lacked of API/Documents.
    There is a very few endpoints that can be made

    Verify Accounts
    Search
        -Anime
        -Manga
    User
        -List
            -Anime
            -Manga
        -Anime
            -Add
            -Update
            -Delete
        -Manga
            -Add
            -Update
            -Delete


    Method that can be used:
    verify - checking if account verify. It will auto check when create instances.
    search_anime - finding an anime relative to that title, it may return just an Anime object or List of an Anime Object
    search_manga - finding manga relative to that title, it may return just Manga object or List of Manga Object
    aio_search_user - getting user list with anime/magna list (only user relative attitude) [coroutine])
    req_search_user - getting user list with anime/manga list (only user relative attitude) with  Request.
    add - add anime/manga to user list. It will add to account that was given to this instances
    update - update anime/manga to user list. It will update of user'list, You cannot use add if it already exist inside. that was given to this instances
    delete- delete anime/manga from user list. It will delete from account that was given to this instances
    """

    def __init__(self,username,password,connection):
        """
        MAL require Username/Password for every endpoint expect User's List. However, even so, it will require username/password
        Args:
            username: The username account.
            password: Password for username
            connection: connection of either connectors.AioAnimu or connectors.ReqAnimu
        """
        self.username = username
        self.password = password
        self.connect = connection

        self.connect.set_auth(username,password)

    def verify(self):
        try:
            return self.connect.get_api(endpoint.verify_user,return_type="text", obj = object.verify_user)
        except error.Http_denied:
            return False
            #raise error.Unverify_account("This account either don't exist or incorrect username/password")

    def search_anime(self,title):
        #searching anime list by calling api with endpoint of search anime, and params are title. We are also telling it is text which is xml, and create it by giving instances of object.
         return self.connect.get_api(endpoint.search_anime,params = {"q":title},return_type = "text",obj = object.get_anime)

    def search_manga(self,title):#Same as Search anime method but within manga this time
        return self.connect.get_api(endpoint.search_manga,params = {"q":title},return_type = "text",obj = object.get_manga)

    """
    Until I found a better way for having one function search user for both async/req.
    
    
    This will search User and return their anime/manga list.
    Please do note that this only return anime/manga that are relative to user, not community.
    """
    async def aio_search_user(self,name): #first getting all data anime relative to user, then manga, finally put them together into User object
        data_anime, anime = await self.connect.get_api(endpoint.user_list,params = {"u": name, "status": "all", "type": "anime"},return_type = "text", obj = object.get_anime_user)
        data_magna, manga = await self.connect.get_api(endpoint.user_list,params = {"u": name, "status": "all", "type": "manga"},return_type = "text", obj = object.get_manga_user)
        user = object.get_user(data_anime,data_magna,anime, manga)
        return user

    def req_search_user(self,name):#same as aio_search user but this time it is request.
        data_anime,anime  =  self.connect.get_api(endpoint.user_list,params = {"u":name,"status":"all","type":"anime"},return_type = "text",obj = object.get_anime_user)
        data_magna,manga =  self.connect.get_api(endpoint.user_list,params = {"u":name,"status":"all","type":"manga"},return_type = "text",obj = object.get_manga_user)
        user = object.get_user(data_anime,data_magna,anime,manga)
        return user
    """
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    Until I found a better way for having one function search user for both async/req.
    """


    """
    Those except delete method require xml to send, by default user status will be set as plan to watch/read unless set it.
    You can easily set it with UserStatus.
    UserStatus.watching
    
    anime.user_status = UserStatus.onhold
    
    etc
    
    """
    def add(self,obj):
        if isinstance(obj,object.Anime):
            return self.connect.get_api(endpoint.add_anime.format(obj.id),params = {"data":obj.to_xml()},return_type="text",obj = object._user_update_list)
        elif isinstance(obj,object.Manga):
            return self.connect.get_api(endpoint.add_manga.format(obj.id),params = {"data":obj.to_xml()},return_type="text",obj = object._user_update_list)
        raise ValueError("{} is not an Anime or Manga object.".format(type(obj)))

    def update(self,obj):
        if isinstance(obj,object.Anime):
            return self.connect.get_api(endpoint.update_anime.format(obj.id),params = {"data":obj.to_xml()},return_type ="text",obj = object._user_update_list)
        elif isinstance(obj, object.Manga):
            return self.connect.get_api(endpoint.update_manga.format(obj.id),params = {"data":obj.to_xml()},return_type ="text",obj = object._user_update_list)
        raise ValueError("{} is not an Anime or Manga object.".format(type(obj)))

    def delete(self,obj):
        if isinstance(obj,object.Anime):
            return self.connect.get_api(endpoint.delete_anime.format(obj.id),return_type ="text",obj = object._user_update_list)
        if isinstance(obj, object.Manga):
            return self.connect.get_api(endpoint.delete_manga.format(obj.id),return_type ="text",obj = object._user_update_list)
        raise ValueError("{} is not an Anime or Manga object.".format(type(obj)))
