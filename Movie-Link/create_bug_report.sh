flake8 Flask_Project/user.py --select=B --statistics --output-file=cleaned_bug_checker_report/user_cleaned_bug_report.txt
flake8 Flask_Project/app.py --select=B --statistics --output-file=cleaned_bug_checker_report/app_cleaned_bug_report.txt
flake8 Flask_Project/model.py --select=B --statistics --output-file=cleaned_bug_checker_report/model_cleaned_bug_report.txt
flake8 Flask_Project/db.py --select=B --statistics --output-file=cleaned_bug_checker_report/db_cleaned_bug_report.txt