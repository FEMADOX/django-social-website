import anchorAction from './anchorAction.js'

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