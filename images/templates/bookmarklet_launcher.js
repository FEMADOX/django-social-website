(function () {
    if (!window.bookmarklet) {
        bookmarklet_js = document.body.appendChild(document.createElement('script'));
        bookmarklet_js.src =
        '//django-social-website.up.railway.app/static/js/bookmarklet.js?r=' + Math.floor(Math.random() * 9999999999999999);
        window.bookmarklet = true;
    }
    else {
        bookmarkletLaunch();
    }
})();
