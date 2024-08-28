@echo off
title Run KPI_checker

cd %~dp0

java -jar jars\jython.jar src\main.py -c multi

pause