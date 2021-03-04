<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8"> 
    <link rel="shortcut icon" href="/static/favicon.ico" type="image/x-icon"> 
    <script src="/static/jquery-3.3.1.min.js"></script> 
</head>

<body>

<audio id="player" controls loop>
</audio>

<ul>
%for index in indices:
    <li><a href="javascript:onPlay({{index}});">Track {{int(index)+1}}</a></li>
%end
</ul>

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

pull();

$('#player')[0].volume = 0.01;
</script>

</body>
</html>
