import pathlib

from zeep import Client

WSDL = pathlib.Path(__file__).resolve().parents[1].joinpath('hello.wsdl')

client = Client(str(WSDL))
service = client.create_service(
    '{http://example.com/HelloWorld}HelloBindingSoap11',
    'http://localhost:9100/hello/mysoap11'
)
response = service.requestMessage(userName='taro')

print(type(response))
print(response)
