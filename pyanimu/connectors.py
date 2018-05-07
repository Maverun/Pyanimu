"""
This idea was inspire by Spoopy ( khazhyk) https://github.com/khazhyk/osuapi
Allow to have Requests and Aiohttps based of user's choice.

Based of this, Both of them need get_api and send_api
so that it can call method without easily without checking type.
"""
from . import __github__
from .error import Http_denied


try:#If user want to use aiohttps, they will need to install aiohttp, otherwise it will throw out an error.
    import aiohttp
    import asyncio
except ImportError:
    raise NotImplementedError("You need to install aiohttp in order to use AioAnimu")
else:
    class AioAnimu:
        """
        Version of Aiohttp
        """
        def __init__(self,user_agent = None):
            self.type =  "Aiohttp" #dont ask me please
            self.header = {"User-Agent":user_agent or __github__}

        #set auth
        def set_auth(self,username,password):
            self.auth = aiohttp.BasicAuth(login = username,password = password)

        #get data
        async def get_api(self,endpoint,obj,params = {},return_type = "json",):
            with aiohttp.ClientSession(auth = self.auth,headers=self.header) as session:
                async with session.get(endpoint,headers = self.header,params=params) as resp:
                    # resp = await self.session.get(endpoint,auth = self.auth,params = params)
                    if resp.status == 200:
                        data = None
                        if return_type == "text":
                            data = await resp.text()
                        elif return_type == "json":
                            data = await resp.json()
                        return obj(data)

                    else:
                        raise Http_denied(resp.status,await resp.text())
        #get data

        #send data

try:#unless User want to use requests, they will need to install requests, otherwise it will throw out an error.
    import requests
except ImportError:
    raise NotImplementedError("You will need to install requests in order to use ReqAnimu")
else:
    class ReqAnimu:
        """
        Version of Requests
        """
        def __init__(self,user_agent = None):
            self.type =  "Requests" #dont ask me please
            self.header = {"User-Agent":user_agent or __github__}


        #set auth
        def set_auth(self,username,password):
            self.auth = (username,password)

        #get data
        def get_api(self,endpoint,obj,params = {},return_type = "json"):
            r = requests.get(endpoint, auth = self.auth,headers = self.header,params=params)
            if r.status_code in (200,201):
                data = None
                if return_type == "text":
                    data = r.text
                elif return_type == "json":
                    data = r.json()
                return obj(data)
            else:
                raise Http_denied(r.status_code,r.text)
        #send data
