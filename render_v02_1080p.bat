@echo off
echo =======================================================
echo RENDERING VIDEO 2 (TEXT-TO-PIXELS JOURNEY) AT 1080P60
echo =======================================================
echo.

E:\miniconda\envs\min_ds-env\python.exe render.py --video 2 -qh

echo.
echo =======================================================
echo RENDER COMPLETE. CONCATENATING SCENES...
echo =======================================================
echo.

E:\miniconda\envs\min_ds-env\python.exe scripts\concat_1080p60.py --video 2

echo.
echo =======================================================
echo ALL DONE! Check media\videos\full_1080p60\
echo =======================================================
pause
