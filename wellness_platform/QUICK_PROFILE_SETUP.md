# Quick Setup Guide - Profile System

## Prerequisites Check ✓

Before proceeding, ensure you have:
- Python 3.8 or higher installed
- Django installed (or requirements.txt ready)
- Access to the project directory

## Fast Setup (5 Steps)

### 1️⃣ Navigate to Project
```powershell
cd "c:\Users\Windows 10\OneDrive\Desktop\pulsewell\wellness_platform"
```

### 2️⃣ Activate Virtual Environment (Optional but Recommended)
```powershell
# If you have a venv folder:
..\venv\Scripts\Activate.ps1

# If you need to create one:
cd ..
python -m venv venv
cd wellness_platform
..\venv\Scripts\Activate.ps1
```

### 3️⃣ Install Dependencies
```powershell
pip install -r requirements.txt
```

### 4️⃣ Run Migrations
```powershell
python manage.py makemigrations profiles
python manage.py migrate
```

### 5️⃣ Create Media Directory
```powershell
mkdir media
mkdir media\profile_pictures
```

## Start Server & Test

```powershell
python manage.py runserver
```

Open browser: http://127.0.0.1:8000/

## Quick Test Flow

1. Register a new user at `/accounts/register/`
2. Login at `/accounts/login/`
3. View dashboard (you'll see the profile card)
4. Click "View Full Profile" or go to `/profile/`
5. Click "Edit Profile" to add information
6. Upload a profile picture
7. Save changes

## Done! ✅

Your profile management system is now live!

---

## Troubleshooting

**Django not found?**
```powershell
pip install django
```

**Migration errors?**
```powershell
python manage.py migrate --run-syncdb
```

**Port 8000 in use?**
```powershell
python manage.py runserver 8080
```

See PROFILE_SETUP.md for detailed documentation.
