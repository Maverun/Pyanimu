This is Pyanimu, inspired by [Pymoe](https://github.com/ccubed/PyMoe) and [osuapi](https://github.com/khazhyk/osuapi) for their way of structure lib, (osuapi for having requests/aiohttp).

This is my first library, and created for fun and learning educations purpose.
Any feedback are always appreciates, however I may not able to update it often.


## Mal
To create an instance.
```python
from pyanimu import Mal
from pyanimu import connectors

con = connectors.ReqAnimu() # or AioAnimu() for aiohttp

mal = Mal(username, password,con)  # Since every endpoint requires authentication, username/password isn't optional

anime_obj = mal.search_anime("Trigun") #it may return an object or list of an object depending on search queue.


```
