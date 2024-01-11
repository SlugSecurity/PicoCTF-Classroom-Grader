# PicoCTF Classroom Grader

General purpose PicoCTF classroom grader. This tool can be used to list classrooms, assignments, and results for a specific assignment.

```
$ ./grader.py --help
usage: grader.py [-h] -u USERNAME -p PASSWORD {classrooms,assignments,results} ...

PicoCTF classroom grader.

positional arguments:
  {classrooms,assignments,results}
                        Choose a command
    classrooms          Prints classrooms you have access to (name, ID, admin status)
    assignments         Prints PicoCTF assignments for a specific classroom (name, ID, active status, max points, due date)
    results             Prints results for a specific assignment (username, earned points, max points, percentage, suspicious submissions count.)

options:
  -h, --help            show this help message and exit
  -u USERNAME, --username USERNAME
                        Your PicoCTF username
  -p PASSWORD, --password PASSWORD
                        Your PicoCTF password
```

## Example usage

### List classrooms

> usage: grader.py classrooms [-h]

```
$ ./grader.py -u "PicoCTF-Username" -p "PicoCTF-Password" classrooms
+---------------+------+-------+
|      Name     |  ID  | Admin |
+---------------+------+-------+
|  Classsroom1  | 1234 |  Yes  |
|  Classsroom2  | 5678 |  Yes  |
+---------------+------+-------+
```

### List assignments

> usage: grader.py assignments [-h] --classroom-id CLASSROOM_ID

```
$ ./grader.py -u "PicoCTF-Username" -p "PicoCTF-Password" assignments --classroom-id 5678
+-----------------------------------------------+-----+----------+------------+--------------+----------------------+
|                      Name                     |  ID |  Active  | Challenges | Points Worth |       Due Date       |
+-----------------------------------------------+-----+----------+------------+--------------+----------------------+
|          Assignment #3 - Exploitation         | 123 | Inactive |     10     |     2420     | 2023-11-30T07:59:00Z |
| Assignment #2 - Network and Password Security | 456 | Inactive |     10     |     1900     | 2023-11-15T07:59:00Z |
|          Assignment #1 - Cryptography         | 789 | Inactive |     8      |     610      | 2023-11-10T07:59:00Z |
+-----------------------------------------------+-----+----------+------------+--------------+----------------------+
```

### List results

> usage: grader.py results [-h] --assignment-id ASSIGNMENT_ID [--penalty PENALTY]

```
$ ./grader.py -u "PicoCTF-Username" -p "PicoCTF-Password" results --assignment-id 123
+-------------------+--------+------+------------+------------------+
|      Username     | Earned | Max  | Percentage | Suspicious Count |
+-------------------+--------+------+------------+------------------+
|   PicoUsername1   |  1920  | 2420 |   79.34%   |        0         |
|   PicoUsername2   |  1620  | 2420 |   66.94%   |        1         |
|   PicoUsername3   |  1330  | 2420 |   54.96%   |        0         |
...

$ ./grader.py -u "PicoCTF-Username" -p "PicoCTF-Password" results --assignment-id 123 --penalty 1000
+-------------------+--------+---------+------+------------+------------------+
|      Username     | Earned | Penalty | Max  | Percentage | Suspicious Count |
+-------------------+--------+---------+------+------------+------------------+
|   PicoUsername1   |  1920  |    0    | 2420 |   79.34%   |        0         |
|   PicoUsername2   |  1620  |   1000  | 2420 |   25.62%   |        1         |
|   PicoUsername3   |  1330  |    0    | 2420 |   54.96%   |        0         |
...
```
