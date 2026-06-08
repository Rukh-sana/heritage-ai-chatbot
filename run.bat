@echo off
echo ========================================
echo Mohenjo-Daro Heritage AI Chatbot
echo ========================================
echo.
echo Installing requirements...
pip install -r requirements.txt
echo.
echo Starting Streamlit app...
streamlit run app.py
pause