"""
This idea was inspire by Spoopy ( khazhyk) https://github.com/khazhyk/osuapi
Allow to have Requests and Aiohttps based of user's choice.

Based of this, Both of them need get_api and send_api
so that it can call method without easily without checking type.
"""
from . import __github__
from .error import Http_denied

aio_boolean = False
req_boolean = False

try:#If user want to use aiohttps, they will need to install aiohttp, otherwise it will throw out an error.
    import aiohttp
    import asyncio
except ImportError:
    aio_boolean = True
else:
    class AioAnimu:
        """
        Version of Aiohttp
        """
        def __init__(self,user_agent = None):
            if aio_boolean:
                raise NotImplementedError("You need to install aiohttp in order to use AioAnimu")

            self.type =  "Aiohttp" #dont ask me please
            self.header = {"User-Agent":user_agent or __github__}
            self.has_auth = False
            self.auth = None

        #set auth
        def set_auth(self,username,password):
            self.auth = aiohttp.BasicAuth(login = username,password = password)

        async def return_data(self,resp,return_type,obj):
            if resp.status in (200,201):
                data = None
                if return_type == "text":
                    data = await resp.text()
                elif return_type == "json":
                    data = await resp.json()
                return obj(data)
            else:
                raise Http_denied(resp.status,await resp.text())

        #get data
        async def get_api(self,endpoint,obj,params = {},json = {},return_type = "json",):
            async with aiohttp.ClientSession(auth = self.auth,headers=self.header) as session:
                async with session.get(endpoint,headers = self.header,params=params,json=json) as resp:
                    return await self.return_data(resp,return_type,obj)
        #get data

        #send data
        async def send_api(self,endpoint,obj,params = {},json = {},return_type = "json"):
            async with aiohttp.ClientSession(auth = self.auth,headers=self.header) as session:
                async with session.post(endpoint,headers = self.header,params=params,json=json) as resp:
                    return await self.return_data(resp,return_type,obj)

try:#unless User want to use requests, they will need to install requests, otherwise it will throw out an error.
    import requests
except ImportError:
    req_boolean = True
else:
    class ReqAnimu:
        """
        Version of Requests
        """
        def __init__(self,user_agent = None):
            if req_boolean:
                raise NotImplementedError("You will need to install requests in order to use ReqAnimu")

            self.type =  "Requests" #dont ask me please
            self.header = {"User-Agent":user_agent or __github__}
            self.has_auth = False

        #set auth
        def set_auth(self,username,password):
            self.auth = (username,password)


        def return_data(self,r,return_type,obj):
            if r.status_code in (200,201):
                data = None
                if return_type == "text":
                    data = r.text
                elif return_type == "json":
                    data = r.json()
                return obj(data)
            else:
                raise Http_denied(r.status_code,r.text)
        #get data
        def get_api(self,endpoint,obj,params = {},return_type = "json"):
            if self.has_auth:
                r = requests.get(endpoint, auth = self.auth,headers = self.header,params=params)
            else:
                r = requests.get(endpoint,headers = self.header,params=params)
            return self.return_data(r,return_type,obj)

        #send data
        def send_api(self,endpoint,obj,params = {},json={},return_type = "json"):
            if self.has_auth:
                r = requests.post(endpoint, auth = self.auth,headers = self.header,params=params,json = json)
            else:
                r = requests.post(endpoint,headers = self.header,params=params,json = json)
            return self.return_data(r,return_type,obj)
