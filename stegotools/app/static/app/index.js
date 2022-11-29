upload = document.querySelector('.upload-icon');
upload_div = document.querySelector('.upload-div');

upload_div.onmouseover = mouseOverUpload;
upload_div.onmouseout = mouseOutUpload;

function mouseOverUpload()
{
    upload.src = "upload.png";
}

function mouseOutUpload()
{
    upload.src = "export.png";

}