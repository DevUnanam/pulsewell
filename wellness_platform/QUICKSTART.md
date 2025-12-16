# 🚀 Quick Start Guide - PulseWell

## Run These Commands to Get Started

### 1. Navigate to Project Directory
```bash
cd "c:\Users\Windows 10\OneDrive\Desktop\pulsewell\wellness_platform"
```

### 2. Install Django (if needed)
```bash
pip install django
```

### 3. Create Database Tables
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Create Admin User (Optional but Recommended)
```bash
python manage.py createsuperuser
```
Follow the prompts to create your admin account.

### 5. Start the Development Server
```bash
python manage.py runserver
```

### 6. Open Your Browser
Visit: **http://127.0.0.1:8000/**

---

## What You'll See

1. **Homepage** → Automatically redirects to Login page
2. **Login Page** → Beautiful gradient design with dark mode
3. **Register Link** → Click to create a new account
4. **After Login** → Redirected to Dashboard
5. **Dashboard** → See your wellness overview with stats

---

## Test the System

### Create a Test User
1. Go to: http://127.0.0.1:8000/account/register/
2. Fill in the form:
   - Username: testuser
   - Email: test@example.com
   - Password: TestPass123!
   - Confirm Password: TestPass123!
3. Click "Create Account"
4. You'll be automatically logged in and redirected to dashboard

### Test Login
1. Logout (click the Logout button)
2. Go to: http://127.0.0.1:8000/account/login/
3. Enter your credentials
4. Click "Sign In"
5. You'll be redirected to the dashboard

---

## Pages to Explore

| URL | Description | Auth Required |
|-----|-------------|---------------|
| `/` | Homepage (redirects to login) | No |
| `/account/login/` | Login page | No |
| `/account/register/` | Registration page | No |
| `/account/logout/` | Logout (redirects to login) | Yes |
| `/account/profile/` | User profile page | Yes |
| `/dashboard/` | Main dashboard | Yes |
| `/admin/` | Django admin panel | Yes (superuser) |

---

## Features to Test

### ✅ Registration
- [ ] Fill out registration form
- [ ] See validation errors for invalid input
- [ ] Successfully create account
- [ ] Auto-login after registration

### ✅ Login
- [ ] Enter valid credentials
- [ ] See error for invalid credentials
- [ ] Successfully login
- [ ] Redirect to dashboard

### ✅ Dark Mode
- [ ] Click the moon/sun icon
- [ ] See theme change
- [ ] Reload page - theme should persist

### ✅ Protected Routes
- [ ] Try accessing `/dashboard/` without login
- [ ] Should redirect to login page
- [ ] Login and access dashboard successfully

---

## Troubleshooting

### Issue: "No module named 'django'"
**Solution**: Install Django
```bash
pip install django
```

### Issue: "Table doesn't exist"
**Solution**: Run migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Issue: "Static files not loading"
**Solution**: Check that `output.css` exists in `static/css/`

### Issue: "Template not found"
**Solution**: Check that templates are in the correct directory structure

---

## Next Steps After Testing

1. ✅ Verify all pages load correctly
2. ✅ Test registration and login flow
3. ✅ Check dark mode toggle
4. ✅ Explore dashboard features
5. 🔨 Start building additional features (habits, mood, journal, etc.)

---

## Need Help?

Check these files for detailed information:
- `SETUP_COMPLETE.md` - Complete setup summary
- `ACCOUNT_SETUP.md` - Detailed account app documentation

---

**Ready to roll! Your authentication system is fully functional.** 🎉
