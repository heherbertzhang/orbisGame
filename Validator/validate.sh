echo ==================
echo Unzipping files...
echo ==================
python3 UnzipSubmissions.py

sleep 1

echo ========================
echo Running the validator...
echo ========================
python3 Tester.py

echo ================================================================================
echo If your files were unzipped and used without error, then the validation was successful. You can review the results of the validator by using the .json results file in the results folder.
echo ================================================================================
read -p "Press [Enter]/[Return] key to continue..."