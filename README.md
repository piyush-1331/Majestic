# Majestic Interior & Furniture — Flask Web Application

A full-featured interior design and furniture e-commerce website built by integrating the Majestic HTML5/CSS3 template into a Python Flask backend. Developed as part of the **Project-Based Learning (PBL) Python Frameworks** curriculum for B.Tech Semester 5.

---

## 📌 Project Status & PBL Task Roadmap

| Task | Title | Description | Status |
| :---: | :--- | :--- | :---: |
| **Task 1** | **Website Integration Using Flask** | Converting static HTML/CSS/JS template into a structured Flask web app with dynamic routing. | ✅ **Completed** |
| **Task 2** | **User Login & Registration Pages** | Designing separate Login and Registration pages styled after `contact.html` with server-side validation. | ✅ **Completed** |
| **Task 3** | **Registration Processing & Home Display** | Processing registration POST data, storing in JSON, and rendering registered user cards on Home. | ✅ **Completed** |
| **Task 4** | **Email Notifications** | Automated login confirmation, security alerts & registration emails via SMTP with `.env` configuration. | ✅ **Completed** |
| **Task 5** | **Payment Gateway Integration** | Demonstrating secure Razorpay Test Mode checkout, backend order creation, and server-side signature verification. | ✅ **Completed** |

---

## 📖 Project Overview

The Majestic project transforms an elegant, multi-page static website template into a dynamic Python Flask web application. It retains all original design aesthetics—including typography (Titillium Web, Lato), responsive Bootstrap grids, FlexSlider banners, Chocolat lightbox galleries, and custom animations—while powering page delivery, client authentication flows, automated email security notifications, and full-stack Razorpay payment processing in Test Mode.

---

## 💻 Coding Efforts

The primary development effort spans several architectural layers:

1. **Backend Routing & Control (`app.py`)**:
   - Structured entry point utilizing Flask with canonical route decorators.
   - Session-based feedback using `flask.flash()` and secret key configuration.
   - RESTful request handling supporting `GET` for page rendering and `POST` for form submissions.
2. **Dynamic Templating (Jinja2)**:
   - Asset linking transformed from hard-coded relative paths to `{{ url_for('static', filename='...') }}` across all 10 pages.
   - Internal navigation links rewritten to dynamic route endpoints using `{{ url_for(...) }}`.
   - Conditional rendering blocks (`{% if users %}`, `{% if current_user %}`, and `{% with messages = get_flashed_messages() %}`).
3. **Forms & Client Input Handling**:
   - Developed registration, login, and payment checkout forms with appropriate HTML5 input types (`text`, `email`, `tel`, `password`, `number`).
   - Maintained visual harmony with the Majestic contact form layout.
4. **Data Persistence**:
   - Implemented JSON storage helper functions (`load_users()`, `save_users()`) to persist registered client records in `data/users.json`.
5. **Form Validation**:
   - Added robust server-side validation preventing blank fields, password mismatches, duplicate email entries, and non-numeric or negative transaction amounts.
6. **SMTP Email Notification System (`smtplib`, `email.mime`)**:
   - Integrated automated email dispatch using Python's built-in `smtplib` and `email.mime` libraries with TLS support.
   - Designed dual-format (HTML and plain-text fallback) emails branded with Majestic theme styling (`#97262A`).
   - Implemented secure credential management via environment variables (`.env`) loaded by `python-dotenv`.
7. **Razorpay Payment Gateway Integration (`razorpay`, Test Mode)**:
   - Integrated Razorpay Python SDK using environment variables (`RAZORPAY_KEY_ID`, `RAZORPAY_KEY_SECRET`).
   - Implemented server-side amount validation, conversion to smallest currency unit (paise), and official Razorpay Test Order generation.
   - Seamless frontend Razorpay Checkout modal launch with branded theme styling.
   - Strict server-side cryptographic signature verification (`client.utility.verify_payment_signature`) preventing client-side forgery.
   - Comprehensive handling of successful payments, cancellations, and backend errors.

---

## 🛠️ Implementation Approach

