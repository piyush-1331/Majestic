# Majestic Interior & Furniture — Flask Web Application

A full-featured interior design and furniture e-commerce website built by integrating the Majestic HTML5/CSS3 template into a Python Flask backend. Developed as part of the **Project-Based Learning (PBL) Python Frameworks** curriculum for B.Tech Semester 5.

---

## 📌 Project Status & PBL Task Roadmap

| Task | Title | Description | Status |
| :---: | :--- | :--- | :---: |
| **Task 1** | **Website Integration Using Flask** | Converting static HTML/CSS/JS template into a structured Flask web app with dynamic routing. | ✅ **Completed** |
| **Task 2** | **User Login & Registration Pages** | Designing separate Login and Registration pages styled after `contact.html` with server-side validation. | ✅ **Completed** |
| **Task 3** | **Registration Processing & Home Display** | Processing registration POST data, storing in JSON, and rendering registered user cards on Home. | ✅ **Completed** |
| **Task 4** | **Email Notifications** | Automated welcome & alert emails via SMTP. | ⏳ *Not Implemented Yet* |
| **Task 5** | **Payment Gateway Integration** | Checkout and payment processing. | ⏳ *Not Implemented Yet* |

---

## 📖 Project Overview

The Majestic project transforms an elegant, multi-page static website template into a dynamic Python Flask web application. It retains all original design aesthetics—including typography (Titillium Web, Lato), responsive Bootstrap grids, FlexSlider banners, Chocolat lightbox galleries, and custom animations—while powering page delivery and client authentication flows through Python.

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

---

## 🛠️ Implementation Approach

The transition from a static website to an integrated Flask application was performed in three systematic phases:

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
- **Log In**:
  - Sign in via `/login` with validation and success messages.
  - Switch between Login and Registration via direct links.

---

## 📁 Project Structure

```text
majestic-web/
│
├── app.py                     # Main Flask application and route definitions
├── requirements.txt           # Python dependencies (Flask>=3.0.0)
├── .gitignore                 # Excludes virtual environments and caches
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
│   ├── login.html             # User login page (Task 2)
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
└── web/                       # Original untouched static backup template
```

---

## ⚙️ Technologies Used

- **Backend**: Python 3.13, Flask 3.1
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

### 3. Run Application
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
| `/register` | `GET`, `POST` | `register()` | User registration form, validation, and JSON storage. |
| `/login` | `GET`, `POST` | `login()` | User authentication and sign-in page. |

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

## 🔒 Basic Security Considerations

1. **Password Masking**: All password input fields use `<input type="password">` to prevent visual snooping.
2. **Password Protection in UI**: Passwords are **never** rendered in templates or exposed on the Home page (`{{ user.password }}` is omitted entirely).
3. **Server-Side Validation**: All inputs are checked on the server in Python to prevent bypassed client-side constraints.
4. **Duplicate Account Prevention**: Email addresses are checked case-insensitively before storing, preventing account collisions.
5. **Secret Key Usage**: Flask session cookies are protected with a server secret key to support secure flash messaging.

---

## 🧪 Testing

### Test Suite Execution
Run the automated test scripts to verify the functionality:
```powershell
python -m unittest scratch/test_task3.py
```

### Manual Viva Demonstration Checklist
1. **Task 1 Verification**: Click through all top navigation links (`Home`, `About`, `Blog`, `Pages`, `Gallery`, `Contact`). Confirm all pages load with CSS and images intact.
2. **Task 2 Empty Form Check**: Navigate to `/register`, click **REGISTER** without entering data. Confirm *"Full Name is required."* appears.
3. **Task 2 Password Mismatch Check**: Fill in details with differing passwords. Confirm *"Password and Confirm Password do not match."* appears.
4. **Task 3 Registration Check**:
   - Register a new client:
     - **Name**: `Alex Johnson`
     - **Email**: `alex@example.com`
     - **Phone**: `9876543210`
     - **Password**: `SecurePass123`
     - **Confirm Password**: `SecurePass123`
   - Click **REGISTER**.
   - Verify immediate redirect to Home (`/`).
   - Confirm green success message appears.
   - Scroll down to the **REGISTERED USER DETAILS** section: confirm `Alex Johnson`, `alex@example.com`, and `9876543210` are displayed.
   - Inspect page source: verify password `SecurePass123` is **not** present in the HTML.
5. **Duplicate Email Check**: Go back to `/register` and enter `alex@example.com` again. Confirm *"Email already registered."* prevents duplicate insertion.

---

## 🎓 Viva Explanation Guide (B.Tech PBL)

When asked during your evaluation:

- **Q1: Why did we convert a static template into Flask?**
  > *"Static templates only serve fixed HTML files. Flask allows us to dynamically render pages, manage URL routing centrally, handle form submissions via POST requests, validate user inputs, and persist data across requests."*

- **Q2: What is the Post-Redirect-Get (PRG) pattern in Task 3?**
  > *"After processing a successful POST request in `/register`, we issue an HTTP redirect (`return redirect(url_for('home'))`). This prevents accidental duplicate form submissions if the user refreshes their browser."*

- **Q3: How is registration data stored?**
  > *"For Task 3, we use a structured JSON file (`data/users.json`). Python's native `json` module reads and writes client dictionaries, making the data human-readable, self-contained, and simple to demonstrate without requiring an external database server."*

- **Q4: How do static files work in Flask?**
  > *"Flask serves static assets from the `static/` directory using `{{ url_for('static', filename='...') }}`. This ensures correct URL generation regardless of sub-paths or deployment environments."*

- **Q5: How is user privacy handled on the Home page?**
  > *"Although the password is saved in `users.json`, the Jinja template in `index.html` explicitly extracts only `user.name`, `user.email`, and `user.phone`, ensuring sensitive credentials are never displayed in the frontend."*
