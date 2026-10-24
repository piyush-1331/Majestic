# Majestic Interior & Furniture — Flask Web Application

A full-featured interior design and furniture e-commerce website built by integrating the Majestic HTML5/CSS3 template into a Python Flask backend. Developed as part of the **Project-Based Learning (PBL) Python Frameworks** curriculum for B.Tech Semester 5.

---

## 📌 Project Status & PBL Task Roadmap

| Task | Title | Description | Status |
| :---: | :--- | :--- | :---: |
| **Task 1** | **Website Integration Using Flask** | Converting static HTML/CSS/JS template into a structured Flask web app with dynamic routing. | ✅ **Completed** |
| **Task 2** | **User Login & Registration Pages** | Designing separate Login and Registration pages styled after `contact.html` with server-side validation. | ✅ **Completed** |
| **Task 3** | **Registration Processing & Home Display** | Processing registration POST data, storing in JSON, and rendering registered user cards on Home. | ✅ **Completed** |
| **Task 4** | **Email Notifications** | Automated login confirmation & security alert emails via SMTP with `.env` configuration. | ✅ **Completed** |
| **Task 5** | **Payment Gateway Integration** | Checkout and payment processing. | ⏳ *Not Implemented Yet* |

---

## 📖 Project Overview

The Majestic project transforms an elegant, multi-page static website template into a dynamic Python Flask web application. It retains all original design aesthetics—including typography (Titillium Web, Lato), responsive Bootstrap grids, FlexSlider banners, Chocolat lightbox galleries, and custom animations—while powering page delivery, client authentication flows, and automated email security notifications through Python.

---

## 💻 Coding Efforts

The primary development effort spans several architectural layers:

1. **Backend Routing & Control (`app.py`)**:
   - Structured entry point utilizing Flask with canonical route decorators.
   - Session-based feedback using `flask.flash()` and secret key configuration.
   - RESTful request handling supporting `GET` for page rendering and `POST` for form submissions.
2. **Dynamic Templating (Jinja2)**:
   - Asset linking transformed from hard-coded relative paths to `{{ url_for('static', filename='...') }}` across all 9 pages.
   - Internal navigation links rewritten to dynamic route endpoints using `{{ url_for(...) }}`.
   - Conditional rendering blocks (`{% if users %}`, `{% for user in users %}`, and `{% with messages = get_flashed_messages() %}`).
3. **Forms & Client Input Handling**:
   - Developed registration and login forms with appropriate HTML5 input types (`text`, `email`, `tel`, `password`).
   - Maintained visual harmony with the Majestic contact form layout.
4. **Data Persistence**:
   - Implemented JSON storage helper functions (`load_users()`, `save_users()`) to persist registered client records in `data/users.json`.
5. **Form Validation**:
   - Added robust server-side validation preventing blank fields, password mismatches, and duplicate email entries.
6. **SMTP Email Notification System (`smtplib`, `email.mime`)**:
   - Integrated automated email dispatch using Python's built-in `smtplib` and `email.mime` libraries with TLS support.
   - Designed dual-format (HTML and plain-text fallback) emails branded with Majestic theme styling (`#97262A`).
   - Implemented secure credential management via environment variables (`.env`) loaded by `python-dotenv`.
   - Added graceful simulation fallbacks so the application functions reliably in both connected and offline demonstration modes.

---

## 🛠️ Implementation Approach

The transition from a static website to an integrated Flask application was performed in four systematic phases:

### Phase 1: Task 1 — Flask Architecture & Routing
1. **Asset Restructuring**: Grouped CSS, JavaScript, images, and glyphicon fonts into the `static/` directory; moved HTML files into the `templates/` directory.
2. **Template Modernization**: Updated every asset reference (`<link>`, `<script>`, `<img>`, background lightbox links) to use `url_for('static', ...)`.
3. **Route Construction**: Created Flask view functions for all 7 original pages (`/`, `/about`, `/blog`, `/contact`, `/gallery`, `/pages`, `/single`).
4. **Navigation Updating**: Replaced `.html` href attributes with Jinja route calls.