The transition from a static website to an integrated Flask application was performed in five systematic phases:

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

### Phase 4: Task 4 — Email Notification System (Login & Register Authentication)
1. **Environment Configuration**: Created `.env.example` defining standard SMTP configuration keys. Added `.env` to `.gitignore`.
2. **Email Engine**: Created `send_email_notification()`, `send_login_success_email()`, `send_login_failed_email()`, and `send_registration_success_email()`.
3. **Session & Navbar Enhancements**:
   - Successful login sets `session["user"]` and redirects to Home.
   - When logged in, "Login" and "Register" buttons disappear and are replaced by the user greeting and a **Logout** button.
   - Themed custom flash messages to match `#2a2017` header styling with 4.5s auto-fadeout.

### Phase 5: Task 5 — Razorpay Payment Gateway Demonstration (Test Mode)
1. **SDK Setup**: Installed `razorpay` and added to `requirements.txt`.
2. **Environment Variables**: Defined `RAZORPAY_KEY_ID` and `RAZORPAY_KEY_SECRET` in `.env` and `.env.example`.
3. **Payment Page**: Designed `templates/payment.html` with responsive layout, quick amount chips (₹100, ₹500, ₹1,500, ₹5,000), test mode banner, and status result cards.
4. **Order Creation & Validation**: Implemented server-side validation (rejecting empty, non-numeric, zero, negative, or <₹1 amounts) and created Razorpay Test Orders via `client.order.create()`.
5. **Checkout & Signature Verification**:
   - Razorpay Checkout modal launches with `order_id`, `amount`, and `key_id`.
   - On payment success, client response is sent via POST to `/payment/success` where HMAC-SHA256 signature is verified via `client.utility.verify_payment_signature()`.
   - On cancellation/failure, handles redirection to `/payment/failure`.

---

## 🌟 Project Functionality

Currently, users can:
- **Browse All Pages**: Navigate seamlessly across Home, About, Blog, Pages, Gallery, Contact, and Payment without 404 errors.
- **Experience Rich Media**: View sliding hero banners (FlexSlider) on Home and interactive lightbox popups (Chocolat) on Gallery.
- **Register an Account**:
  - Enter Name, Email, Phone, and Password on `/register`.
  - Receive instant validation feedback.
  - Receive automated "Registration Successful" welcome email.
  - Automatically logged in and redirected to Home.
- **Log In with Automated Email Notifications**:
  - Valid Credentials: "Login Successful" email dispatched to registered address, session established, redirected to Home.
  - Invalid Credentials: "Security Alert: Unsuccessful Login Attempt" dispatched to entered address, error shown on login page.
- **Dynamic Navigation Bar**:
  - Shows styled "Login" and "Register" pill buttons when logged out.
  - Shows user greeting badge (`Hi, [Name]`) and red **Logout** button when logged in.
- **Demonstrate Razorpay Payment Gateway (Task 5)**:
  - Visit `/payment` directly from the top navigation.
  - Clear test mode banner confirms sandbox mode (no real money debited).
  - Select quick amount chips or enter a custom amount.
  - Server validates amount and creates a Razorpay Test Order.
  - Razorpay Checkout modal opens with test payment options (Cards, NetBanking, Wallet, UPI).
  - Cryptographic server-side signature verification displays verified payment receipts (Payment ID, Order ID, Amount, Timestamp).
  - Cancellation or failed payments display appropriate failure cards with a "Try Again" option.

---

## 💳 Razorpay Payment Gateway Integration (Task 5)

### 1. Payment Integration Flow
```text
User
 │
 ▼
Payment Page (/payment)
 │
 │ Submits Amount (e.g. ₹500)
 ▼
Flask Backend (POST /payment)
 │
 ├── Validates Amount (> 0, numeric, >= ₹1.00)
 ├── Converts to Paise (50000 paise)
 ├── Calls Razorpay API: client.order.create()
 └── Generates Razorpay order_id
 ▼
Razorpay Checkout (checkout.js on payment.html)
 │
 │ User enters Razorpay Test Card / UPI details
 ▼
Test Payment Processed by Sandbox
 │
 ├── User Cancels ──────────► [ GET /payment/failure ] ──► "Payment Cancelled"
 │
 └── Payment Successful
           │
           ▼ (razorpay_payment_id, razorpay_order_id, razorpay_signature)
      POST /payment/success
           │
           ▼
      Flask Backend Signature Verification
      client.utility.verify_payment_signature(params_dict)
           │
           ├── Signature Mismatch ──► "Verification Failed (Tampering Alert)"
           │
           └── Signature Valid ─────► "Payment Successful!"
                                      Displays: Payment ID, Order ID, Amount
```

