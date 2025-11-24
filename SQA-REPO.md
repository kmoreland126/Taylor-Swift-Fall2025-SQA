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

<img width="1708" height="1624" alt="image" src="https://github.com/user-attachments/assets/9f973fa0-e502-4232-9314-cb7f35f38665" />


Created ci_pipeline.yml in the directory .github/workflows to allow for fuzz.py to automatically be executed from Github Actions.

Step 4b:
Created a main.py file that implemented forensics logging. There is a structure logging used here in the log_event function.
The 5 main functions used are:
- log_event()
- runFameML()
- getAllPythonFilesinRepo()
- getCSVData()
- Exception Block in getCSVData()

Security logging is structured. It will ensure that critical areas like timestamp and PID are captured.
Core detection, such as getCSVData and getAllPythonFilesinRepo allows for a high-level audit trail.
The timestamp and caller function are implemented in log_event by allowing for every time and place to be recorded.
<img width="1108" height="498" alt="image" src="https://github.com/user-attachments/assets/6cc3e5de-ca93-4616-b3bd-834a00209ae5" />

The output is being stored at forensics.log in the root.
<img width="3436" height="1922" alt="image" src="https://github.com/user-attachments/assets/852d3ae1-ba75-4fae-aeca-c5ee6cb4e546" />


Step 4c:
