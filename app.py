import os
from flask import Flask, render_template, request, redirect, url_for, flash # Added flash for messages
from dotenv import load_dotenv
from scanner.scanner import perform_scan # Import the scanning function
import datetime # To pass current year to template

load_dotenv() # Load environment variables from .env file

app = Flask(__name__)
# Secret key is needed for session management and flash messages (important for auth later)
# Use a strong, random secret key in production, stored in environment variables
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'a_default_development_secret_key')

@app.context_processor
def inject_now():
    """Inject current year into templates."""
    return {'now': datetime.datetime.utcnow()}

@app.route('/', methods=['GET', 'POST'])
def index():
    results = None
    error_message = None
    target_url = None # To keep the URL in the input box after submission

    if request.method == 'POST':
        target_url = request.form.get('url', '').strip()
        if not target_url:
            error_message = "URL cannot be empty."
            # Using flash for better message handling:
            # flash("URL cannot be empty.", "error")
            # return redirect(url_for('index')) # Redirect prevents form resubmission
        else:
            # Basic validation (scanner does more thorough validation)
            if not (target_url.startswith('http://') or target_url.startswith('https://')):
                 error_message = "Invalid URL format. Please include http:// or https://"
                 # flash("Invalid URL format. Please include http:// or https://", "error")
                 # return redirect(url_for('index'))
            else:
                print(f"Scanning URL: {target_url}") # Log the scan attempt
                # Run the scan
                # **IMPORTANT SECURITY NOTE:** In a real-world app, you MUST add rate limiting,
                # input sanitization, and potentially queueing for scans to prevent abuse.
                # Never run scans directly from web requests without controls in production.
                results = perform_scan(target_url)
                print(f"Scan results: {results}") # Log results

                # Check if scan itself resulted in an error to display
                if results and results.get('scan_status') == 'error':
                    error_message = f"Scan Error: {results.get('error', 'Unknown error during scan.')}"
                    # Reset results so only the error message shows clearly
                    results = None


    # Retrieve flashed messages (if using flash)
    # messages = get_flashed_messages(with_categories=True)

    return render_template('index.html',
                           results=results,
                           error_message=error_message,
                           target_url=target_url)
                           # messages=messages # Pass flashed messages if using flash

# --- Placeholder Routes for Phase 2 ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Logic for Firebase login will go here in Phase 2
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    # Logic for Firebase registration will go here in Phase 2
    return render_template('register.html')

@app.route('/logout')
def logout():
    # Logic for Firebase logout
    return redirect(url_for('index'))

@app.route('/history')
# @login_required # Decorator needed after implementing authentication
def history():
    # Logic to fetch scan history from Firebase DB for the logged-in user (Phase 2)
    scans = [] # Placeholder
    return render_template('history.html', scans=scans)
# --- End Placeholder Routes ---


if __name__ == '__main__':
    # Use debug=True only for development
    # Use host='0.0.0.0' to make it accessible on your network (use with caution)
    app.run(debug=True, host='127.0.0.1', port=5000)