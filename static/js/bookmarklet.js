const develop = location.host === '127.0.0.1:8000'
const domain = develop ? '127.0.0.1:8000' : 'django-social-website-hade.onrender.com'

const siteUrl = '//' + domain + '/'
const styleUrl = siteUrl + 'static/css/bookmarklet.css'
const minWidth = 250
const minHeight = 250

// load CSS
let head = document.getElementsByTagName('head')[0]  // Get HTML head element
let link = document.createElement('link') // Create new link Element
link.rel = 'stylesheet' // set the attributes for link element
link.type = 'text/css'
link.href = styleUrl + '?r=' + Math.floor(Math.random() * 9999999999999999)
head.appendChild(link)  // Append link element to HTML head

// load HTML
let body = document.getElementsByTagName('body')[0]
boxHtml = `
  <div id="bookmarklet">
    <a href="#" id="close">&times;</a>
    <h1>Select an image to bookmark:</h1>
    <div class="images"></div>
  </div>
  `
body.innerHTML += boxHtml

const bookmarkletLaunch = () => {
    const bookmarklet = document.getElementById('bookmarklet')
    const imagesFound = bookmarklet.querySelector('.images')

    // clear images found
    imagesFound.innerHTML = ''
    // display bookmarklet
    bookmarklet.style.display = 'block'

    // close event
    bookmarklet.querySelector('#close')
        .addEventListener('click', () => {
            bookmarklet.style.display = 'none'
        })

    // find images in the DOM with the minimum dimensions
    const images = document.querySelectorAll('img[src$=".jpg"], img[src$=".jpeg"], img[src$=".png"]')
    images.forEach(image => {
        if (image.naturalWidth >= minWidth
            && image.naturalHeight >= minHeight) {
            let imageFound = document.createElement('img')
            imageFound.src = image.src
            imagesFound.append(imageFound)
        }
    })

    // select image event
    imagesFound.querySelectorAll('img').forEach(image => {
        image.addEventListener('click', (event) => {
            imageSelected = event.target
            bookmarklet.style.display = 'none'
            window.open(siteUrl + 'images/create/?url='
                + encodeURIComponent(imageSelected.src)
                + '&title='
                + encodeURIComponent(document.title),
                '_blank')
        })
    })
}

// launch the bookmkarklet
bookmarkletLaunch()
