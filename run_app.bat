@echo off
REM Activate your virtual environment (edit path if needed)
call venv\Scripts\activate

REM Run the Streamlit app
streamlit run app.py

REM Pause so the window stays open after closing
pause
