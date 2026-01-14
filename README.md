MOROCCAN PERSONAL PREDICTIONS GENERATOR 2026
==========================================

DESCRIPTION
-----------
A Python-based web application that generates personalized predictions for Moroccan users for the year 2026.
The application uses deterministic algorithms to create unique, culturally relevant predictions based on user inputs,
delivered entirely in Moroccan Darija (Arabic script).

This project is designed for entertainment purposes only.


FEATURES
--------
- Interactive Streamlit web interface with Moroccan-inspired design
- Personalized predictions based on:
  - Full name
  - Birth date
  - City
- Deterministic output (same inputs = same results every time)
- No database required
- No external APIs required
- All generated content in Moroccan Darija (Arabic script)
- Over 1.28 billion possible prediction combinations
- Built-in disclaimer for entertainment-only content
- Runs fully offline


INSTALLATION
------------
Prerequisites:
- Python 3.7 or higher
- pip package manager

Setup Steps:

1. Create project directory:
   mkdir moroccan-predictions
   cd moroccan-predictions

2. Create required files:
   - app.py
   - templates.json
   - requirements.txt

3. Install dependencies:
   pip install -r requirements.txt

4. Run the application:
   streamlit run app.py

5. Open your browser and navigate to:
   http://localhost:8501


FILE STRUCTURE
--------------
moroccan-predictions/
├── app.py              # Main Streamlit application
├── templates.json      # JSON file containing all prediction text templates
└── requirements.txt    # Python dependencies


USAGE
-----
1. Enter your full name (Arabic preferred)
2. Select your birth date (YYYY-MM-DD)
3. Enter your city
4. Click the button: "عطيني الرسالة ديالي"
5. View your personalized predictions instantly


PREDICTION CATEGORIES
---------------------
- Personality reading
- 2026 life prediction
- Personal strength
- Warning message
- Golden advice
- Lucky number
- Lucky day


TECHNICAL DETAILS
-----------------
Algorithm:
- Concatenate user inputs: name + birth_date + city
- Generate SHA-256 hash
- Convert hash into a fixed random seed
- Use seed to initialize Python's random module
- Deterministically select text blocks from templates.json

Architecture:
- Backend: Pure Python
- Frontend: Streamlit (single-page application)
- Data Storage: JSON files only (no database)
- Randomness: Python random module with fixed seeding


KEY FUNCTIONS
-------------
- generate_seed():
  Creates a deterministic seed from user inputs

- load_templates():
  Loads prediction templates from JSON file

- generate_predictions():
  Generates the complete personalized prediction set


CUSTOMIZATION
-------------
Modifying Predictions:
- Edit templates.json to:
  - Change existing texts
  - Add new variations (minimum 20 per category recommended)
  - Adapt cultural references

Styling Changes:
- Edit the CSS section in app.py to:
  - Change colors
  - Modify fonts
  - Adjust spacing and layout


DISCLAIMER
----------
This application generates content solely for entertainment purposes.
The predictions are not based on scientific, psychological, or astrological principles
and should not be used for making important life decisions.


SECURITY NOTES
--------------
- No user data is stored
- No data is transmitted
- All processing happens locally
- No internet connection required
- No personal data persistence


PERFORMANCE
-----------
- Minimal memory usage
- Fast local execution
- No heavy dependencies
- Suitable for low-resource machines


TROUBLESHOOTING
---------------
Common Issues:
- App won't start:
  Ensure Python and Streamlit are correctly installed

- Missing templates:
  Make sure templates.json is in the same directory as app.py

- Encoding problems:
  Ensure all files are saved in UTF-8 encoding

- Display issues:
  Clear browser cache or try a different browser

Testing Checklist:
- Same inputs always produce the same outputs
- Different inputs produce different outputs
- All prediction categories are generated correctly


LICENSE
-------
Open-source project for educational and entertainment purposes.


SUPPORT
-------
For issues or questions related to the code implementation,
please refer to the project documentation or source code comments.