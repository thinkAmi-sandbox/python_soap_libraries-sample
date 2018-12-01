"""
実装してみたものの、エラーが出たため、この実装で正しいのかは不明

Null Serverの実装で、asyncキーワードを使っているため、例外が出るので、
Python3.7では使えなかった

  File "/path/to/lib/python3.7/site-packages/spyne/server/null.py", line 69
    self.service = _FunctionProxy(self, self.app, async=False)
                                                      ^
SyntaxError: invalid syntax


別のライブラリでも同じようなエラーがissueにあり、対応されていた
https://github.com/pycontribs/jira/issues/603
"""

from spyne.application import Application
from spyne.decorator import rpc
from spyne.model.complex import Iterable
from spyne.model.primitive.string import Unicode
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from spyne.service import ServiceBase


class HelloWorldService(ServiceBase):
    @rpc(Unicode, _returns=Iterable(Unicode))
    def hello(ctx, name):
        return f'Hello, {name}'


application = Application([HelloWorldService],
                          tns='spyne.examples.hello',
                          in_protocol=Soap11(),
                          out_protocol=Soap11()
                          )


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    wsgi_app = WsgiApplication(application)
    server = make_server('0.0.0.0', 9100, wsgi_app)
    server.serve_forever()
