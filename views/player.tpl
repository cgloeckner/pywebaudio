%include("header")

<div class="player">
    <audio id="player" loop></audio>
    <h1 id="track">---</h1>
    <div class="volume">&#128266;
        <input type="button" value="-" onClick="onQuieter();">
        <input type="button" value="+" onClick="onLouder();">
        <span id="volume">0%</span>
    </div>

    <p>CLICK TO PLAY FOR ALL:</p>
    <ul>
    %for index in indices:
        <li><a href="javascript:onPlay({{index}});">Track {{int(index)+1}}</a></li>
    %end
    </ul>
</div>

<script>
var active = null;

function onPlay(index) {
    navigator.sendBeacon('/push/{{sid}}/' + index, null);
}

function onUpdate() {
    var player = $('#player')[0];
    // reload url
    player.src = '/stream/{{sid}}/' + active;
    player.play();
    showTrack();
}

function getVolumeDelta(v) {
    if (v > 0.25) {
        return 0.05;
    } else {
        return v * 0.25;
    }
}

function onQuieter() {
    var player = $('#player')[0];
    var v = player.volume;
    delta = getVolumeDelta(v);
    v -= delta;
    if (v < 0.01) {
        v = 0.01;
    }
    player.volume = v;
    if (player.paused) {
        player.play();
    }
    showVolume();
}
   
function onLouder() {
    var player = $('#player')[0];
    var v = player.volume;
    delta = getVolumeDelta(v);
    v += delta;
    if (v > 1.0) {
        v = 1.0;
    }
    player.volume = v; 
    if (player.paused) {
        player.play();
    }    
    showVolume();
}

function pull() {
    $.get('/pull/{{sid}}', success=function(data) {
        if (data != active) {
            active = data;
            onUpdate();
        }
        setTimeout(pull, 5000);
    });
}

function showTrack() {
    $('#track')[0].innerHTML = 'Track ' + (parseInt(active)+1);
}

function showVolume() {  
    var player = $('#player')[0];
    var v = parseInt(player.volume * 100);
    if (player.paused) {
        v = 0;
    }
    $('#volume')[0].innerHTML = v + '%';
}

pull();

$('#player')[0].volume = 0.1;
</script>

%include("footer")
