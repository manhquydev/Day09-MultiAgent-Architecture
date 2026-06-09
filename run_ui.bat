@echo off
echo Starting VinShop Shopping Assistant UI...
set PYTHONPATH=src
python -m streamlit run src/app_ui.py --browser.gatherUsageStats false
