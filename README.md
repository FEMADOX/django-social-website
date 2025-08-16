# Django Social Website - Bookmarks

A full-featured social media platform built with Django that allows users to bookmark images, follow other users, and interact through likes and social authentication.

## 🚀 Features

### User Management

- **Custom User Registration** with email verification
- **Social Authentication** (Google & Twitter OAuth)
- **Password Reset** functionality via email
- **User Profiles** with photo uploads (Cloudinary integration)
- **Follow/Unfollow** system between users

### Image Bookmarking

- **Image Upload** from external URLs
- **Image Browsing** with infinite scroll pagination
- **Like/Unlike** functionality for images
- **Image Views** tracking
- **Bookmarklet** for easy image saving from any website

### Social Features

- **Activity Feed** showing actions from followed users
- **Real-time Interactions** with AJAX
- **User Discovery** with people listing
- **Activity Tracking** (likes, follows, bookmarks)

### UI/UX

- **Dark/Light Mode** toggle
- **Responsive Design**
- **Live Reload** during development
- **Custom CSS** with modern styling

## 🛠️ Technology Stack

- **Backend**: Django 5.1.2
- **Database**: PostgreSQL (production) / SQLite (development)
- **Media Storage**: Cloudinary
- **Authentication**: Django Allauth
- **Frontend**: HTML, CSS, JavaScript (Vanilla)
- **Deployment**: Render/Railway compatible
- **Email**: SMTP (Gmail)

## 📦 Dependencies

### Core Dependencies

```toml
django>=5.1.2
django-allauth[socialaccount]>=65.8.0
cloudinary>=1.44.0
django-cloudinary-storage>=0.3.0
dj-database-url>=2.3.0
python-decouple>=3.8
psycopg2-binary>=2.9.10
gunicorn>=23.0.0
whitenoise>=6.9.0
```

### Development Dependencies

```toml
django-livereload-server>=0.5.1
django-extensions>=4.1
ipython>=9.2.0
```

## 🔧 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/FEMADOX/django-social-website.git
cd Social_Website
```

### 2. Environment Setup

Create a `.env` file with the following variables:

```env
# Django
SECRET_KEY="your-secret-key"
DEBUG=True
ALLOWED_HOSTS="127.0.0.1,localhost"
LOCAL_DATABASE=True

# Database (for production)
DATABASE_URL="postgresql://username:password@host:port/database"

# Social Authentication
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY="your-google-client-id"
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET="your-google-client-secret"
SOCIAL_AUTH_TWITTER_KEY="your-twitter-api-key"
SOCIAL_AUTH_TWITTER_SECRET="your-twitter-api-secret"

# Cloudinary
CLOUD_NAME="your-cloudinary-name"
CLOUD_API_KEY="your-cloudinary-api-key"
CLOUD_API_SECRET="your-cloudinary-api-secret"

# Email
EMAIL_HOST_USER="your-email@gmail.com"
EMAIL_HOST_PASSWORD="your-app-password"
```

### 3. Install Dependencies

```bash
# Using uv (recommended)
uv sync

# Or using pip
pip install -r requirements.txt
```

### 4. Database Setup

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### 5. Run Development Server

```bash
python manage.py runserver
```

## 📁 Project Structure

```text
Social_Website/
├── accounts/              # User management app
│   ├── models.py         # User profiles, contacts
│   ├── views.py          # Authentication, user management
│   ├── forms.py          # Registration, profile forms
│   └── emails.py         # Email verification
├── images/               # Image bookmarking app
│   ├── models.py         # Image model
│   ├── views.py          # Image CRUD, likes
│   └── forms.py          # Image upload forms
├── action/               # Activity tracking app
│   ├── models.py         # User actions
│   └── utils.py          # Action creation utilities
├── templates/            # HTML templates
│   ├── account/          # User templates
│   ├── images/           # Image templates
│   └── registration/     # Auth templates
├── static/               # Static files
│   ├── css/              # Stylesheets
│   └── js/               # JavaScript files
└── Bookmarks/            # Main project settings
    ├── settings.py       # Django configuration
    └── urls.py           # URL routing
```

## 🔐 Authentication Setup

### Google OAuth Setup

1. Go to [Google Developers Console](https://console.developers.google.com/)
2. Create a new project or select existing
3. Enable Google+ API
4. Create OAuth 2.0 credentials
5. Add redirect URI: `http://127.0.0.1:8000/accounts/google/login/callback/`

### Twitter OAuth Setup

1. Go to [Twitter Developer Portal](https://developer.twitter.com/)
2. Create a new app
3. Generate API keys and tokens
4. Add callback URL: `http://127.0.0.1:8000/accounts/twitter/login/callback/`

### Email Configuration

1. Enable 2-factor authentication on Gmail
2. Generate an App Password
3. Use the App Password in `EMAIL_HOST_PASSWORD`

## 🚀 Deployment

### Environment Variables for Production

```env
DEBUG=False
ALLOWED_HOSTS="your-domain.com"
LOCAL_DATABASE=False
DATABASE_URL="your-production-database-url"
```

### Collect Static Files

```bash
python manage.py collectstatic
```

### Run with Gunicorn

```bash
gunicorn Bookmarks.wsgi:application
```

## 📋 Usage

### User Registration Flow

1. User fills registration form
2. Email verification link sent
3. User clicks link to activate account
4. Profile creation page displayed
5. User can start using the platform

### Bookmarklet Usage

1. Drag the "Bookmark it" button to browser bookmarks
2. Navigate to any webpage with images
3. Click the bookmarklet
4. Select an image to bookmark
5. Add title and description

### Image Interaction

- **Like/Unlike**: Click heart button on images
- **View Details**: Click on image for full view
- **Infinite Scroll**: Scroll down to load more images

## 🤝 API Endpoints

### User Management Endpoints

- `GET /` - Dashboard
- `POST /register/` - User registration
- `GET /edit/` - Edit profile
- `GET /users/` - User listing
- `POST /users/follow/` - Follow/unfollow users

### Image Management

- `GET /images/` - Image listing
- `POST /images/create/` - Create image bookmark
- `GET /images/detail/<id>/<slug>/` - Image details
- `POST /images/like/` - Like/unlike image

## 🔧 Custom Features

### Dark Mode

- Toggle between light and dark themes
- Preference saved in localStorage
- CSS custom properties for theme switching

### Activity Feed

- Shows actions from followed users
- Prevents duplicate actions within 60 seconds
- Excludes admin user actions

### Email Verification

- Custom token generation
- Secure activation links
- Resend email functionality

## 🐛 Troubleshooting

### Email Not Sending

1. Check Gmail App Password is correct
2. Verify 2FA is enabled on Gmail
3. Check firewall settings for SMTP

### OAuth Not Working

1. Verify redirect URIs match exactly
2. Check API keys are correct
3. Ensure OAuth consent screen is configured

### Image Upload Issues

1. Verify Cloudinary credentials
2. Check file size limits
3. Ensure valid image extensions

## 📈 Performance Optimizations

- **Database Indexing** on frequently queried fields
- **Query Optimization** with select_related and prefetch_related
- **Static File Compression** with WhiteNoise
- **CDN Integration** with Cloudinary
- **Pagination** for large datasets

## 🔒 Security Features

- **CSRF Protection** on all forms
- **Email Verification** for new accounts
- **Secure Token Generation** for activation links
- **Input Validation** on all forms
- **SQL Injection Protection** via Django ORM

## 📝 License

This project is open source and available under the MIT License.

## 👥 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📞 Support

For support and questions:

- Create an issue on GitHub
- Check the Django documentation
- Review the django-allauth documentation

---

## Built with ❤️ using Django
