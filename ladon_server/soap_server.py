from wsgiref.simple_server import make_server

from ladon.interfaces import expose
from ladon.interfaces.base import BaseResponseHandler
from ladon.interfaces.soap11 import SOAP11ServiceDescriptor, SOAP11RequestHandler, \
    SOAP11ResponseHandler, SOAP11FaultHandler, BaseInterface
from ladon.server.wsgi import LadonWSGIApplication
from os.path import dirname, abspath, join

from ladon.compat import PORTABLE_STRING, type_to_xsd, pytype_support, BytesIO


class MySOAP11ResponseHandler(BaseResponseHandler):

    _content_type = 'text/xml'
    _stringify_res_dict = True

    def build_response(self, res_dict, sinfo, encoding):
        import xml.dom.minidom as md
        doc = md.Document()
        envelope = doc.createElement('SOAP-ENV:Envelope')
        envelope.setAttribute(
            'xmlns:SOAP-ENV', 'http://schemas.xmlsoap.org/soap/envelope/')
        envelope.setAttribute(
            'xmlns:SOAP-ENC', 'http://schemas.xmlsoap.org/soap/encoding/')
        envelope.setAttribute('xmlns:xsd', 'http://www.w3.org/2001/XMLSchema')
        envelope.setAttribute('xmlns:ns', 'urn:%s' % res_dict['servicename'])
        doc.appendChild(envelope)
        body_elem = doc.createElement('SOAP-ENV:Body')
        body_elem.setAttribute('SOAP-ENV:encodingStyle',
                               'http://schemas.xmlsoap.org/soap/encoding/')
        envelope.appendChild(body_elem)
        method_elem = doc.createElement("ns:%sResponse" % res_dict['method'])
        if 'result' in res_dict['result']:
            SOAP11ResponseHandler.value_to_soapxml(
                res_dict['result'], method_elem, doc, is_toplevel=True)
        else:
            SOAP11ResponseHandler.value_to_soapxml(
                # 自分のレスポンス型へと修正
                {'returnMessage': res_dict['result']}, method_elem, doc, is_toplevel=True)
        body_elem.appendChild(method_elem)
        return doc.toxml(encoding=encoding)


@expose
class MySOAP11Interface(BaseInterface):

    def __init__(self, sinfo, **kw):
        def_kw = {
            'service_descriptor': SOAP11ServiceDescriptor,
            'request_handler': SOAP11RequestHandler,

            # 自作のResponseHandlerへと修正
            'response_handler': MySOAP11ResponseHandler,
            'fault_handler': SOAP11FaultHandler}
        def_kw.update(kw)
        BaseInterface.__init__(self, sinfo, **def_kw)

    @staticmethod
    def _interface_name():
        # 差し替えたエンドポイントを新規作成する必要があるため、既存とは異なる値へと変更
        return 'mysoap11'

    @staticmethod
    def _accept_basetype(typ):
        return pytype_support.count(typ) > 0

    @staticmethod
    def _accept_list():
        return True

    @staticmethod
    def _accept_dict():
        return False


scriptdir = dirname(abspath(__file__))
service_modules = ['hello', ]

# Create the WSGI Application
application = LadonWSGIApplication(
    service_modules,
    [join(scriptdir, 'hello'), ],
    catalog_name='Ladon Service Examples',
    catalog_desc='The services in this catalog serve as examples to how Ladon is used',
    logging=31)


port = 9100
print("\nExample services are running on port %(port)s.\nView browsable API at http://localhost:%(port)s\n" %
      {'port': port})

server = make_server('', port, application)
server.serve_forever()
