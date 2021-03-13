%route = '/'
%if sid is not None:
    %route = '/manager/' + sid
%end
<div class="upload">
    %if sid is not None:
        <p>URL: <a href="/player/{{sid}}" target="_blank">/player/{{sid}}</a></p>
    %end
    <form action="{{route}}" method="post" enctype="multipart/form-data">
        <input name="file" type="file" onchange="form.submit();" multiple>
        </input>
    </form>
</div>
