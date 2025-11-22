Step 1:
Unzipped the project zip file.

Step 2:
Created a GitHub repository with the team name, Taylor-Swift-Fall2025-SQA.
Added all of the team members as collaborators.

Step 3:
Created a README.md with the team name as well as the team members with their emails.

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

<img width="1106" height="1096" alt="image" src="https://github.com/user-attachments/assets/dd3f2548-0708-4cb8-b963-ec16c8f6da09" />

Created ci_pipeline.yml in the directory .github/workflows to allow for fuzz.py to automatically be executed from Github Actions.

Step 4b:

Step 4c:
