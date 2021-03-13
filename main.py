#!/usr/bin/python3

import tempfile, pathlib, uuid, os

from gevent import monkey
monkey.patch_all()

from bottle import ServerAdapter, get, post, request, static_file, view, redirect, run

#from gevent import Greenlet
#from gevent.pywsgi import WSGIServer
#from geventwebsocket.handler import WebSocketHandler


# Server adapter providing support for WebSockets
#class CustomServer(ServerAdapter):
#    def run(self, handler):
#        server = WSGIServer((self.host, self.port), handler, handler_class=WebSocketHandler, **self.options)
#        server.serve_forever()

# ---------------------------------------------------------------------

# Holds sessions, handles playback update
class Session(object):
    def __init__(self, sid):
        self.sid       = sid
        self.tmpfile   = tempfile.NamedTemporaryFile()
        self.dirtyflag = 0
    #    self.listeners = set()

    #def addListener(self, socket):
    #    self.listeners.add(socket)

    #def removeListener(self, socket):
    #    self.listeners.remove(socket)

    def uploadAudio(self):
        # upload file
        handle = request.files.getall('file')[0]
        handle.save(destination=self.tmpfile.name, overwrite=True)
        print('UPPED')
        self.dirtyflag += 1

        # notify track being changed
        #for socket in self.listeners:
        #    try:
        #        socket.send('UPDATE')
        #        print('NOTIFIED')
        #    except Exception as e:
        #        print(e)
    
    #def handleAccept(self):
    #    while True:
    #        pass


# ---------------------------------------------------------------------

# Holds multiple sessions
class Engine(object):
    def __init__(self):
        self.sessions = dict()
    
    def startSession(self):
        sid = uuid.uuid4().hex
        self.sessions[sid] = Session(sid)
        self.sessions[sid].uploadAudio()
        return sid

    def getSession(self, sid):
        return self.sessions[sid]

    def run(self):
        run(host='0.0.0.0', port=8080, debug=True, server='gevent')#, server=CustomServer)


# ---------------------------------------------------------------------

def setup_routes(engine):

    @get('/static/<fname>')
    def static_files(fname):
        return static_file(fname, root='./static')
    
    @get('/')
    @view('landing_page')
    def upload_page():
        return dict()

    @post('/')
    def upload_post():
        sid = engine.startSession()
        
        redirect('/manager/{0}'.format(sid))

    @get('/player/<sid>')
    @view('user_view')
    def user_view(sid):
        return dict(sid=sid)

    @get('/manager/<sid>')
    @view('manager_view')
    def user_view(sid):
        return dict(sid=sid)

    @post('/manager/<sid>')
    def upload_track(sid):
        s = engine.getSession(sid)
        s.uploadAudio()
        redirect('/manager/{0}'.format(sid))
    
    @get('/stream/<sid>')
    def stream(sid):
        s = engine.getSession(sid)
        fname = s.tmpfile.name.split('/')[-1]
        root  = '/'.join(s.tmpfile.name.split('/')[:-1])
        return static_file(fname, root)

    @get('/pull/<sid>/<oldflag>')
    def ask_pull(sid, oldflag):
        s = engine.getSession(sid)
        return str(s.dirtyflag)

    #@get('/websocket/<sid>')
    #def accept_websocket(sid):
    #    socket = request.environ.get('wsgi.websocket')
    #    if socket is None:
    #        return
    #    
    #    s = engine.getSession(sid)
    #    s.addListener(socket)
    #    
    #    greenlet = Greenlet(run=s.handleAccept)
    #    greenlet.start()
    #    greenlet.get()
    #    
    #    s.removeListener(socket)


if __name__ == '__main__':
    engine = Engine()
    setup_routes(engine)
    engine.run()
    