### Phase 2: Task 2 — Login & Registration Design
1. **Pattern Matching**: Inspected `contact.html` to replicate its 2-column layout (hero image banner at the top, split heading & form at the bottom).
2. **View Development**: Built `register.html` and `login.html` reusing existing styles and brand colors (`#97262A`).
3. **Form Logic**: Added `@app.route('/register')` and `@app.route('/login')` with `GET` and `POST` method support.
4. **Navigation Expansion**: Added `Login` and `Register` links to `ul.navig` across all templates.

### Phase 3: Task 3 — Data Processing & Home Page Integration
1. **Storage Setup**: Created `data/users.json` for lightweight, file-based data storage.
2. **Validation Logic**: Verified required fields, confirmed password matching, and performed duplicate email verification.
3. **Post-Redirect-Get (PRG) Pattern**: Upon valid registration, user data is saved to `data/users.json`, a success message is flashed, and the client is redirected to `/` via `redirect(url_for('home'))`.
4. **Home Page Rendering**: Updated `home()` to read `data/users.json` and pass `users` to `index.html`. Added a responsive "REGISTERED USER DETAILS" card section.

### Phase 4: Task 4 — Email Notification System (Login Authentication)
1. **Environment Configuration**: Created `.env.example` defining standard SMTP configuration keys (`SMTP_SERVER`, `SMTP_PORT`, `SMTP_USE_TLS`, `SMTP_USERNAME`, `SMTP_PASSWORD`, `SMTP_SENDER`). Added `.env` to `.gitignore` to prevent credential exposure.
2. **Email Engine**: Created `send_email_notification()`, `send_login_success_email()`, and `send_login_failed_email()` supporting TLS authentication, custom subjects, and branded HTML templates.
3. **Authentication & Dispatch in `/login`**:
   - For valid credentials: user is authenticated, "Login Successful" email is sent to their registered address, and a success message is displayed.
   - For invalid credentials (wrong password or unregistered email): "Login Failed" security alert is sent to the entered email address, and an error message is displayed on the login page.
4. **Safe Fallback**: Enabled simulation logging when `.env` is unconfigured, preventing any server crash during offline evaluations.

---

## 🌟 Project Functionality

Currently, users can:
- **Browse All Pages**: Navigate seamlessly across Home, About, Blog, Pages, Gallery, and Contact without 404 errors or page reloads.
- **Experience Rich Media**: View sliding hero banners (FlexSlider) on Home and interactive lightbox popups (Chocolat) on Gallery.
- **Register an Account**:
  - Enter Full Name, Email, Phone Number, Password, and Confirm Password on `/register`.
  - Receive instant validation feedback if fields are blank, passwords mismatch, or email already exists.
  - Automatically redirect to Home upon successful registration.
- **View Registered Profiles on Home**:
  - The Home page displays verified client cards with user initials, Name, Email, and Phone number.
- **Log In with Email Notifications (Task 4)**:
  - Enter credentials on `/login`.
  - **Valid Credentials**: Authenticated successfully, green confirmation banner displayed on site, and "Login Successful" notification dispatched to registered email.
  - **Invalid Credentials**: Red error alert displayed on site, and "Security Alert: Unsuccessful Login Attempt" dispatched to entered email address.

---

## 📧 Email Notification System (Task 4)

### 1. Valid Login Flow
```text
[ User enters registered Email & correct Password ]
                     │
                     ▼
             [ POST /login ]
                     │
         User matched in users.json?
                     │  (YES)
                     ▼
     [ Authenticate User Session ]
                     │
                     ├──► [ Dispatch "Login Successful" Email ]
                     │    Recipient: user["email"] (Registered email)
                     │    Subject: "Majestic Interior — Login Successful"
                     │    Content: User Name, Account Email, Timestamp, Security notice
                     │
                     ▼
     [ Flash Green Success Alert on Website ]
     "Login successful! Welcome back, {Name}. A login confirmation email has been sent to {Email}."
```

