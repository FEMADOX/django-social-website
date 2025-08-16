const anchorAction = (htmlElement, href, func) => {
  const aButton = document.querySelector(htmlElement)
  const throttleDelay = 3000
  let lastRequestTime = 0

  let options = {
    method: "POST",
    headers: { "X-CSRFToken": csrftoken },
    mode: "same-origin",
  }

  aButton.addEventListener("click", (event) => {
    event.preventDefault()
    const now = Date.now()
    if (now - lastRequestTime < throttleDelay) {
      console.log("Request throttled...")
      return
    }
    lastRequestTime = now

    aButton.classList.add("disabled")
    aButton.innerHTML = "Processing..."

    setTimeout(() => {
      const url = href ? href : event.target.href
      let actionButton = event.target


      //* add request body 
      let formData = new FormData()
      formData.append("id", actionButton.dataset.id)
      formData.append("action", actionButton.dataset.action)
      options["body"] = formData

      //* send HTTP request 
      fetch(url, options)
        .then(response => response.json())
        .then(data => {
          if (data["status"] === "ok") {
            let previousAction = actionButton.dataset.action

            func(previousAction, actionButton, data)
          }
        })
        .catch(error => {
          console.error("Request failed:", error)
        })
        .finally(() => {
          aButton.classList.remove("disabled")
        })
    }, 1000)
  })
}

export default anchorAction