function userFollow() {
    const url = "follow/";

    var options = {
        method: "POST",
        headers: { "X-CSRFToken": csrftoken },
        mode: "same-origin",
    };

    document.addEventListener("click", function (event) {
        if (event.target.matches("a.follow")) {
            event.preventDefault();
            var followButton = event.target;

            //* add request body 
            var formData = new FormData();
            formData.append("id", followButton.dataset.id);
            formData.append("action", followButton.dataset.action);
            options["body"] = formData;

            //* send HTTP request 
            fetch(url, options).then(response => response.json()).then(data => {
                if (data["status"] === "ok") {
                    var previousAction = followButton.dataset.action;

                    //* toggle button text and data-action 
                    var action = previousAction === "follow" ? "unfollow" : "follow";
                    followButton.dataset.action = action;
                    followButton.innerHTML = action;

                    //* update follower count 
                    var followerCount = document.querySelector("span.count .total");
                    var totalFollowers = parseInt(followerCount.innerHTML);
                    var followWord = "followers";
                    totalFollowers = previousAction === "follow" ? totalFollowers + 1 : totalFollowers - 1;
                    followWord = totalFollowers === 1 ? followWord = "follower" : followWord;
                    followerCount.innerHTML = `${totalFollowers} ${followWord}`;
                };
            });
        };
    });
};

userFollow()