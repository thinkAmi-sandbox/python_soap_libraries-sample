import pathlib

from zeep import Client

WSDL = pathlib.Path(__file__).resolve().parents[1].joinpath('hello.wsdl')

client = Client(str(WSDL))

response = client.service.requestMessage(userName='taro')

print(type(response))
print(response)
