
document.addEventListener("DOMContentLoaded", function () {
    const url = "/account/users/follow/"; // Asegúrate de que esta URL sea correcta
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    var options = {
        method: "POST",
        headers: { "X-CSRFToken": csrftoken },
        mode: "same-origin",
    };

    document.querySelector("a.follow").addEventListener("click", function (e) {
        e.preventDefault();
        var followButton = this;

        // Add request body
        var formData = new FormData();
        formData.append("id", followButton.dataset.id);
        formData.append("action", followButton.dataset.action);
        options["body"] = formData;

        // Send HTTP request
        fetch(url, options)
            .then((response) => response.json())
            .then((data) => {
                if (data["status"] === "ok") {
                    var previousAction = followButton.dataset.action;

                    // Toggle button text and data-action
                    var action = previousAction === "follow" ? "unfollow" : "follow";
                    followButton.dataset.action = action;
                    followButton.innerHTML = action;

                    // Update follower count
                    var followerCount = document.querySelector("span.count .total");
                    var totalFollowers = parseInt(followerCount.innerHTML);
                    var followWord = "followers";
                    totalFollowers =
                        previousAction === "follow"
                            ? totalFollowers + 1
                            : totalFollowers - 1;
                    followWord = totalFollowers === 1 ? "follower" : "followers";
                    followerCount.innerHTML = `${totalFollowers} ${followWord}`;
                }
            });
    });
});