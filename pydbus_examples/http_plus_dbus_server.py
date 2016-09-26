from gevent import monkey
monkey.patch_all()

from pydbus import SessionBus
from gevent.pywsgi import WSGIServer

class TestObject(object):
	dbus = '''
<node>
	<interface name='net.lew21.pydbus.WSGIPlusDBus'>
		<method name='HelloWorld'/>
	</interface>
	<interface name='net.lew21.pydbus.WSGIPlusDBusInternal'>
		<method name='GetHelloWorldString'>
			<arg direction="out" type="s"/>
		</method>
	</interface>
</node>
	'''
	def HelloWorld(self):
		bus = SessionBus()
		bus.get("net.lew21.pydbus.WSGIPlusDBus").GetHelloWorldString()
		print("DBus call")

	def GetHelloWorldString(self):
		print("Internal DBus call")
		return "Hello World!"

def application(environ, start_response):
	print("HTTP call")

	bus = SessionBus()
	out = bus.get("net.lew21.pydbus.WSGIPlusDBus").GetHelloWorldString()

	status = '200 OK'
	response_headers = [('Content-type', 'text/plain')]
	start_response(status, response_headers)
	return [out.encode("utf-8")]

if __name__ == "__main__":
	bus = SessionBus()
	bus.publish("net.lew21.pydbus.WSGIPlusDBus", TestObject())

	WSGIServer(('', 8000), application).serve_forever()
