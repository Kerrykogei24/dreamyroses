# Dreamy Roses

The website for Dreamy Roses — personalised coloring books drawn by Miriam Maiko in Nairobi.

Built with Django 5. Four public pages (landing, about us, drawings, contact) plus an
admin where Miriam adds drawings and reads enquiries without touching any code.

---

## Run it on your machine

```bash
cd dreamyroses
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env               # then open .env and edit it

python manage.py migrate
python manage.py seed_drawings     # loads the nine sample pages into the gallery
python manage.py createsuperuser   # your login for the admin
python manage.py runserver
```

Open http://127.0.0.1:8000 for the site and http://127.0.0.1:8000/studio-admin/ for the admin.

---

## The admin

Log in at `/studio-admin/`.

**Drawings** — every page in the gallery. Upload the image, give it a title, pick a style
(portrait, couple, family, friends, anime, milestone), and add a one-line caption. Tick
**is featured** to show it on the landing page. **Position** controls the order — lower
numbers come first.

**Enquiries** — every message sent through the contact form, newest first. Tick **replied**
once you have answered so you can see what is still outstanding.

---

## Email

In development, messages print to the terminal instead of sending — useful for testing.

To send for real, fill these in `.env`:

```
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=miriammaiko368@gmail.com
EMAIL_HOST_PASSWORD=your-gmail-app-password
```

Gmail needs an **app password**, not your normal password. Turn on 2-step verification on the
Google account, then create one at myaccount.google.com → Security → App passwords.

Every enquiry is saved to the database as well, so nothing is lost if an email fails.

---

## Changing the contact details

Email, the Payhip shop link, social handles and location live in one place: the `BRAND`
dictionary near the bottom of `config/settings.py`. Change them there and they update across
the whole site — footer, contact page and every shop link.

---

## Putting it online

1. Set real values in `.env`: `DEBUG=False`, a long random `SECRET_KEY`,
   your domain in `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS`.
2. `python manage.py collectstatic`
3. Serve with gunicorn: `gunicorn config.wsgi` (Railway, Render and Fly all run this fine).
4. Uploaded drawings land in `media/`. On hosts with disposable disks, either attach a
   persistent volume or move media to S3 / Cloudinary.

SQLite is fine for this amount of traffic. If it ever outgrows it, swap `DATABASES` in
settings for Postgres.

---

## Project layout

```
dreamyroses/
├── config/            settings, urls, wsgi
├── studio/            the app: models, views, forms, admin
│   └── management/commands/seed_drawings.py
├── templates/
│   ├── base.html      header, footer, shared shell
│   └── pages/         home, about, drawings, contact
├── static/
│   ├── css/site.css   all styling, hand-written
│   ├── js/site.js     mobile menu + the drag-to-colour hero
│   └── img/           logo, wordmark, pattern, sample pages
└── media/             drawings uploaded through the admin
```

## A note on what goes in the gallery

The sample pages shipped here are drawn from customers' own photographs, which is the
studio's own work. The football page featuring Ronaldo, Messi, Neymar and Mbappé was left
out on purpose — those are real identifiable people alongside the Nike and FIFA marks, and
selling pages like that is the usual reason a Payhip or Etsy shop gets taken down. Keep the
shop to personal commissions and original styles.
