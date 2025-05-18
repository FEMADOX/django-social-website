var domain = window.location.host;

(function () {
    if (!window.bookmarklet) {
        bookmarklet_js = document.body.appendChild(document.createElement('script'));
        bookmarklet_js.src =
            '//' + domain + '/static/js/bookmarklet.js?r=' + Math.floor(Math.random() * 9999999999999999);
        window.bookmarklet = true;
    }
    else {
        bookmarkletLaunch();
    }
})();
