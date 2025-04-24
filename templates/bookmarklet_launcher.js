// import bookmarklet from 'static/js/bookmarklet.js';

(function () {
    if (!window.bookmarklet) {
        bookmarklet_js = document.body.appendChild(document.createElement('script'));
        bookmarklet_js.src =
<<<<<<< HEAD:images/templates/bookmarklet_launcher.js
        '//django-social-website.up.railway.app/static/js/bookmarklet.js?r=' + Math.floor(Math.random() * 9999999999999999);
=======
        '../static/js/bookmarklet.js?r=' + Math.floor(Math.random() * 9999999999999999);
>>>>>>> develop:templates/bookmarklet_launcher.js
        window.bookmarklet = true;
    }
    else {
        bookmarkletLaunch();
    }
})();
