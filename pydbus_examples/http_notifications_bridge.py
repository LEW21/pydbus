from gevent import monkey
monkey.patch_all()

from pydbus import SessionBus

# I'm creating the SessionBus object in application(), and not in global scope,
# because WSGI servers usually fork after importing the module; and forking will break glib.

def application(environ, start_response):
	bus = SessionBus()
	bus.get(".Notifications").Notify('pydbus', 0, 'dialog-information', "Received a HTTP request!", "Path: " + environ["PATH_INFO"], [], {}, 2000)

	status = '200 OK'
	response_headers = [('Content-type', 'text/plain')]
	start_response(status, response_headers)
	return [b"Notification sent."]

if __name__ == "__main__":
	from gevent.pywsgi import WSGIServer
	WSGIServer(('', 8000), application).serve_forever()

	"""
	You can also use:
		gunicorn -k gevent pydbus_examples.http_notifications_bridge
	or any other WSGI server with gevent support.
	"""