### 2. Environment Variables Configuration
To run live test transactions with your Razorpay sandbox account, update `.env`:

```env
# Razorpay Payment Gateway Configuration (Task 5 - TEST MODE ONLY)
RAZORPAY_KEY_ID=your_test_key_id
RAZORPAY_KEY_SECRET=your_test_secret_key
```

> **Where to find Razorpay Test Keys**:
> 1. Log in to your [Razorpay Dashboard](https://dashboard.razorpay.com/).
> 2. Toggle to **Test Mode** at the top right of the dashboard.
> 3. Go to **Account & Settings** -> **API Keys**.
> 4. Generate a Test Key and copy the `Key ID` and `Key Secret` into `.env`.

---

## 📁 Project Structure

```text
majestic-web/
│
├── app.py                     # Main Flask application and route definitions
├── requirements.txt           # Python dependencies (Flask, python-dotenv, razorpay)
├── .env.example               # Template for environment variables (SMTP, Razorpay)
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
│   ├── login.html             # User login page (Task 2 & 4)
│   ├── register.html          # User registration page (Task 2, 3 & 4)
│   └── payment.html           # Razorpay Test Mode Payment Gateway page (Task 5)
│
├── static/                    # Frontend static assets
│   ├── css/
│   │   ├── bootstrap.css      # Bootstrap framework styles
│   │   ├── style.css          # Majestic primary stylesheet (includes Task 5 styles)
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
│   └── images/                # Furniture & layout images
│
└── scratch/                   # Automated unit test suites
    ├── test_task4.py          # Task 4 authentication & email test suite
    └── test_task5.py          # Task 5 Razorpay order, validation & signature test suite
```

---

## ⚙️ Technologies Used

- **Backend**: Python 3.13, Flask 3.1
- **Payment Processing**: `razorpay 2.0+` (Python SDK), Razorpay Checkout.js (Test Mode)
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

### 3. Configure Environment Variables
Copy `.env.example` to `.env`:
```powershell
copy .env.example .env
```
Open `.env` and fill in:
- `SMTP_USERNAME` & `SMTP_PASSWORD` (for Task 4 emails).
- `RAZORPAY_KEY_ID` & `RAZORPAY_KEY_SECRET` (for Task 5 payment gateway).

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
| `/register` | `GET`, `POST` | `register()` | User registration, JSON storage, and welcome email dispatch. |
| `/login` | `GET`, `POST` | `login()` | User authentication, email notification dispatch, and redirect to Home. |
| `/logout` | `GET` | `logout()` | Session termination and redirect to Home. |
| `/payment` | `GET`, `POST` | `payment()` | Payment page, amount validation, and Razorpay Test Order creation. |
| `/payment/success` | `POST` | `payment_success()` | Cryptographic HMAC signature verification and payment receipt display. |
| `/payment/failure` | `GET`, `POST` | `payment_failure()` | Payment cancellation and failure response handling. |

---

## 🔒 Security Considerations

1. **API Key & Secret Isolation**:
   - `RAZORPAY_KEY_ID` is safely exposed to frontend checkout.
   - `RAZORPAY_KEY_SECRET` is kept **strictly server-side** on Flask and never passed to HTML or JS templates.
2. **Environment Variable Storage**: All secrets (`SECRET_KEY`, SMTP passwords, Razorpay secrets) are isolated in `.env` and excluded via `.gitignore`.
3. **Cryptographic Signature Verification**:
   - Payment success is **never** trusted from frontend callbacks alone.
   - The backend computes and verifies `HMAC-SHA256(order_id + "|" + payment_id, key_secret)` using `client.utility.verify_payment_signature` before granting success status.
4. **Server-Side Amount Validation**:
   - The backend validates amount types and values, rejecting empty, zero, negative, or below ₹1.00 inputs.
5. **Sandbox Isolation**:
   - The system connects exclusively to Razorpay Sandbox/Test Mode. No real credit cards or bank accounts are touched.

---

## 🧪 Testing

### Automated Test Suite Execution
Run the unit test suites:
```powershell
# Run Task 5 Razorpay test suite (11 tests)
python scratch/test_task5.py

# Run Task 4 Email notification test suite (4 tests)
python scratch/test_task4.py
```

### Manual Testing Guide for Task 5

1. **Open Payment Page**:
   Navigate to: `http://127.0.0.1:5000/payment`
   - Confirm page loads with Majestic styling, "TEST MODE DEMO" banner, and quick amount chips.

2. **Test Validation Cases**:
   - **Empty Amount**: Leave input blank and submit. Verify: *"Please enter a payment amount."* appears.
   - **Zero Amount**: Enter `0` and submit. Verify: *"Payment amount must be greater than zero."* appears.
   - **Negative Amount**: Enter `-50` and submit. Verify: *"Payment amount must be greater than zero."* appears.
   - **Non-numeric Amount**: Enter `abc` and submit. Verify: *"Amount must be a valid numeric value."* appears.

3. **Test Successful Payment**:
   - Configure active Razorpay Test Keys in `.env`.
   - Enter `₹500` and click **PROCEED TO PAY NOW**.
   - Razorpay Checkout modal appears.
   - Select **Cards** and enter Razorpay official test card:
     - Card Number: `4000 0000 0000 0002` (or select NetBanking/UPI simulation).
     - Expiry: Any future date (e.g. `12/28`).
     - CVV: `123`.
   - Click **Pay** and approve the OTP simulation.
   - Page renders **Payment Successful!** with Payment ID, Order ID, Amount, and Verified Signature badge.

4. **Test Payment Cancellation**:
   - Enter `₹100` and click **PROCEED TO PAY NOW**.
   - In the Razorpay modal, click the **×** (Close) button or choose Cancel.
   - Page redirects to **Payment Failed / Cancelled** with order details and a "Try Again" button.

---

## 🎓 Viva Explanation Guide (B.Tech PBL)

When asked during your evaluation:

- **Q1: Why is an order created on the backend instead of directly in frontend JS?**
  > *"Creating the order on the backend prevents client-side price tampering. If the order was created in JavaScript, a malicious user could inspect the browser console, modify the amount to ₹1, and purchase a ₹50,000 furniture piece. The backend order binds the amount and currency securely before checkout begins."*

- **Q2: Why do we convert the amount to paise?**
  > *"Razorpay (and most payment gateways) handles amounts in the smallest currency unit to avoid floating-point rounding errors. For INR, ₹1 = 100 paise. So ₹500.50 becomes 50050 paise as an integer."*

- **Q3: What is Razorpay payment signature verification?**
  > *"When Razorpay processes a payment, it returns `razorpay_payment_id`, `razorpay_order_id`, and `razorpay_signature`. The signature is an HMAC-SHA256 hash created using our private `RAZORPAY_KEY_SECRET`. On the Flask backend, `client.utility.verify_payment_signature()` recalculates the hash. If the hashes match, we know the payment genuinely came from Razorpay and was not forged."*

- **Q4: Why must `RAZORPAY_KEY_SECRET` never be sent to the frontend?**
  > *"The Key ID acts as a public identifier for the checkout window, but the Key Secret has full administrative power to verify signatures, issue refunds, and access transactions. If exposed to the frontend, anyone could forge successful payment signatures."*

- **Q5: How does the application handle payment failures and cancellations?**
  > *"Razorpay Checkout's `modal.ondismiss` and `payment.failed` event listeners intercept user cancellations or banking declines and redirect to `/payment/failure`, displaying user-friendly feedback without crashing the application."*
