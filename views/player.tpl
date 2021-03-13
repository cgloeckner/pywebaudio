%print(sid)
<div class="player">
    <audio id="player" src="/stream/{{sid}}" loop></audio>
    <div class="volume">
        <span class="button" onClick="onQuieter();">&#x1f507;</span>
        <span id="volume" onClick="onToggle();">PAUSED</span>
        <span class="button" style="float: right;" onClick="onLouder();">&#128266;</span>
    </div>
</div>

<script>
onStart('{{sid}}');
</script>
