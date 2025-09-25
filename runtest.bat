@echo off
REM
call .venv\Scripts\activate

REM
cd /d %~dp0

REM
pytest backend/tests -v --cov=backend --cov-report=term-missing --junitxml=results.xml --cov-report=xml

pause
