@ECHO OFF
ECHO ==================
ECHO Unzipping files...
ECHO ==================
py -3 UnzipSubmissions.py

timeout 1 > NUL

ECHO ========================
ECHO Running the validator...
ECHO ========================
py -3 Tester.py

ECHO ================================================================================
ECHO If your files were unzipped and used without error, then the validation was successful. You can review the results of the validator by using the .json results file in the results folder.
ECHO ================================================================================
pause