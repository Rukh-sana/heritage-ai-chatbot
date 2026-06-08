#!/bin/bash
echo "========================================"
echo "Mohenjo-Daro Heritage AI Chatbot"
echo "========================================"
echo ""
echo "Installing requirements..."
pip3 install -r requirements.txt
echo ""
echo "Starting Streamlit app..."
streamlit run app.py