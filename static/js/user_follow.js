import anchorAction from './anchorAction.js'

// const userFollow = () => {
//     const aButton = document.querySelector("a.follow")
//     // let lastRequestTime = 0
//     // const throttleDelay = 5000

//     let options = {
//         method: "POST",
//         headers: { "X-CSRFToken": csrftoken },
//         mode: "same-origin",
//     }

//     aButton.addEventListener("click", (event) => {
//         // const now = Date.now()
//         // if (now - lastRequestTime < throttleDelay) {
//         //     console.log("Request throttled...")
//         //     return
//         // }
//         // lastRequestTime = now

//         event.preventDefault()

//         aButton.classList.add("disabled")
//         aButton.innerHTML = "Processing..."

//         const url = 'follow/'
//         let followButton = event.target


//         //* add request body 
//         let formData = new FormData()
//         formData.append("id", followButton.dataset.id)
//         formData.append("action", followButton.dataset.action)
//         options["body"] = formData

//         //* send HTTP request 
//         fetch(url, options)
//             .then(response => response.json())
//             .then(data => {
//                 if (data["status"] === "ok") {
//                     let previousAction = followButton.dataset.action

//                     //* toggle button text and data-action 
//                     let action = previousAction === "follow" ? "unfollow" : "follow"
//                     followButton.dataset.action = action
//                     followButton.innerHTML = action

//                     //* update follower count 
//                     let followerCount = document.querySelector("span.count .total")
//                     let totalFollowers = parseInt(followerCount.innerHTML)
//                     let followWord = "followers"
//                     totalFollowers = previousAction === "follow" ? totalFollowers + 1 : totalFollowers - 1
//                     followWord = totalFollowers === 1 ? followWord = "follower" : followWord
//                     followerCount.innerHTML = `${totalFollowers} ${followWord}`
//                 }
//             })
//             .catch(error => {
//                 console.error("Follow request failed:", error)
//             })
//             .finally(() => {
//                 aButton.classList.remove("disabled")
//             })
//     })
// }
// userFollow()

const userFollow = (previousAction, actionButton) => {
    //* toggle button text and data-action 
    const action = previousAction === "follow" ? "unfollow" : "follow"

    actionButton.dataset.action = action
    actionButton.innerHTML = action

    //* update follower count 
    let followerCount = document.querySelector("span.count .total")
    let totalFollowers = parseInt(followerCount.innerHTML)
    let followWord = "followers"

    totalFollowers = previousAction === "follow" ? totalFollowers + 1 : totalFollowers - 1
    followWord = totalFollowers === 1 ? "follower" : "followers"
    followerCount.innerHTML = `${totalFollowers} ${followWord}`
}

anchorAction("a.follow", 'follow/', userFollow)