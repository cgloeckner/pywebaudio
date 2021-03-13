var session = null;

function showVolume() {  
    var player = $('#player')[0];
    var v = parseInt(player.volume * 100) + '%'
    if (player.paused) {
        v = '<span class="muted">' + v + '</span>';
    }
    $('#volume')[0].innerHTML = v;
}

function getVolumeDelta(v) {
    if (v > 0.5) {
        return 0.1
    } else if (v > 0.25) {
        return 0.05;
    } else if (v > 0.1) {
        return 0.03
    } else {
        return 0.01;
    }
}
 
function setVolume(v) {
    var player = $('#player')[0];
    player.volume = v;
    localStorage.setItem('volume', v);
    if (player.paused) {
        player.play();
    }
    showVolume();
}
   
function onQuieter() {
    var player = $('#player')[0];
    var v = player.volume;
    delta = getVolumeDelta(v);
    v -= delta;
    if (v < 0.01) {
        v = 0.01;
    }
    setVolume(v);
}

function onLouder() {
    var player = $('#player')[0];
    var v = player.volume;
    delta = getVolumeDelta(v);
    v += delta;
    if (v > 1.0) {
        v = 1.0;
    }
    setVolume(v);
}

function onToggle() { 
    var player = $('#player')[0];
    if (player.paused) {
        player.play();
    } else {
        player.pause();
    }
    showVolume();
}

function onUpdate() {
    var player = $('#player')[0];
    player.src = '/stream/' + session;
    player.play();
    console.log('PUSHED');
}

/// ajax-based pull if track has changed
/// @NOTE: this may be replaced by a websocket

var dirtyflag = -1;

function pull() {
    $.get('/pull/' + session + '/' + dirtyflag, success=function(data) {
        var newflag = parseInt(data);
        if (newflag != dirtyflag) {
            dirtyflag = newflag;
            onUpdate();
        }

        setTimeout(pull, 5000);
    });
}

function onStart(sid) {
    /*
    var protocol = 'ws';
    if (location.protocol == 'https') {
        protocol += 's'
    }
    var url = protocol + '://' + location.host + '/websocket/' + sid;
    console.log(url);
    socket = new WebSocket(url);
    
    socket.onmessage = function(event) {
        onUpdate(sid);
    };
    */

    session = sid;

    // setup default volume
    default_volume = localStorage.getItem('volume');;
    if (default_volume == null) {
        default_volume = 0.15;
    }
    var player = $('#player')[0];
    player.volume = default_volume;
    
    pull();
}    
