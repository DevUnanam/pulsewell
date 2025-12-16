# Profile Management System - Setup Complete! 🎉

## ✅ What Has Been Completed

### 1. Profile Model Enhancement
- **Extended UserProfile model** with 20+ comprehensive fields:
  - Profile picture upload (ImageField)
  - Phone number and date of birth
  - Gender selection
  - Complete address (line1, line2, city, state, postal_code, country)
  - Health metrics (height, weight, unit_preference)
  - Wellness goals, medical conditions, allergies
  - Privacy settings (profile_visibility, show_email)
  - Tags/interests (Many-to-Many relationship)
  - Helper methods: `get_age()`, `get_bmi()`

### 2. Profile Forms Created
- **UserUpdateForm**: Update email, first name, last name
- **ProfileUpdateForm**: Update all profile fields with Tailwind styling
- **AccountDeleteForm**: Password confirmation for account deletion

### 3. Profile Views Implemented
- **profile_view**: Display user profile with calculated age and BMI
- **profile_edit**: Combined user and profile form editing
- **account_settings**: Settings page (expandable)
- **account_delete**: Secure account deletion with password verification

### 4. Beautiful Templates Created
- **profile_view.html**: Comprehensive profile display with:
  - Profile picture or avatar initial
  - Personal information card
  - Address card (conditional display)
  - Health stats with color-coded cards
  - Wellness goals section
  - Account information
  - Edit and Settings action buttons

- **profile_edit.html**: Organized edit form with sections:
  - Account information
  - Profile picture upload with preview
  - Personal details
  - Address information
  - Health metrics
  - Privacy settings
  - Save/Cancel buttons

- **account_delete.html**: Security-focused deletion page with:
  - Warning banners
  - Information about what will be deleted
  - Password confirmation
  - Confirmation checkbox
  - Danger zone styling

### 5. Dashboard Integration
- Updated user dashboard to include:
  - Profile card with picture and name
  - "View Full Profile" button
  - "Edit" quick link
  - Profile picture in navbar (uses {% if user.userprofile.profile_picture %})

### 6. URL Configuration
- Set up profiles app URLs:
  - `/profile/` - View profile
  - `/profile/edit/` - Edit profile
  - `/profile/settings/` - Account settings
  - `/profile/delete/` - Delete account

### 7. Media File Configuration
- Added MEDIA_URL = '/media/' to settings.py
- Added MEDIA_ROOT = BASE_DIR / 'media'
- Configured URL patterns to serve media files in DEBUG mode

### 8. Admin Interface
- Registered UserProfile and Tag models
- Created organized fieldsets for better admin experience

## 🔧 Setup Steps Required

### Step 1: Activate Virtual Environment (if you have one)
If you're using a virtual environment, activate it first:

**Windows:**
```powershell
# If using venv
.\venv\Scripts\Activate.ps1

# If using virtualenv
.\env\Scripts\Activate.ps1
```

**If you don't have a virtual environment**, create one:
```powershell
# Navigate to project root
cd "c:\Users\Windows 10\OneDrive\Desktop\pulsewell"

# Create virtual environment
python -m venv venv

# Activate it
.\venv\Scripts\Activate.ps1
```

### Step 2: Install Django (if not already installed)
```powershell
cd "c:\Users\Windows 10\OneDrive\Desktop\pulsewell\wellness_platform"
pip install -r requirements.txt
```

### Step 3: Run Migrations
```powershell
# Create migration files for profiles app
python manage.py makemigrations profiles

# Apply all migrations
python manage.py migrate
```

### Step 4: Create Media Directory
```powershell
# Create media directory for uploaded files
New-Item -ItemType Directory -Path "media" -Force
New-Item -ItemType Directory -Path "media\profile_pictures" -Force
```

### Step 5: Test the Application
```powershell
# Start development server
python manage.py runserver

# Open browser to http://127.0.0.1:8000/
```

## 🧪 Testing Checklist

After running migrations and starting the server, test these features:

### 1. User Registration & Login
- [ ] Register a new user account
- [ ] Log in with credentials
- [ ] Verify redirect to user dashboard

### 2. Profile Management
- [ ] View profile at `/profile/`
- [ ] Click "Edit Profile" button
- [ ] Upload a profile picture
- [ ] Fill in personal details (phone, date of birth, gender)
- [ ] Add address information
- [ ] Enter health metrics (height, weight)
- [ ] Set wellness goals
- [ ] Save changes
- [ ] Verify profile displays correctly

### 3. Dashboard Integration
- [ ] Check profile card appears on dashboard
- [ ] Verify profile picture displays
- [ ] Click "View Full Profile" button
- [ ] Test "Edit" quick link

### 4. Account Deletion
- [ ] Navigate to Settings
- [ ] Click "Delete Account"
- [ ] Try to delete without password (should fail)
- [ ] Try to delete without checkbox (should fail)
- [ ] Enter password and check box
- [ ] Confirm deletion works and user is logged out

