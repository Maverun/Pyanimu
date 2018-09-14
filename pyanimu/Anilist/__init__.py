from .. import error

def return_data(data):
    return data["data"]["Page"]

def return_mutations(data):
    return data

class UserStatus_Anilist:
    current = "CURRENT"
    planning = "PLANNING"
    complete = "COMPLETED"
    drop = "DROPPED"
    pause = "PAUSED"
    repeat = "REPEATING"


class Anilist:
    def __init__(self,connection,api_token = None):
        self.connection = connection
        self.api_token = api_token
        self.graphql_endpoint = "https://graphql.anilist.co/"
        if api_token:
            self.connection.header.update({'Content-Type': 'application/json','Accept': 'application/json',"Authorization": "Bearer {}".format(api_token)},)
        else:
            self.connection.header.update({'Content-Type': 'application/json','Accept': 'application/json'})
        self._setting = []

    def toggle_setting(self,char = False,airing_date = False,ranking = False,media_list = False):
        """
        Terrible way of doing it I know.

        Asking if user want to have extra of char, airing date and ranking etc.
        Args:
            char:boolean
            airing_date:boolean
            ranking: boolean

        Returns: None

        """
        temp = []
        if char:
            temp.append(self._add_char)
        if ranking:
            temp.append(self._add_ranking)
        if media_list:
            temp.append(self._add_medialist)
        self._setting  = temp

    def _add_char(self):
        return """\
        characters{
            nodes{
              name {
                first
                last
                native
              }
              description
              image {
                large
                medium
              }}}"""

    def _add_ranking(self):
        return"""\
        rankings {
            id
            rank
            type
            format
            year
            season
            allTime
            context
        }"""

    def _add_medialist(self):
        return"""\
      mediaListEntry {
        id
        userId
        status
        score
        notes
        progress
        progressVolumes
        startedAt{
          year
          month
          day
        }
        completedAt{
          year
          month
          day
        }
      }"""

    def _run_setting(self):
        extra = ""
        for x in self._setting:
            extra += x()
        return extra

    def search_anime(self,name):
        data = """\
        query ($id: Int,$id_in:[Int],$search: String, $page: Int, $perPage: Int) {
          Page(page: $page, perPage: $perPage) {
            pageInfo {
              total
              currentPage
              lastPage
              hasNextPage
              perPage
            }
            media(id: $id,id_in:$id_in search: $search, type: ANIME) {
              id
              idMal
              siteUrl
              title {
                romaji
                english
                native
              }
              synonyms
              startDate {
                year
                month
                day
              }
              endDate {
                year
                month
                day
              }
              coverImage {
                large
              }
              bannerImage
              format
              status
              episodes
              season
              description
              averageScore
              meanScore
              genres
              type

              studios{
                edges{
                  id
                  node{
                    name
                  }
                }
              }
              nextAiringEpisode {
                airingAt
                timeUntilAiring
                episode
              }
              stats {
                scoreDistribution {
                  score
                  amount
                }
                statusDistribution {
                  status
                  amount
                }
              }
            {extra}
            }
          }
        }
        """.replace("{extra}",self._run_setting()) #terrible way heh
        if isinstance(name,int):
            v = {"id":name}
        elif isinstance(name,list):
            v = {"id_in":name}
        else:
            v = {"search":name}
        return self.connection.send_api(self.graphql_endpoint, json = {"query":data,"variables":v}, obj = return_data)

    def search_manga(self,name):
        data = """\
        query ($id: Int,$id_in:[Int],$search:String, $page: Int, $perPage: Int) {
          Page(page: $page, perPage: $perPage) {
            pageInfo {
              total
              currentPage
              lastPage
              hasNextPage
              perPage
            }
            media(id: $id,id_in:$id_in search: $search, type: MANGA) {
              id
              idMal
              siteUrl
              title {
                romaji
                english
                native
              }
              synonyms
              startDate {
                year
                month
                day
              }
              endDate {
                year
                month
                day
              }
              coverImage {
                large
              }
              bannerImage
              format
              status
              chapters
              volumes
              description
              averageScore
              meanScore
              genres
              type
              stats {
                scoreDistribution {
                  score
                  amount
                }
                statusDistribution {
                  status
                  amount
                }
              }
            {extra}
            }
          }
        }""".replace("{extra}",self._run_setting()) #terrible way heh
        if isinstance(name,int):
            v = {"id":name}
        elif isinstance(name,list):
            v = {"id_in":name}
        else:
            v = {"search":name}
        return self.connection.send_api(self.graphql_endpoint, json = {"query":data,"variables":v}, obj = return_data)

    def search_character(self,name):
        """
        Searching characters
        It can be searched by ID or name, if provide ID, it will give accurate one info, if string, it may return multi result.

        Args:
            name: int or string

        Returns: dict

        """
        data = """\
        query ($id: Int, $page: Int, $perPage: Int, $search: String) {
          Page(page: $page, perPage: $perPage) {
            pageInfo {
              total
              currentPage
              lastPage
              hasNextPage
              perPage
            }
            characters(search: $search, id: $id) {
              description
              siteUrl
              image{
                large
                }
              name {
                first
                last
                native
              }
              id
              media {
                edges {
                  id
                }
                nodes {
                  id
                  title {
                    romaji
                    english
                    native
                  }
                }
              }
            }
          }
        }"""
        if isinstance(name,int):
            v = {"id":name}
        else:
            v = {"search":name}
        return self.connection.send_api(self.graphql_endpoint, json = {"query":data,"variables":v}, obj = return_data)

    def search_studio(self,name):
        """
        Searching studios
        It can be searched by ID or name, if provide ID, it will give accurate one info, if string, it may return multi result.

        Args:
            name: int or string

        Returns: dict

        """
        data = """\
        query ($id: Int, $page: Int, $perPage: Int, $search: String) {
          Page(page: $page, perPage: $perPage) {
            pageInfo {
              total
              currentPage
              lastPage
              hasNextPage
              perPage
            }
            studios(search: $search, id: $id) {
              id
              name
              siteUrl
              favourites
              media {
                nodes {
                  id
                  siteUrl
                  title {
                    romaji
                    english
                    native
                  }
                }
              }
            }
          }
        }"""
        if isinstance(name,int):
            v = {"id":name}
        else:
            v = {"search":name}
        return self.connection.send_api(self.graphql_endpoint, json = {"query":data,"variables":v}, obj = return_data)

    def search_user(self,name):
        """
        Searching user
        It can be searched by ID or name, if provide ID, it will give accurate one info, if string, it may return multi result.

        p.s wow this string took 145 lines and person who use this method are likely to be a stalker? (joking)

        Args:
            name: int or string

        Returns: dict

        """
        data = """\
        query ($id: Int, $page: Int, $perPage: Int, $search: String) {
          Page(page: $page, perPage: $perPage) {
            pageInfo {
              total
              currentPage
              lastPage
              hasNextPage
              perPage
            }
            users(search: $search, id: $id) {
              id
              name
              about
              avatar {
                large
              }
              bannerImage
              options {
                titleLanguage
                displayAdultContent
                airingNotifications
                profileColor
              }
              mediaListOptions {
                scoreFormat
                rowOrder
                animeList {
                  splitCompletedSectionByFormat
                  theme
                  advancedScoringEnabled
                }
                mangaList {
                  splitCompletedSectionByFormat
                  theme
                  advancedScoringEnabled
                }
              }
              favourites {
                anime {
                  edges {
                    id
                  }
                }
                manga {
                  edges {
                    id
                  }
                }
                characters {
                  edges {
                    id
                  }
                }
                staff {
                  edges {
                    id
                  }
                }
                studios {
                  edges {
                    id
                  }
                }
              }
              siteUrl
              donatorTier
              moderatorStatus
              updatedAt
              stats {
                watchedTime
                chaptersRead
                activityHistory {
                  date
                  amount
                  level
                }
                animeStatusDistribution {
                  status
                  amount
                }
                mangaStatusDistribution {
                  status
                  amount
                }
                animeScoreDistribution {
                  score
                  amount
                }
                mangaScoreDistribution {
                  score
                  amount
                }
                animeListScores {
                  meanScore
                  standardDeviation
                }
                mangaListScores {
                  meanScore
                  standardDeviation
                }
                favouredGenresOverview {
                  genre
                  amount
                  meanScore
                  timeWatched
                }
                favouredGenres {
                  genre
                  amount
                  meanScore
                  timeWatched
                }
                favouredTags {
                  amount
                  meanScore
                  timeWatched
                }
                favouredActors {
                  amount
                  meanScore
                  timeWatched
                }
                favouredStaff {
                  amount
                  meanScore
                  timeWatched
                }
                favouredStudios {
                  amount
                  meanScore
                  timeWatched
                }
                favouredYears {
                  year
                  amount
                  meanScore
                }
                favouredFormats {
                  format
                  amount
                }
              }
            }
          }
        }"""
        if isinstance(name,int):
            v = {"id":name}
        else:
            v = {"search":name}
        return self.connection.send_api(self.graphql_endpoint, json = {"query":data,"variables":v}, obj = return_data)

    def user(self):
        """
        Give info about authenticated user that provide this token.
        p.s wow this string took 145 lines and person who use this method are likely to be a stalker? (joking)

        Returns: dict
        """
        if self.api_token is None:
           return error.Missing_token("This method need a api token.")
        query = """
        query{
            Viewer{
              id
              name
              about
              avatar {
                large
              }
              bannerImage
              options {
                titleLanguage
                displayAdultContent
                airingNotifications
                profileColor
              }
              mediaListOptions {
                scoreFormat
                rowOrder
                animeList {
                  splitCompletedSectionByFormat
                  theme
                  advancedScoringEnabled
                }
                mangaList {
                  splitCompletedSectionByFormat
                  theme
                  advancedScoringEnabled
                }
              }
              favourites {
                anime {
                  edges {
                    id
                  }
                }
                manga {
                  edges {
                    id
                  }
                }
                characters {
                  edges {
                    id
                  }
                }
                staff {
                  edges {
                    id
                  }
                }
                studios {
                  edges {
                    id
                  }
                }
              }
              siteUrl
              donatorTier
              moderatorStatus
              updatedAt
              stats {
                watchedTime
                chaptersRead
                activityHistory {
                  date
                  amount
                  level
                }
                animeStatusDistribution {
                  status
                  amount
                }
                mangaStatusDistribution {
                  status
                  amount
                }
                animeScoreDistribution {
                  score
                  amount
                }
                mangaScoreDistribution {
                  score
                  amount
                }
                animeListScores {
                  meanScore
                  standardDeviation
                }
                mangaListScores {
                  meanScore
                  standardDeviation
                }
                favouredGenresOverview {
                  genre
                  amount
                  meanScore
                  timeWatched
                }
                favouredGenres {
                  genre
                  amount
                  meanScore
                  timeWatched
                }
                favouredTags {
                  amount
                  meanScore
                  timeWatched
                }
                favouredActors {
                  amount
                  meanScore
                  timeWatched
                }
                favouredStaff {
                  amount
                  meanScore
                  timeWatched
                }
                favouredStudios {
                  amount
                  meanScore
                  timeWatched
                }
                favouredYears {
                  year
                  amount
                  meanScore
                }
                favouredFormats {
                  format
                  amount
                }
              }
            }
          }
        """
        return self.connection.send_api(self.graphql_endpoint, json={"query": query}, obj=return_mutations)

    def add(self,the_id,status,extra = {}):
        """
        Allow to add anime to the list

        Note: This need auth token.

        Args:
            the_id:int:can be regular ID or media ID
            status:UserStatus_Anilist obj: select which property it is, current, planning, complete, drop,pause or repeat.
            extra:dict: something else to add to it, for now, score which is Float atm.
        Returns: json of response.
        """
        if self.api_token is None:
            return error.Missing_token("This method need a api token.")
        query = """
        mutation ($mediaId: Int, $status: MediaListStatus,$score:Float) {
            SaveMediaListEntry (mediaId: $mediaId, status: $status,score:$score) {
                id
                status
                score
            }
        }"""
        return self.connection.send_api(self.graphql_endpoint,json ={"query":query,"variables":{"mediaId":the_id,"status":status,**extra}},obj = return_mutations)

    def delete(self,id_):
        """
        This will delete anime from your list, to delete it, you will need to run toggle_setting and set media_list to True
        Run Request to search anime/manga, then json["data"]["Page"]["media"][0]["mediaListEntry"]["id"] in order to delete it.

        This require token
        Args:
            id_:int:media ID under MediaListEntry.

        Returns: json of confirm deleted.
        """
        if self.api_token is None:
            return error.Missing_token("This method need a api token.")
        query = """
        mutation ($id:Int!) {
            DeleteMediaListEntry (id:$id){
                deleted
            }
        }"""
        return self.connection.send_api(self.graphql_endpoint,json ={"query":query,"variables":{"id":id_}},obj = return_mutations)

    def airingSchedules(self,var):
        """
        Bring up airing schedules.
        Args:
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
            {
            "airAtG": x,
            "sort": "TIME"
            }
        Returns: dict

        """
        query = """
        query ($page: Int, $perPage: Int,$eg: Int,$airAt:Int,$id_in:[Int],$mid_in:[Int],
        $ep:Int,$id:Int,$mid:Int,$airAtG:Int,$airAtL:Int,$sort:[AiringSort]) {
          Page(page: $page, perPage: $perPage) {
            pageInfo {
              total
              currentPage
              lastPage
              hasNextPage
              perPage
            }
            
            airingSchedules(episode_greater: $eg,airingAt:$airAt,id_in:$id_in,
            mediaId_in:$mid_in,episode:$ep,id:$id,mediaId:$mid,airingAt_greater:$airAtG,
            airingAt_lesser:$airAtL,sort:$sort) {
              id
              airingAt
              timeUntilAiring
              episode
              mediaId
              media {
                id
                idMal
                siteUrl
                title {
                    romaji
                    english
                    native
                }
              }
            }
          }
        }
        """
        return self.connection.send_api(self.graphql_endpoint,json ={"query":query,"variables":var},obj = return_data)
