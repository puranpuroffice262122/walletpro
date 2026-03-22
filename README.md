# WalletPro — Django + PostgreSQL

**PHP se Django mein convert kiya gaya wallet system**

## Features
- User Registration + KYC (ID Upload)
- Deposit / Withdrawal with Admin Approval
- Modern Dark Admin Panel
- Real-time Balance Refresh
- Products + Orders
- Notifications System
- PostgreSQL Database

## Local Setup (Apne PC pe)

### Requirements
- Python 3.10+
- PostgreSQL installed

### Step 1: PostgreSQL Database banao
```sql
psql -U postgres
CREATE DATABASE walletpro;
\q
```

### Step 2: Dependencies install karo
```bash
pip install -r requirements.txt
```

### Step 3: .env file banao
```bash
cp .env.example .env
# .env mein apna DB password bharo
```

### Step 4: Migrations run karo
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 5: Admin user banao
```bash
python manage.py create_admin
# Email: admin@walletpro.com | Password: admin123
```

### Step 6: Server start karo
```bash
python manage.py runserver
```

## URLs
| Page | URL |
|------|-----|
| User Dashboard | http://localhost:8000/wallet/dashboard/ |
| User Login | http://localhost:8000/accounts/login/ |
| Admin Panel | http://localhost:8000/admin-panel/ |
| Django Admin | http://localhost:8000/django-admin/ |

---

## FREE Live Deployment — Railway.app ⭐

### Step 1: GitHub pe upload karo
```bash
git init
git add .
git commit -m "WalletPro Django"
git remote add origin https://github.com/YOURUSERNAME/walletpro.git
git push -u origin main
```

### Step 2: Railway pe deploy
1. https://railway.app → Sign up (GitHub se)
2. **New Project** → **Deploy from GitHub Repo**
3. Apna `walletpro` repo select karo
4. **Add Service** → **Database** → **PostgreSQL** add karo
5. Variables mein jaao → Add karo:
   - `SECRET_KEY` = (koi random string)
   - `DEBUG` = `False`
   - `DJANGO_SETTINGS_MODULE` = `walletpro.settings`
   - Railway automatically `DATABASE_URL` set karta hai

### Step 3: Build commands set karo
Railway Settings → Deploy:
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `gunicorn walletpro.wsgi`

### Step 4: After deploy — migrations run karo
Railway → your service → **Shell** tab:
```bash
python manage.py migrate
python manage.py create_admin
python manage.py collectstatic --noinput
```

**Done! Your site is live!** 🎉

---

## Render.com pe Deploy

1. https://render.com → New Web Service
2. GitHub repo connect karo
3. Settings:
   - **Build Command:** `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
   - **Start Command:** `gunicorn walletpro.wsgi`
4. **New PostgreSQL** database add karo
5. `DATABASE_URL` env variable auto-set hoga
6. `SECRET_KEY` and `DEBUG=False` add karo

---

## Default Credentials
| Role | Email | Password |
|------|-------|---------|
| Admin | admin@walletpro.com | admin123 |

> ⚠️ Production mein password zaroor change karo!

## Project Structure
```
walletpro/
├── accounts/       → Auth, User model, Profile
├── wallet/         → Dashboard, Deposit, Withdraw, Transactions
├── adminpanel/     → Admin views (Users, Deposits, Withdrawals)
├── templates/      → HTML templates
├── static/         → CSS/JS files
├── requirements.txt
├── Procfile        → Railway/Heroku
└── runtime.txt     → Python version
```