### 5. Privacy Settings
- [ ] Toggle profile visibility
- [ ] Toggle show email setting
- [ ] Verify settings save correctly

## 📁 Project Structure

```
wellness_platform/
├── profiles/
│   ├── models.py          # UserProfile model with 20+ fields
│   ├── forms.py           # UserUpdateForm, ProfileUpdateForm, AccountDeleteForm
│   ├── views.py           # profile_view, profile_edit, account_settings, account_delete
│   ├── urls.py            # URL patterns
│   ├── admin.py           # Admin configuration
│   └── migrations/        # Database migrations (run makemigrations to create)
├── templates/
│   ├── profiles/
│   │   ├── profile_view.html     # Profile display template
│   │   ├── profile_edit.html     # Profile edit form
│   │   └── account_delete.html   # Account deletion template
│   └── dashboard/
│       └── user_dashboard.html   # Updated with profile card
├── media/                 # Upload directory (create with mkdir)
│   └── profile_pictures/  # Profile pictures storage
└── wellness_platform/
    ├── settings.py        # Updated with MEDIA_URL and MEDIA_ROOT
    └── urls.py            # Includes profiles URLs and media serving
```

## 🎨 Features Implemented

### Profile Fields
- ✅ Profile picture with upload capability
- ✅ Phone number
- ✅ Date of birth (with automatic age calculation)
- ✅ Gender selection
- ✅ Complete address (6 fields)
- ✅ Height and weight
- ✅ Unit preference (metric/imperial)
- ✅ Bio/description
- ✅ Wellness goals
- ✅ Medical conditions
- ✅ Allergies
- ✅ Privacy settings
- ✅ Interests/Tags (Many-to-Many)

### User Experience
- ✅ Beautiful Tailwind CSS styling with dark mode
- ✅ Responsive design for mobile/tablet/desktop
- ✅ Color-coded health metrics cards
- ✅ BMI calculation and display
- ✅ Conditional section display (address only shown if filled)
- ✅ Form validation with error messages
- ✅ Success/error message feedback
- ✅ Profile picture preview on edit page
- ✅ Avatar fallback (user's first initial)

### Security
- ✅ @login_required decorators on all views
- ✅ Password verification for account deletion
- ✅ Confirmation checkbox for destructive actions
- ✅ CSRF protection on all forms
- ✅ Proper user.delete() and logout on deletion

### Integration
- ✅ Dashboard profile card with quick access
- ✅ Navbar profile link
- ✅ Auto-creation of profiles via signals
- ✅ Seamless navigation between dashboard and profile

## 🚀 Next Steps (Optional Enhancements)

1. **Profile Picture Cropping**
   - Add image cropping library (django-image-cropping)
   - Allow users to crop uploaded images

2. **Profile Completion Progress**
   - Add progress bar showing % of profile completed
   - Encourage users to fill in all fields

3. **Social Features**
   - Public profile pages (if profile_visibility is True)
   - Follow/friend system
   - Activity feed

4. **Health Tracking**
   - Connect profile to habits/workouts/nutrition
   - Display stats from other apps on profile
   - Health trend charts

5. **Account Export**
   - Allow users to export their data before deletion
   - GDPR compliance feature

## 📝 Important Notes

### Profile Auto-Creation
Profiles are automatically created for new users via Django signals in `profiles/models.py`:
```python
@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
```

### Media Files in Production
For production deployment:
1. Configure cloud storage (AWS S3, Azure Blob, etc.)
2. Install django-storages
3. Update settings.py with storage backend
4. Set up CDN for media files

### Database Considerations
- Profile pictures are stored as file paths in the database
- Actual images are stored in `media/profile_pictures/`
- Consider image optimization for better performance
- Implement image size limits in forms

## 🐛 Troubleshooting

### Migration Issues
If migrations fail:
```powershell
# Reset profiles migrations (DANGER: loses data!)
python manage.py migrate profiles zero
# Delete migration files in profiles/migrations/ (except __init__.py)
# Then run:
python manage.py makemigrations profiles
python manage.py migrate
```

### Media Files Not Showing
1. Check MEDIA_URL and MEDIA_ROOT in settings.py
2. Verify media URL patterns in wellness_platform/urls.py
3. Ensure DEBUG = True for development
4. Check file permissions on media directory

### Profile Not Created
If a user doesn't have a profile:
```python
# In Django shell
python manage.py shell
from account.models import CustomUser
from profiles.models import UserProfile

user = CustomUser.objects.get(username='username')
UserProfile.objects.create(user=user)
```

## ✨ Congratulations!

Your comprehensive profile management system is complete! Users can now:
- Create detailed profiles with personal information
- Upload profile pictures
- Track health metrics
- Set wellness goals
- Manage privacy settings
- Edit their information anytime
- Delete their accounts securely

The system is fully integrated with your dashboard and uses beautiful, modern UI with dark mode support!