### 2. Invalid Login Flow
```text
[ User enters unregistered Email OR wrong Password ]
                     │
                     ▼
             [ POST /login ]
                     │
         Credentials match in users.json?
                     │  (NO)
                     ▼
     [ Reject Authentication ]
                     │
                     ├──► [ Dispatch "Login Failed" Security Alert Email ]
                     │    Recipient: email (Address entered in login form)
                     │    Subject: "Security Alert: Unsuccessful Login Attempt — Majestic Interior"
                     │    Content: Target Email, Timestamp, Invalid Credentials notice
                     │
                     ▼
     [ Flash Red Error Alert on Login Page ]
     "Invalid email or password. An alert email has been sent to the entered address."
```

### 3. SMTP Configuration via `.env`
Email dispatch is powered by SMTP (Simple Mail Transfer Protocol) using environment variables loaded securely via `python-dotenv`:

| Environment Variable | Default Value | Description |
| :--- | :--- | :--- |
| `SMTP_SERVER` | `smtp.gmail.com` | SMTP host server address |
| `SMTP_PORT` | `587` | SMTP port (587 for TLS) |
| `SMTP_USE_TLS` | `True` | Enables STARTTLS encryption |
| `SMTP_USERNAME` | *(Your Gmail)* | Registered sender email address |
| `SMTP_PASSWORD` | *(16-char App Password)* | Google 16-character App Password |
| `SMTP_SENDER` | `Majestic Interior <...>` | Display name and sender address |

