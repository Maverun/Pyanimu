class Http_denied(Exception):
    """
    If https is denied for some reason, it will post out status code such as 404, 400, 504 etc and print out content for giving reason
    """
    def __init__(self,status,content):
        self.status = status
        self.content = content

class Unverify_account(Exception):
    """
    if Account is unverify or does not exist, this is.
    """
    def __init(self,msg):
        self.msg = msg
