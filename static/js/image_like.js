import anchorAction from './anchorAction.js'

const imageLike = (previousAction, actionButton, data) => {
    //* Toggle button text and data-action 
    const action = previousAction === "like" ? "dislike" : "like"

    actionButton.dataset.action = action
    actionButton.innerHTML = action

    //* Update like count 
    let likeCount = document.querySelector("span.count .total")
    let totalLikes = parseInt(likeCount.innerHTML)
    let likeWord = "like"

    totalLikes = previousAction === "like" ? totalLikes + 1 : totalLikes - 1
    likeWord = totalLikes !== 1 ? "likes" : "like"
    likeCount.innerHTML = `${totalLikes} ${likeWord}`

    //* Update users like information 
    let usersLike = document.getElementById("image-likes")

    usersLike.innerHTML = "" // Clear exising content

    let pUsersLike = document.createElement("p")

    pUsersLike.textContent = "Users Like:"
    pUsersLike.classList.add("image-detail")
    usersLike.appendChild(pUsersLike)

    if (totalLikes === 0) {
        let txtDiv = document.createElement("div")
        let txtNoLikesYet = document.createElement("p")

        txtNoLikesYet.textContent = "Nobody likes this image yet"
        txtDiv.appendChild(txtNoLikesYet)
        usersLike.appendChild(txtDiv)
    } else {
        data["users_like"].forEach(user => {
            let userDiv = document.createElement("div")
            let img = document.createElement("img")

            userDiv.classList.add("image-likes")

            if (user.profile_photo) {
                img.src = user.profile_photo
                userDiv.appendChild(img)
            }

            let p = document.createElement("p")

            p.textContent = user.first_name
            userDiv.appendChild(p)
            usersLike.appendChild(userDiv)

            let a = document.createElement("a")

            a.href = user.profile_url
            a.appendChild(img)
            a.appendChild(p)

            userDiv.appendChild(a)
            usersLike.appendChild(userDiv)
        })
    };
}

anchorAction('a.like', null, imageLike)