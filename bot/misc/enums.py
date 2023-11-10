from enum import Enum


class Request(Enum):
    get = "get"
    post = "post"


r = Request("get")

print(r is Request.get)