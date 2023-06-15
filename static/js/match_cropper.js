// Cropper
let uploadButton = document.getElementById("id_upload_profile_picture");
let chosenImage = document.getElementById("chosen-image");
let result = document.querySelector('.result');
let save = document.querySelector('.save');
let cropped = document.querySelector('.cropped');
let cropper = '';

uploadButton.onchange = () => {
  let reader = new FileReader();
  reader.onload = () => {
    $('#modal_crop_picture').modal('show');
    let img = document.createElement('img');
    img.id = 'image';
    img.src = reader.result;
    // clean result before
    result.innerHTML = '';
    // append new image
    result.appendChild(img);
    // show save btn and options
    save.classList.remove('hide');
    // init cropper
    cropper = new Cropper(img);
  }
  reader.readAsDataURL(uploadButton.files[0]);
  // save on click
  save.addEventListener('click', async (e) => {
    e.preventDefault();
    // get result to data uri
    let imgSrc = cropper.getCroppedCanvas({
      width: 400,
      height: 400
    }).toDataURL();
    // show image cropped
    let img = document.createElement('img');
    img.id = 'image';
    img.src = imgSrc;

    fetch(imgSrc)
      .then(res => res.blob())
      .then(blob => {
        let container = new DataTransfer();
        let file = new File([blob], "img___.png", { type: "image/png", lastModified: new Date().getTime() });

        container.items.add(file);

        uploadButton.files = container.files;

      });

    chosenImage.setAttribute("src", imgSrc);
    $('#modal_crop_picture').modal('hide');
  });
  // important to permit reload picture
  //uploadButton.value = '';
}
// End Cropper
