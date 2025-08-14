function userFollow() {
    const url = "follow/"

    let options = {
        method: "POST",
        headers: { "X-CSRFToken": csrftoken },
        mode: "same-origin",
    }

    document.addEventListener("click", function (event) {
        if (event.target.matches("a.follow")) {
            event.preventDefault()
            let followButton = event.target

            //* add request body 
            let formData = new FormData()
            formData.append("id", followButton.dataset.id)
            formData.append("action", followButton.dataset.action)
            options["body"] = formData

            //* send HTTP request 
            fetch(url, options).then(response => response.json()).then(data => {
                if (data["status"] === "ok") {
                    let previousAction = followButton.dataset.action

                    //* toggle button text and data-action 
                    let action = previousAction === "follow" ? "unfollow" : "follow"
                    followButton.dataset.action = action
                    followButton.innerHTML = action

                    //* update follower count 
                    let followerCount = document.querySelector("span.count .total")
                    let totalFollowers = parseInt(followerCount.innerHTML)
                    let followWord = "followers"
                    totalFollowers = previousAction === "follow" ? totalFollowers + 1 : totalFollowers - 1
                    followWord = totalFollowers === 1 ? followWord = "follower" : followWord
                    followerCount.innerHTML = `${totalFollowers} ${followWord}`
                }
            })
        }
    })
}

userFollow()