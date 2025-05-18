function imageLike() {

    var options = {
        method: "POST",
        headers: { "X-CSRFToken": csrftoken },
        mode: "same-origin",
    };

    document.addEventListener("click", function (event) {
        if (event.target.matches("a.like")) {
            event.preventDefault();

            const url = event.target.href;
            var likeButton = event.target;

            //* Create form data to send in the request
            var formData = new FormData();
            formData.append("id", likeButton.dataset.id);
            formData.append("action", likeButton.dataset.action);
            options["body"] = formData;

            //* Send the fetch request
            fetch(url, options)
                .then(response => response.json())
                .then(data => {
                    if (data["status"] === "ok") {
                        var previousAction = likeButton.dataset.action;

                        //* Toggle button text and data-action 
                        var action = previousAction === "like" ? "dislike" : "like";
                        likeButton.dataset.action = action;
                        likeButton.innerHTML = action;

                        //* Update like count 
                        var likeCount = document.querySelector("span.count .total");
                        var totalLikes = parseInt(likeCount.innerHTML);
                        var likeWord = "like";
                        totalLikes = previousAction === "like" ? totalLikes + 1 : totalLikes - 1;
                        likeWord = totalLikes !== 1 ? "likes" : "like";
                        likeCount.innerHTML = `${totalLikes} ${likeWord}`;

                        //* Update users like information 
                        var usersLike = document.getElementById("image-likes");
                        usersLike.innerHTML = ""; // Clear exising content

                        var pUsersLike = document.createElement("p");
                        pUsersLike.textContent = "Users Like:";
                        pUsersLike.classList.add("image-detail");
                        usersLike.appendChild(pUsersLike);

                        if (totalLikes === 0) {
                            var txtDiv = document.createElement("div");
                            var txtNoLikesYet = document.createElement("p");
                            txtNoLikesYet.textContent = "Nobody likes this image yet";
                            txtDiv.appendChild(txtNoLikesYet);
                            usersLike.appendChild(txtDiv);
                        } else {
                            data["users_like"].forEach(user => {
                                var userDiv = document.createElement("div");
                                userDiv.classList.add("image-likes");

                                if (user.profile_photo) {
                                    var img = document.createElement("img");
                                    img.src = user.profile_photo;
                                    userDiv.appendChild(img);
                                }

                                var p = document.createElement("p");
                                p.textContent = user.first_name;
                                userDiv.appendChild(p);
                                usersLike.appendChild(userDiv);

                                var a = document.createElement("a");
                                a.href = user.profile_url;
                                console.log(user)
                                a.appendChild(img)
                                a.appendChild(p)

                                userDiv.appendChild(a);
                                usersLike.appendChild(userDiv);
                            });
                        };
                    };
                })
                .catch(error => {
                    console.error("Error:", error);
                });
        };
    });
}
imageLike();