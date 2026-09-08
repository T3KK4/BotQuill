# The BotQuill Writer Portfolio & Blog

A Flask-powered portfolio and blog site for authors — built to help a writer track manuscript
progress privately, showcase finished novels and exclusive previews publicly, and sell e-book
access, all managed from a single writer-only dashboard.

## Features

**Public site**
- Home page introducing the writer, with featured novels and latest blog posts
- About page with bio, tagline, and skills (pulled from the writer's profile)
- Blog — an index of published posts with a single-post view
- Novel showcase — cover, blurb, completion date, and author name for each title
- Exclusive preview novels gated behind e-book purchase
- Contact page with the writer's info and a message form
- Checkout flow for buying e-book access (payment provider swappable — see below)

**Writer dashboard** (private, login-required)
- Manuscript tracker — title, status, word count progress, notes — **never exposed on any public route**
- Full CRUD for novels, blog posts, contact info, and the About page profile
- Contact form inbox (mark messages as read)
- Sales overview of e-book purchases

**Access control**
- Single writer account, no public registration route
- Manuscripts live in their own table with no public blueprint, route, or template that ever
  queries it — not just permission-gated, structurally unreachable from the public side
- E-book files are served only after a purchase is verified as paid

## Tech stack

- **Backend:** Flask, Flask-SQLAlchemy, Flask-Login, Flask-WTF (CSRF)
- **Frontend:** Jinja2 templates, hand-written CSS (Fraunces + Source Serif 4 for a literary
  editorial feel), vanilla JS
- **Database:** SQLite by default (swap `DATABASE_URL` for Postgres in production)
- **Payments:** provider-agnostic stub (`app/payments.py`) — currently simulates a successful
  payment with no real charge; drop in Paystack, Flutterwave, or Stripe later without touching
  the checkout routes

## Project structure

```
writer_site/
├── app/
│   ├── __init__.py        # app factory
│   ├── extensions.py      # db, login_manager, csrf — instantiated here to avoid circular imports
│   ├── models.py           # Writer, WriterProfile, ContactInfo, ContactMessage,
│   │                        # Manuscript, Novel, BlogPost, Purchase
│   ├── payments.py         # swappable payment provider stub
│   ├── auth/                # writer login/logout (no public registration)
│   ├── public/               # public routes: home, about, blog, novels, contact, checkout
│   ├── dashboard/            # writer-only CRUD, all routes @login_required
│   │   └── helpers.py        # file upload helpers (covers, e-book files)
│   ├── templates/
│   │   ├── public/
│   │   ├── auth/
│   │   └── dashboard/
│   └── static/
│       ├── css/
│       ├── js/
│       └── uploads/covers/
├── config.py
├── run.py
├── seed.py                 # creates the writer account + sample data
├── requirements.txt
└── .env.example
```

## Setup

1. **Clone and enter the project**
   ```bash
   git clone <repo-url>
   cd writer_site
   ```

2. **Create a virtual environment and install dependencies**
   ```bash
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```
   Then edit `.env` and set a real `SECRET_KEY`. Leave `PAYMENT_PROVIDER=stub` until a real
   gateway is chosen.

4. **Create the database and the writer account**
   ```bash
   python seed.py
   ```
   This creates the SQLite database, a singleton profile/contact row, and prompts for the
   writer's login email and password.

5. **Run the app**
   ```bash
   python run.py
   ```
   Visit `http://localhost:5000` for the public site and `http://localhost:5000/dashboard`
   for the writer dashboard (redirects to login first).

## Adding a real payment provider

`app/payments.py` exposes two functions the checkout routes call — `init_payment()` and
`verify_payment()`. To go live:

1. Add a branch for your provider (Paystack, Flutterwave, Stripe) inside those two functions.
2. Set `PAYMENT_PROVIDER` in `.env` to match.
3. No changes are needed in `app/public/routes.py` — it only ever calls the two abstracted
   functions.

## Notes on the manuscript/novel distinction

- **Manuscripts** are works in progress. They're for the writer's own tracking only — status,
  word count, notes — and have no public-facing route at all.
- **Novels** are finished, published titles meant to be shown off: title, author name,
  completion date, cover photo, and (optionally) an e-book file gated behind purchase.

## License

Add a license of your choice here (MIT is a common default for personal-site projects).
