#!/usr/bin/python3

import tempfile, pathlib, uuid, os

from gevent import monkey
monkey.patch_all()

from bottle import ServerAdapter, get, post, request, static_file, view, redirect, run


class AudioServer(object):
    def __init__(self):
        self.playlists = dict()

    def onUpload(self):
        tmp_dir = tempfile.TemporaryDirectory()
        root    = pathlib.Path(tmp_dir.name)

        files = files = request.files.getall('file[]')
        for i, handle in enumerate(files):
            fname = str(root / str(i))
            handle.save(fname)

        size = i
        sid = uuid.uuid4().hex

        self.playlists[sid] = {
            'dir'   : tmp_dir,
            'root'  : root,
            'active': '0'
        }
        
        redirect('/player/{0}'.format(sid))

    def run(self):
        @get('/static/<fname>')
        def static_files(fname):
            return static_file(fname, root='./static')
        
        @get('/')
        @view('upload')
        def index():
            return dict()
        
        @post('/upload')
        def upload():
            return self.onUpload()

        @get('/stream/<sid>/<index>')
        def stream(sid, index):
            plist = self.playlists[sid]
            return static_file(index, plist['root'])

        @get('/player/<sid>') 
        @view('player')
        def player(sid):
            plist = self.playlists[sid]
            indices = os.listdir(plist['root'])
            indices.sort()
            return dict(sid=sid, indices=indices)

        @post('/push/<sid>/<index>')
        def push(sid, index):
            plist = self.playlists[sid]
            plist['active'] = index

        @get('/pull/<sid>')
        def pull(sid):
            plist = self.playlists[sid]
            return plist['active']

        run(host='0.0.0.0', port=8080, server='gevent', debug=True)


if __name__ == '__main__':
    s = AudioServer()
    s.run()

