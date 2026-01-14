PERSONALIZED MOROCCAN INSIGHTS 2026
====================================

DESCRIPTION
-----------
A Python-based Streamlit web application that generates **personalized insights and messages** for Moroccan users in 2026. 
The app delivers culturally relevant, fun, and motivational readings in **Moroccan Darija (Arabic script)**.

This app is designed for **entertainment purposes only**, using legal-safe terminology like "reading" or "insight" rather than fortune-telling or astrology.

---

FEATURES
--------
- Interactive Streamlit web interface with **Moroccan-inspired design**:
  - Warm colors (red, orange, yellow, soft green)
  - Decorative fonts
  - Cards for each insight category
  - Mobile-first responsive design
- Free and Premium experiences:
  - Free: personality description + one general insight
  - Premium: full message with:
    - Golden advice
    - Challenge/Warning
    - Lucky number and lucky day
    - Fun surprises: mini quiz, joke, or motivational phrase
- Copy-to-clipboard and optional PDF download
- Deterministic output (same input → same result)
- Over 1.5 billion possible insight combinations
- Legal-safe disclaimer: "هاد المحتوى للترفيه فقط"

---

INSTALLATION
------------
Prerequisites:
- Python 3.7 or higher
- pip package manager

Setup:
1. Clone or download the repository
2. Create required files:
   - app.py
   - templates.json
   - requirements.txt
3. Install dependencies:
   pip install -r requirements.txt
4. Run application:
   streamlit run app.py
5. Open browser (or phone) at:
   http://localhost:8501

---

FILE STRUCTURE
--------------
moroccan-insights/
├── app.py            # Main Streamlit application
├── templates.json    # JSON with all text templates and insights
└── requirements.txt  # Python dependencies

---

USAGE
-----
1. Enter your full name (in Arabic)
2. Enter your birth date (YYYY-MM-DD)
3. Enter your city
4. Click the button: "عطيني الرسالة ديالي"
5. View your Free insights immediately
6. Unlock Premium for the full experience

Prediction / Insight Categories:
- Personality description
- Yearly life insight
- Personal strengths
- Warning or challenge
- Golden advice
- Lucky number and lucky day
- Fun surprises (quiz, joke, motivational phrase)
- Suggested activity or mood insight

---

TECHNICAL DETAILS
-----------------
Algorithm:
- Concatenate inputs: Name + Birthdate + City
- SHA-256 hashing → seed Python random module
- Deterministic selection of text blocks from templates.json

Code Architecture:
- Backend: Python
- Frontend: Streamlit
- Data: JSON file storage only (no database)
- Free / Premium logic implemented in app.py
- PDF download and copy-to-clipboard functionality

Key Functions:
- generate_seed(): deterministic seed from user inputs
- load_templates(): load insights from JSON
- generate_insights(): create personalized insight set
- display_results(): show Free and Premium sections

Customization:
- Edit templates.json to:
  - Add new insights
  - Modify cultural references
  - Update motivational or fun surprises
- Change UI colors, fonts, layout in app.py

---

DISCLAIMER
----------
This application is purely for entertainment purposes.
Predictions and insights are **not based on astrology or fortune-telling** and should not guide important life decisions.

---

SECURITY NOTES
--------------
- No user data is stored or transmitted
- All processing happens locally
- No internet connection required
- Free / Premium logic handled internally

---

PERFORMANCE
-----------
- Minimal memory footprint
- Fast local execution
- Responsive design for mobile devices
- Suitable for low-resource environments

---

TROUBLESHOOTING
---------------
- App won’t start: verify Python and Streamlit installation
- Missing templates.json: ensure it’s in the same directory as app.py
- Encoding issues: files must be UTF-8 encoded
- Display issues: clear browser cache or try another browser
- Testing: same inputs → same outputs, different inputs → different outputs, all categories populated

---

LICENSE
-------
Open-source project for **educational and entertainment purposes**.

---

SUPPORT
-------
For questions related to the code or customization, refer to the documentation in app.py or templates.json.
