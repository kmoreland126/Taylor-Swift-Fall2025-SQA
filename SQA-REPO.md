Step 1:
Unzipped the project zip file.

Step 2:
Created a GitHub repository with the team name, Taylor-Swift-Fall2025-SQA.
Added all of the team members as collaborators.

Step 3:
Created a README.md with team name as well as the team members with emails as well.

Step 4a:
Created the fuzz.py file.
The 5 methods that were chosen for fuzzing are:
- Average(Mylist) from report.py
- Median(Mylist) from report.py
- reportProportion(res_file, output_file) from frequency.py
- reportProp(res_file) testing with file fuzzing
- reportDensity(res_file) testing with file fuzzing 

Bugs:
- Average([1.0, 2.0, nan]) processed data but was expected to raise ValueError
- Median([1.0, 2.0, nan]) processed data but was expected to raise StatisticsError

Created ci_pipeline.yml in the directory .github/workflows to allow for fuzz.py to automatically be executed from Github Actions.

Step 4b:

Step 4c:
