let page = 1
let emptyPage = false
let blockRequest = false

window.addEventListener("scroll", (event) => {
  // const margin = document.body.clientHeight - window.innerHeight - 200
  // if (window.pageYOffset > margin && !emptyPage && !blockRequest) {
  //   blockRequest = true
  //   page += 1
  //   fetch("?images_only=1&page=" + page)
  //     .then(response => response.text())
  //     .then(html => {
  //       if (html === "") {
  //         emptyPage = true
  //       } else {
  //         const imageList = document.getElementById("image-list")
  //         imageList.insertAdjacentHTML("beforeEnd", html)
  //         blockRequest = false
  //       }
  //     })
  // }
  const scrollPosition = window.pageYOffset + window.innerHeight
  const documentHeight = Math.max(
    document.body.scrollHeight,
    document.body.offsetHeight,
    document.documentElement.clientHeight,
    document.documentElement.scrollHeight,
    document.documentElement.offsetHeight
  )

  const threshold = documentHeight - 200

  if (scrollPosition >= threshold && !emptyPage && !blockRequest) {
    blockRequest = true
    page += 1


    fetch('?images_only=1&page=' + page)
      .then(response => response.text())
      .then(html => {
        if (html === '' || html.trim() === '') {
          emptyPage = true
        } else {
          const imageList = document.getElementById('image-list')
          if (imageList) {
            imageList.insertAdjacentHTML('beforeEnd', html)
          }
          blockRequest = false
        }
      })
      .catch(error => {
        console.error('Error fetching more images:', error)
        blockRequest = false
      })
  }
})

// Function to load the initial page if needed
const checkInitialLoad = () => {
  const imageList = document.getElementById('image-list')
  if (imageList) {
    const images = imageList.children.length

    if (images < 8 && !emptyPage && !blockRequest) {
      setTimeout(() => {
        window.dispatchEvent(new Event('scroll'))
      }, 500)
    }
  }
}

//* Launch scroll event
const scrollEvent = new Event('scroll')
window.dispatchEvent(scrollEvent)

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', checkInitialLoad)
} else {
  checkInitialLoad()
}