(function () {
    const develop = location.host === '127.0.0.1:8000';
    const domain = develop ? '127.0.0.1:8000' : 'django-social-website-hade.onrender.com';

    if (!window.bookmarklet) {
        bookmarklet_js = document.body.appendChild(document.createElement('script'));
        bookmarklet_js.src =
            '//' + domain + '/static/js/bookmarklet.js?r=' + Math.floor(Math.random() * 9999999999999999);
        window.bookmarklet = true;
    } else {
        bookmarkletLaunch();
    };
})();
