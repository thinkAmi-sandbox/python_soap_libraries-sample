from pysimplesoap.server import SoapDispatcher, WSGISOAPHandler

dispatcher = SoapDispatcher(
    name="PySimpleSoapSample",
    location="http://localhost:9100/",
    action='http://localhost:9100/',  # SOAPAction
    namespace="http://example.com/pysimplesoapsamle/", prefix="ns0",
    documentation='Example soap service using PySimpleSoap',
    trace=True, debug=True,
    ns=True)


# これをやっても、以下のエラーが出る
# AttributeError: 'str' object has no attribute 'decode'
class WSGISOAPPython3Handler(WSGISOAPHandler):
    def do_post(self, environ, start_response):
        length = int(environ['CONTENT_LENGTH'])
        request = environ['wsgi.input'].read(length)
        response = self.dispatcher.dispatch(str(request))
        start_response('200 OK', [('Content-Type', 'text/xml'), ('Content-Length', str(len(response)))])
        return [response]


def say_hello(RequestInterface):
    return RequestInterface.userName


dispatcher.register_function(
    'Hello',
    say_hello,
    args={'messageIn': str},
    returns={'messageOut': str},
)

# print(dispatcher.wsdl())

from wsgiref.simple_server import make_server

application = WSGISOAPPython3Handler(dispatcher)

# 元々のだと、以下のエラーが出る
# Traceback (most recent call last):
# File "python_soap_libraries-sample/env370/lib/python3.7/site-packages/pysimplesoap/server.py", line 163, in dispatch
# ns = NS_RX.findall(xml)
# TypeError: cannot use a string pattern on a bytes-like object
# application = WSGISOAPHandler(dispatcher)

wsgid = make_server('', 9100, application)
wsgid.serve_forever()
