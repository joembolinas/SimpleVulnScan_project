# SimpleVulnScan - Basic Web Vulnerability Scanner

A Flask-based web application designed to perform basic security scans on web URLs. This project serves as an educational tool to understand common web vulnerabilities and security checks.

**Disclaimer:** This tool is for educational purposes only. Unauthorized scanning of websites is illegal and unethical. Always obtain explicit permission before scanning any target. Use responsibly.

## Table of Contents

* [Project Goal](#project-goal)
* [Design &amp; Technical Strategy](#design--technical-strategy)
* [Features (Phase 1)](#features-phase-1)
* [Technology Stack](#technology-stack)
* [Setup and Installation](#setup-and-installation)
* [Running the Application](#running-the-application)
* [Project Documentation (STAR Method Example)](#project-documentation-star-method-example)
* [Critical Thinking &amp; Design Choices](#critical-thinking--design-choices)
* [Challenges &amp; Solutions](#challenges--solutions)
* [Learnings &amp; Future Enhancements](#learnings--future-enhancements)
* [AI Tool Usage (Example)](#ai-tool-usage-example)
* [Highlighting Key Skills](#highlighting-key-skills)
* [Other Significant Projects](#other-significant-projects)
* [Contact](#contact)

## Project Goal

The initial goal was to create a simple, web-based tool to automate basic security checks for a given URL, focusing initially on passive reconnaissance like checking security headers and common informational files.

## Design & Technical Strategy

* **Framework:** Flask was chosen for its simplicity, flexibility, and suitability for smaller web applications. Its microframework nature allows for easy extension.
* **Structure:** A modular structure was adopted, separating the core scanning logic (`scanner/` module) from the web interface (`app.py`, `templates/`, `static/`). This promotes maintainability and scalability.
* **Scanning Logic:** The `requests` library is used for making HTTP requests. Initial checks focus on response headers and the existence of `robots.txt` and `sitemap.xml`.
* **Frontend:** Basic HTML, CSS, and JavaScript are used for the user interface, leveraging Flask's Jinja2 templating engine.

## Features (Phase 1)

* Input field for target URL.
* Basic URL validation (presence of `http://` or `https://`).
* Checks for common HTTP security headers:
  * `X-Frame-Options`
  * `Strict-Transport-Security`
  * `Content-Security-Policy`
  * `X-Content-Type-Options`
* Checks for server information leakage via the `Server` header.
* Checks for the existence of `robots.txt`.
* Checks for the existence of `sitemap.xml`.
* Display of scan results, indicating pass/fail/info status and recommendations.

*(Future phases aim to add user authentication, scan history, and more advanced vulnerability checks like basic XSS and IDOR detection.)*

## Technology Stack

* **Backend:** Python 3, Flask
* **Libraries:** `requests`, `python-dotenv`
* **Frontend:** HTML, CSS, JavaScript (minimal), Jinja2
* **Environment:** Virtual Environment (`venv`)

## Setup and Installation

1. **Clone the repository (or download the source code):**

   ```bash
   git clone <your-repository-url> # Replace with actual URL if hosted
   cd SimpleVulnScan
   ```
2. **Create and activate a virtual environment:**

   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```
3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```
4. **(Optional but Recommended) Create a `.env` file:**
   In the project root, create a file named `.env` and add a secret key for Flask session management (important for future authentication):

   ```env
   FLASK_SECRET_KEY='your_very_strong_random_secret_key_here'
   ```

   Replace the placeholder with a secure, random string.

## Running the Application

1. Ensure your virtual environment is activated and dependencies are installed.
2. Run the Flask development server:
   ```bash
   python app.py
   ```
3. Open your web browser and navigate to `http://127.0.0.1:5000/`.

## Project Documentation

* **Situation:** Needed a way to quickly check basic security configurations (like missing security headers) for web applications without manually using browser developer tools or complex command-line utilities for every check.
* **Task:** Develop a simple web application that accepts a URL and performs automated checks for common security headers and informational files (`robots.txt`, `sitemap.xml`).
* **Action:**
  * Chose Flask as the web framework due to prior experience and its lightweight nature.
  * Designed a modular structure separating scanning logic (`scanner.py`) from the web routes (`app.py`).
  * Implemented functions within `scanner.py` using the `requests` library to fetch the target URL, analyze response headers, and check for specific files.
  * Created Jinja2 templates (`base.html`, `index.html`) to build the user interface for URL input and results display.
  * Used basic CSS for styling the results, differentiating between findings needing attention (fail) and informational/passing checks.
  * Added basic input validation in the Flask route to ensure a valid-looking URL format was submitted.
* **Result:** Successfully created a functional Phase 1 scanner capable of identifying missing security headers, server information disclosure, and the presence of `robots.txt`/`sitemap.xml`. The web interface provides clear feedback and recommendations, reducing the time needed for these initial checks compared to manual methods. (Quantify further if possible, e.g., "Reduced check time by X%").

## Critical Thinking & Design Choices

* **Flask vs. Django:** Chose Flask for its minimalism, suitable for this project's initial scope. Django felt like overkill for a simple scanning tool.
* **Modular Scanner:** Separating `scanner.py` allows for easier testing of the scanning logic independently of the web framework and facilitates adding new scan types later without cluttering `app.py`.
* **Synchronous Scans (Phase 1):** Initial scans are performed synchronously within the web request. *Trade-off:* This is simple but won't scale well for longer scans or many users. *Future:* Asynchronous task queues (like Celery or RQ) would be necessary for more intensive scans or a production environment to avoid blocking web requests.
* **Basic Header Checks:** Focused on presence and common 'good' values (e.g., `X-Frame-Options: DENY`). *Trade-off:* Doesn't parse complex directives (like CSP). *Future:* More robust parsing could be added.
* **Error Handling:** Included `try...except` blocks in `scanner.py` to handle network errors (timeouts, connection issues) and provide informative error messages to the user via the web interface.

## Challenges & Solutions

* **Challenge:** Handling various network errors gracefully (timeouts, DNS resolution failures, non-200 status codes).
* **Solution:** Implemented specific `try...except` blocks for `requests.exceptions.Timeout` and general `requests.exceptions.RequestException`. Used `response.raise_for_status()` to catch HTTP error codes and reported errors clearly back to the user interface.
* **Challenge:** Ensuring consistent display of results and recommendations.
* **Solution:** Standardized the dictionary structure returned by each check function in `scanner.py`. Used Jinja2 conditional logic (`{% if %}`) and CSS classes (`finding-pass`, `finding-fail`) in the template to render results appropriately based on the returned data.

## Learnings & Future Enhancements

* **Learnings:** Reinforced understanding of Flask routing, Jinja2 templating, and handling external HTTP requests with `requests`. Gained practical experience in structuring a small web application.
* **Future Enhancements:**
  * Phase 2: User Authentication (Firebase), Scan History (Firebase DB).
  * Phase 3: Implement basic XSS and IDOR checks (with strong caveats about their limitations). Add more scan types (e.g., cookie attributes, directory listing checks).
  * Phase 4: Refactor for asynchronous scanning, improve UI/UX, add comprehensive logging, package for easier deployment.
  * Consider using a dedicated HTML parsing library (like BeautifulSoup) for more advanced checks involving page content.

## AI Tool Usage

* **Situation:** Needed boilerplate code for Flask routes and basic HTML templates. Also sought suggestions for common security header checks.
* **Task:** Generate initial Flask application structure, basic Jinja2 templates, and functions for checking specific HTTP headers.
* **Action:**
  * Used GitHub Copilot to generate the initial `app.py` structure with a basic index route.
  * Prompted Copilot for examples of checking `X-Frame-Options` and `Strict-Transport-Security` headers using the `requests` library response object. Example prompt: `"python function using requests library to check if X-Frame-Options header is present and set to DENY or SAMEORIGIN"`
  * Used Copilot to suggest basic HTML structure for `base.html` and `index.html`.
* **Result & Evaluation:** AI provided useful starting points for the Flask app and header checks. **However, critical evaluation was necessary:**
  * The initial Flask structure was standard but required modification to add context processors (like `inject_now`) and specific error handling.
  * AI-suggested header checks needed refinement to handle case-insensitivity (using `.lower()`) and provide clearer pass/fail logic and recommendations.
  * Generated HTML required significant adjustments to integrate with Jinja2 templating (`{{ url_for(...) }}`, `{% block %}`, etc.) and specific CSS classes for results display.
  * The AI's role was primarily code generation and suggestion; the architectural decisions, integration, refinement, error handling logic, and specific result formatting were driven by manual development and critical review.

## Highlighting Key Skills

* **Adaptability:** This project involved learning/applying Flask fundamentals, integrating external libraries (`requests`), and planning for future scalability (authentication, async tasks). *(Expand as you learn more)*.
* **Critical Thinking:** Demonstrated through technology choices (Flask), application structure (modularity), and the planned approach to handling scan complexity (synchronous vs. asynchronous). *(See [Critical Thinking &amp; Design Choices](#critical-thinking--design-choices) section)*.
* **Communication:** This README aims for clear, concise documentation of the project's goals, implementation, and usage. *(Consider adding screenshots or a GIF/video demo later)*.

## Other Significant Projects

* **Project 1:**
* **Project 2:**
* ...
