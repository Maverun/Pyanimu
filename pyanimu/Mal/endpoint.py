
base_api = "https://myanimelist.net/"

#Anime
anime = base_api + "api/animelist/"
search_anime = base_api + "api/anime/search.xml"
add_anime = anime + "add/{}.xml"
update_anime = anime + "update/{}.xml"
delete_anime = anime + "delete/{}.xml"

#Manga
manga = base_api + "api/mangalist/"
search_manga = base_api + "api/manga/search.xml"
add_manga = manga + "add/{}.xml"
update_manga = manga + "update/{}.xml"
delete_manga = manga + "delete/{}.xml"

#User Account
verify_user = base_api + "api/account/verify_credentials.xml"
user_list = base_api + "malappinfo.php"