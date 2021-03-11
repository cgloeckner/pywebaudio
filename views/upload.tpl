%include("header")

<form class="upload" action="/upload" method="post" enctype="multipart/form-data">
    <input name="file[]" type="file" onchange="form.submit();" multiple>
    </input>
</form>

%include("footer")
