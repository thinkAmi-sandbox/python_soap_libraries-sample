from ladon.ladonizer import ladonize


class Hello(object):
    @ladonize(str, rtype=str)
    def RequestInterface(self, userName):
        print(userName)
        return f'Hello, {userName}'
