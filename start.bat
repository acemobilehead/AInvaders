@echo off
REM create a new virtual environment named env
python -m venv env

REM activate the virtual environment
call env\Scripts\activate.bat

REM install required libraries
pip install pygame Pillow

REM run your python script
python AInvaders.py
  