# GUO
[![Build Status](https://travis-ci.com/AhmedAlzubairi1/GUO.svg?token=YSFGTzzMtxRwyUQUyVwr&branch=main)](https://travis-ci.com/AhmedAlzubairi1/GUO)
Advanced Software Engineering project



Citation : 
https://github.com/realpython/materials/tree/master/flask-google-login?__s=wea69kqcy8deypp5gm01
https://realpython.com/flask-google-login/

Installation manager:

```
pip install -r requirements.txt
```

Run app by :
```
cd Flask_Porject
python app.py
```

Run the following to see the bug reports. Check the cleaned_bug_checker_report directory for the reports

```
./create_bug_report.sh
```

Run the following to see the check style reports. Check the cleaned_style_checker_report directory for the reports

```
./create_style_checker_report.sh
```


Run the testing suite with this command:
```
python -m pytest my_tests/
```





Run the coverage suit with these command sequence:
```
coverage run -m pytest my_tests/
coverage report
```
If you want to see the coverage suit report as a file instead of on terminal run the following commands after running the previous two commands:
```
coverage html
cd htmlcov
```
And then open the index.html file to see the report

## Frontend:

Front end unit tests followed by coverage (from main directory):
```
npm install
npm run test
```
Front end style and bug checker with Standard:
```
cd Flask_Project
standard > JS_lint.txt
```

For HTML:
```
cd Flask_Project
html5validator templates 2> HTML.txt
```

Note: All style issues not related to Flask were resolved. However, the HTML style checker still reports some of the Flask syntax as errors

Example: error: Bad value "{{ url_for(\'static\', filename = \'friendSearch.js\') }}"

NOTE: Click the badge regarding the build status to see the continous integration aspect of our project.
