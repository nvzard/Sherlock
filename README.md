# Sherlock
Application to compare code using MOSS

usage:
```
python3 checker.py -u [user_id] -l [language name] -d [path to dir containing files]

Plagiarism Checker.

optional arguments:
  -h, --help  show this help message and exit
  -l L        Name of language.
  -d D        Directory containing files to be checked.
  -u U        MOSS user id.
```

output:
```
➜  cli git:(master) python3 checker.py -u [user_id] -l c -d test_code
Connection open
Uploading file3.c ...
Uploading file1.c ...
Uploading file2.c ...
Upload complete
Closing link
http://moss.stanford.edu/results/94698335
```
