<<<<<<< HEAD
const siteUrl = '//django-social-website.up.railway.app/';
const styleUrl = siteUrl + 'static/css/bookmarklet.css';
=======
// const siteUrl = '/127.0.0.1:8000/';
// const styleUrl = siteUrl + '../static/css/bookmarklet.css';
const styleUrl = '../static/css/bookmarklet.css';
>>>>>>> develop
const minWidth = 250;
const minHeight = 250;

// load CSS
var head = document.getElementsByTagName('head')[0];  // Get HTML head element
var link = document.createElement('link'); // Create new link Element
link.rel = 'stylesheet'; // set the attributes for link element
link.type = 'text/css';
<<<<<<< HEAD
link.href = styleUrl + '?r=' + Math.floor(Math.random()*9999999999999999);
=======
link.href = styleUrl + '?r=' + Math.floor(Math.random() * 9999999999999999);
>>>>>>> develop
head.appendChild(link);  // Append link element to HTML head

// load HTML
var body = document.getElementsByTagName('body')[0];
boxHtml = `
  <div id="bookmarklet">
    <a href="#" id="close">&times;</a>
<<<<<<< HEAD
    <h1>Select an image to bookmark: </h1>
=======
    <h1>Select an image to bookmark:</h1>
>>>>>>> develop
    <div class="images"></div>
  </div>`;
body.innerHTML += boxHtml;

function bookmarkletLaunch() {
  bookmarklet = document.getElementById('bookmarklet');
  var imagesFound = bookmarklet.querySelector('.images');

  // clear images found
  imagesFound.innerHTML = '';
  // display bookmarklet
  bookmarklet.style.display = 'block';

  // close event
  bookmarklet.querySelector('#close')
<<<<<<< HEAD
             .addEventListener('click', function(){
    bookmarklet.style.display = 'none'
  });
=======
    .addEventListener('click', function () {
      bookmarklet.style.display = 'none'
    });
>>>>>>> develop

  // find images in the DOM with the minimum dimensions
  images = document.querySelectorAll('img[src$=".jpg"], img[src$=".jpeg"], img[src$=".png"]');
  images.forEach(image => {
<<<<<<< HEAD
    if(image.naturalWidth >= minWidth
       && image.naturalHeight >= minHeight)
    {
=======
    if (image.naturalWidth >= minWidth
      && image.naturalHeight >= minHeight) {
>>>>>>> develop
      var imageFound = document.createElement('img');
      imageFound.src = image.src;
      imagesFound.append(imageFound);
    }
  })

  // select image event
  imagesFound.querySelectorAll('img').forEach(image => {
<<<<<<< HEAD
    image.addEventListener('click', function(event){
      imageSelected = event.target;
      bookmarklet.style.display = 'none';
      window.open(siteUrl + 'images/create/?url='
                  + encodeURIComponent(imageSelected.src)
                  + '&title='
                  + encodeURIComponent(document.title),
                  '_blank');
=======
    image.addEventListener('click', function (event) {
      imageSelected = event.target;
      bookmarklet.style.display = 'none';
      window.open(siteUrl + 'images/create/?url='
        + encodeURIComponent(imageSelected.src)
        + '&title='
        + encodeURIComponent(document.title),
        '_blank');
>>>>>>> develop
    })
  })
}

// launch the bookmkarklet
bookmarkletLaunch();