> **Setting up Gmail SMTP App Password**:
> 1. Visit your [Google Account Security](https://myaccount.google.com/security) settings.
> 2. Ensure **2-Step Verification** is turned ON.
> 3. Search for **App passwords** or visit [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords).
> 4. Create an App password (e.g. name: `Majestic Flask PBL`) and copy the generated 16-character code into `.env`.

---

## 📁 Project Structure

```text
majestic-web/
│
├── app.py                     # Main Flask application and route definitions
├── requirements.txt           # Python dependencies (Flask>=3.0.0, python-dotenv>=1.0.0)
├── .env.example               # Template for environment variables and SMTP setup
├── .gitignore                 # Excludes .env, virtual environments, and caches
│
├── data/
│   └── users.json             # JSON file storing registered user records
│
├── templates/                 # Jinja2 HTML templates
│   ├── index.html             # Home page (with Registered User Details section)
│   ├── about.html             # About Us page
│   ├── blog.html              # Blog articles page
│   ├── contact.html           # Contact Us & Google Maps page
│   ├── gallery.html           # Gallery page with Chocolat lightbox
│   ├── pages.html             # Typography, buttons & table components
│   ├── single.html            # Single post & comments page
│   ├── login.html             # User login page (Task 2 & Task 4)
│   └── register.html          # User registration page (Task 2 & 3)
│
├── static/                    # Frontend static assets
│   ├── css/
│   │   ├── bootstrap.css      # Bootstrap framework styles
│   │   ├── style.css          # Majestic primary stylesheet
│   │   ├── chocolat.css       # Lightbox stylesheet
│   │   ├── flexslider.css     # Banner slider stylesheet
│   │   ├── style4.css         # Team hover animations
│   │   └── common.css         # Shared CSS utilities
│   ├── js/
│   │   ├── jquery-1.11.0.min.js
│   │   ├── easing.js
│   │   ├── move-top.js
│   │   ├── jquery.flexslider.js
│   │   ├── jquery.chocolat.js
│   │   └── modernizr.custom.79639.js
│   ├── fonts/                 # Glyphicons icon fonts
│   └── images/                # Furniture & layout images (54 assets)
│
├── scratch/
│   └── test_task4.py          # Automated test suite for Task 4 login & email flows
│
└── web/                       # Original untouched static backup template
```

---

## ⚙️ Technologies Used

- **Backend**: Python 3.13, Flask 3.1
- **Email & Networking**: `smtplib`, `email.mime` (standard library), `python-dotenv 1.2+`
- **Templating Engine**: Jinja2
- **Data Persistence**: JSON (`data/users.json`)
- **Frontend Core**: HTML5, CSS3, JavaScript (ES5/ES6)
- **UI Framework & Libraries**: Bootstrap 3, jQuery 1.11.0
- **Plugins**: FlexSlider, Chocolat Lightbox, Move-Top Scroll

---

## 🚀 Installation & Run Steps

### 1. Prerequisites
- Python 3.10+ installed on your machine.
- Git (optional, for cloning).

### 2. Setup Environment
Open your terminal in the project directory:

```powershell
# Create a local virtual environment
python -m venv .venv

# Activate the virtual environment
# Windows (PowerShell):
.venv\Scripts\Activate.ps1
# Windows (CMD):
.venv\Scripts\activate.bat
# Linux / macOS:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Environment Variables (Optional for Live SMTP)
Copy `.env.example` to `.env`:
```powershell
copy .env.example .env
```
Open `.env` and set your Gmail address and 16-character App Password. If left unconfigured, the application gracefully operates in **simulation mode**, printing notifications to the console without interrupting user flow.

### 4. Run Application
```powershell
python app.py
```

Open your browser and navigate to:
```text
http://127.0.0.1:5000/
```

---

## 🌐 Flask Routes Inventory

| HTTP Route | Methods | View Function | Description |
| :--- | :---: | :--- | :--- |
| `/` | `GET` | `home()` | Home page with hero slider, welcome section, and registered user cards. |
| `/about` | `GET` | `about()` | Company history, capabilities, and advantages. |
| `/blog` | `GET` | `blog()` | Interior design blog posts and categories. |
| `/contact` | `GET` | `contact()` | Google map embed and general contact form. |
| `/gallery` | `GET` | `gallery()` | Portfolio gallery with interactive popup lightbox. |
| `/pages` | `GET` | `pages()` | UI typography, heading styles, and button components. |
| `/single` | `GET` | `single()` | Detailed blog post view with user discussion comments. |
| `/register` | `GET`, `POST` | `register()` | User registration form, validation, JSON storage, and welcome email dispatch. |
| `/login` | `GET`, `POST` | `login()` | User authentication, credential validation, login email dispatch, and redirect to Home. |
| `/logout` | `GET` | `logout()` | Session destruction, logging user out, and redirect to Home. |


---

## 🔄 Registration Data Flow (Task 3)

```text
[ User on /register ]
        │
        │ Submits Form (Name, Email, Phone, Password, Confirm Password)
        ▼
[ POST /register ]
        │
        ├── Validation Check:
        │   ├── Are any fields empty? ───────────────► [ Flash Error ] ──┐
        │   ├── Do passwords mismatch? ──────────────► [ Flash Error ] ──┼──► Return to /register
        │   └── Does email already exist in JSON? ───► [ Flash Error ] ──┘
        │
        ├── All Valid:
        │   ├── Load existing records from data/users.json
        │   ├── Append new user dictionary
        │   ├── Save updated list to data/users.json
        │   ├── Flash success message
        │   └── HTTP 302 Redirect to / (Home)
        ▼
[ GET / (Home) ]
        │
        ├── home() reads data/users.json
        ├── Passes users list to index.html
        └── Home page renders "REGISTERED USER DETAILS" client cards
```

---

## 🔒 Security Considerations

1. **Environment Secret Isolation**: All SMTP passwords, sender emails, and Flask secret keys are stored strictly in `.env`. No secrets are hardcoded in source code.
2. **Git Exclusion**: `.env` is registered in `.gitignore` to prevent credential leakage to remote repositories.
3. **Password Masking**: Password fields use `<input type="password">` to prevent on-screen shoulder surfing.
4. **Credential Privacy**: Passwords stored in `users.json` are **never** rendered in frontend templates or exposed on the Home page.
5. **Secure Email Transport**: SMTP connections use STARTTLS on port 587, encrypting email communications over the network.
6. **Account Takeover Protection**: Immediate security alert emails on failed login attempts notify users if unauthorized parties attempt to guess their credentials.
7. **Graceful Fault Tolerance**: SMTP errors (network timeouts, bad credentials) are caught and logged without causing HTTP 500 crashes on the website.

---

## 🧪 Testing

### Automated Test Suite Execution
Run the unit test suite verifying both valid and invalid login email notifications as well as Task 1–3 non-breaking regression:
```powershell
python scratch/test_task4.py
```

### Manual Testing Guide

#### Case 1: Valid Login (Success Email Flow)
1. Open `http://127.0.0.1:5000/login`.
2. Enter valid credentials (e.g., registered user in `data/users.json`):
   - **Email**: `piyush@example.com`
   - **Password**: `Test123`
3. Click **LOGIN**.
4. **Verification**:
   - Website displays green success banner: *"Login successful! Welcome back, Piyush Test. A login confirmation email has been sent to piyush@example.com."*
   - If SMTP is configured in `.env`, a confirmation email is delivered to the inbox.
   - If `.env` is unconfigured, terminal outputs `[SMTP Simulation] Email simulated for 'piyush@example.com' | Subject: 'Majestic Interior — Login Successful'`.

#### Case 2: Invalid Login (Security Alert Email Flow)
1. Open `http://127.0.0.1:5000/login`.
2. Enter incorrect credentials:
   - **Email**: `piyush@example.com`
   - **Password**: `WrongPassword123`
3. Click **LOGIN**.
4. **Verification**:
   - Website displays red error banner: *"Invalid email or password. An alert email has been sent to the entered address."*
   - If SMTP is configured in `.env`, an alert email is delivered to `piyush@example.com` with subject *"Security Alert: Unsuccessful Login Attempt — Majestic Interior"*.
   - If `.env` is unconfigured, terminal outputs `[SMTP Simulation] Email simulated for 'piyush@example.com' | Subject: 'Security Alert: Unsuccessful Login Attempt — Majestic Interior'`.

---

## 🎓 Viva Explanation Guide (B.Tech PBL)

When asked during your evaluation:

- **Q1: Why did we convert a static template into Flask?**
  > *"Static templates only serve fixed HTML files. Flask allows us to dynamically render pages, manage URL routing centrally, handle form submissions via POST requests, validate user inputs, and persist data across requests."*

- **Q2: What is the Post-Redirect-Get (PRG) pattern in Task 3?**
  > *"After processing a successful POST request in `/register`, we issue an HTTP redirect (`return redirect(url_for('home'))`). This prevents accidental duplicate form submissions if the user refreshes their browser."*

- **Q3: How is registration data stored?**
  > *"For Task 3, we use a structured JSON file (`data/users.json`). Python's native `json` module reads and writes client dictionaries, making the data human-readable, self-contained, and simple to demonstrate without requiring an external database server."*

- **Q4: How does the SMTP email notification system in Task 4 work?**
  > *"We use Python's built-in `smtplib` library together with `email.mime`. When a user submits the login form, the backend checks credentials against `data/users.json`. If valid, it dispatches a 'Login Successful' notification to the registered user. If invalid, it dispatches a 'Security Alert' to the entered email address so the account owner is notified of potential unauthorized attempts."*

- **Q5: Why do we use environment variables (`.env`) for SMTP?**
  > *"Hardcoding email addresses and passwords into source code is a major security vulnerability. By storing credentials in a `.env` file that is excluded via `.gitignore`, sensitive credentials are never leaked to public version control."*

- **Q6: Why is STARTTLS on port 587 preferred for email sending?**
  > *"Port 587 with STARTTLS starts with a plaintext handshake and immediately upgrades the connection to encrypted TLS before any sensitive credentials (such as App Passwords) or email contents are transmitted."*

- **Q7: What happens if the SMTP server fails or credentials are wrong?**
  > *"All SMTP communication is wrapped inside a `try...except` block with logging. If credentials are missing, simulation mode logs the attempt to terminal. If connection fails, a warning is logged without raising an unhandled HTTP 500 error, guaranteeing that website visitors receive appropriate feedback."*
