# Account App Setup - PulseWell

## Overview
The account app has been fully configured with a modern authentication system including user registration, login, logout, and profile management.

## ✅ Completed Setup

### 1. **Settings Configuration** (`wellness_platform/settings.py`)
- ✅ Added all apps to `INSTALLED_APPS`
- ✅ Configured `AUTH_USER_MODEL = 'account.CustomUser'`
- ✅ Set up `TEMPLATES` directory
- ✅ Configured authentication URLs (LOGIN_URL, LOGIN_REDIRECT_URL, LOGOUT_REDIRECT_URL)

### 2. **Account App Files**

#### `models.py`
- ✅ CustomUser model with `is_admin` and `is_user` fields
- Extends Django's AbstractUser

#### `forms.py` ✨ NEW
- ✅ CustomUserCreationForm - Modern registration form with Tailwind CSS styling
- ✅ CustomAuthenticationForm - Modern login form with Tailwind CSS styling
- Includes proper field validation and styling

#### `views.py` ✨ NEW
- ✅ `register_view` - Handle user registration
- ✅ `login_view` - Handle user login
- ✅ `logout_view` - Handle user logout
- ✅ `profile_view` - Display user profile
- Includes proper authentication checks and message handling

#### `urls.py` ✨ NEW
```python
account/register/  -> register_view
account/login/     -> login_view
account/logout/    -> logout_view
account/profile/   -> profile_view
```

#### `admin.py` ✨ UPDATED
- ✅ Registered CustomUser with CustomUserAdmin
- ✅ Added custom fields to admin interface

### 3. **Templates**

#### `templates/base.html` ✨ UPDATED
- ✅ Proper static file loading with `{% load static %}`
- ✅ Tailwind CSS integration
- ✅ Dark mode support with localStorage persistence
- ✅ Theme toggle functionality
- ✅ Responsive design

#### `templates/accounts/login.html` ✨ NEW
- ✅ Modern gradient background
- ✅ Beautiful card design with shadows
- ✅ Form validation and error messages
- ✅ Dark mode support
- ✅ "Remember me" checkbox
- ✅ "Forgot password" link
- ✅ Link to registration page
- ✅ Responsive mobile-friendly design

#### `templates/accounts/register.html` ✨ NEW
- ✅ Modern gradient background
- ✅ Beautiful card design
- ✅ All form fields (username, email, first/last name, passwords)
- ✅ Field validation with helpful hints
- ✅ Terms & conditions checkbox
- ✅ Dark mode support
- ✅ Link to login page
- ✅ Responsive design

#### `templates/accounts/profile.html` ✨ NEW
- ✅ Navigation bar with theme toggle
- ✅ Profile header with gradient banner
- ✅ User avatar with initial
- ✅ Profile details in grid layout
- ✅ Quick links to dashboard, habits, journal
- ✅ Edit profile and change password buttons
- ✅ Fully responsive

### 4. **Main URLs** (`wellness_platform/urls.py`)
- ✅ Included account URLs
- ✅ Root URL redirects to login page

## 🚀 Next Steps

### 1. Install Dependencies (if not already done)
```bash
pip install django
```

### 2. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

### 4. Compile Tailwind CSS (if needed)
Make sure your Tailwind CSS is compiled. If using Tailwind CLI:
```bash
# In the wellness_platform directory
npx tailwindcss -i ./src/input.css -o ./static/css/output.css --watch
```

### 5. Run Development Server
```bash
python manage.py runserver
```

## 📱 Available URLs

- `/` - Redirects to login page
- `/account/login/` - User login page
- `/account/register/` - User registration page
- `/account/logout/` - Logout (requires authentication)
- `/account/profile/` - User profile page (requires authentication)
- `/admin/` - Django admin panel

## 🎨 Features

### Authentication System
- ✅ User registration with email validation
- ✅ Secure login/logout
- ✅ Password validation
- ✅ Session management
- ✅ Protected routes with `@login_required`

### UI/UX
- ✅ Modern, beautiful Tailwind CSS design
- ✅ Dark mode with toggle
- ✅ Gradient backgrounds
- ✅ Smooth transitions and animations
- ✅ Responsive mobile-first design
- ✅ Form validation with helpful error messages
- ✅ Success/error message notifications

### User Model
- ✅ Custom user model extending AbstractUser
- ✅ Additional fields: `is_admin`, `is_user`
- ✅ Standard Django user fields (username, email, first_name, last_name, etc.)

## 🔐 Security Features

- ✅ CSRF protection on all forms
- ✅ Password hashing
- ✅ Session-based authentication
- ✅ Login required decorators
- ✅ Redirect after authentication

## 📝 Notes

- All templates extend `base.html` for consistent styling
- Tailwind CSS classes are properly applied
- Dark mode persists across page reloads using localStorage
- Forms include proper validation and error handling
- Messages framework integrated for user feedback

## 🎯 Integration Points

The account app is ready to integrate with:
- Dashboard app (LOGIN_REDIRECT_URL points to 'dashboard:dashboard')
- Profiles app (for extended user information)
- All other wellness apps (habits, mood, journal, etc.)

## 🐛 Troubleshooting

### Django Import Errors
If you see Django import errors, make sure:
1. Django is installed: `pip install django`
2. Virtual environment is activated
3. Python interpreter is correctly configured in VS Code

### Template Not Found
If templates aren't loading:
1. Check `TEMPLATES` `DIRS` in settings.py includes `BASE_DIR / 'templates'`
2. Ensure template files are in the correct directory structure

### Static Files Not Loading
If Tailwind CSS isn't working:
1. Run `python manage.py collectstatic` (in production)
2. Ensure `STATICFILES_DIRS` is configured correctly
3. Compile Tailwind CSS if using the CLI

## ✅ Verification Checklist

- [x] Settings configured correctly
- [x] Custom user model created
- [x] Forms created with Tailwind styling
- [x] Views implemented with proper authentication
- [x] URLs configured
- [x] Admin registered
- [x] Templates created and styled
- [x] Base template updated with static loading
- [x] Dark mode functionality added
- [ ] Migrations run
- [ ] Superuser created
- [ ] Server tested

---

**Status**: ✅ Account app setup is complete and ready for testing!
