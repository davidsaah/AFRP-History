@echo off
title AFRP-History - commit and push
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0push.ps1"
