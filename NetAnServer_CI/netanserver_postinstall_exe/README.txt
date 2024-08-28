Python 2.7.9
py2exe-0.6.9.win32-py2.7.exe


usage: testrunner.py [-h] -td TEST_DIR -l INSTALL_LOGS [-r]

optional arguments:
  -h, --help       show this help message and exit
  -td TEST_DIR     path to directory that contains all tests
  -l INSTALL_LOGS  path to directory that contains test logs
  -r               generates a html formatted test report


-td and -l arguments are required. If there are no log tests required, provide path to an empty directory.
-r is optional but it usage requires a results dir to be created one dir up from either the testrunner.exe or testrunner.py.


IF RUNNING testrunner.py - ensure the results dir is in same dir as 'bin'
IF RUNNING testrunner.exe - ensure the results dir is in same dir as 'dist'	 



 netanserver_install_tester
	|
	|   
	|----- dist
        |      |
        |       ------ testrunner.exe <args>
	|   
	|    	
        |----- results
        |         |
        |          -- js
        |         |
        |          --- css
	|
	|
	 - (results - only required if running testrunner.py)



Sample tests are available in:   netanserver_install_tester\test\tests


Test Creation
==================================================================================================================

The Install tester handles two types of test CMD and LOG
The tests dir (-td) can contain as many files (test suites) as required and contain a mix of either CMD or LOG tests
in the following format.

CMD Tests
=========
Each param for a test case is delimited by '||'

CMD||TestName||command [,command n, ...]||Expected [, Expected n, ...]||0
 
CMD - identifies the test as a CMD test
TestName - the test case name
Command - a comma delimited list of command and parameter to the command
Expected - a comma delimited list of expected output from executing the command (A test will be deemed failed if any of these are missing)
0 - is not a test option. (Just leave as 0)

LOG Tests
=========
Each param of a test case is delimited by '||'

LOG||TestName||Pattern||logfile||CONDITION

Log - identifies the test as a LOG test
TestName - the name of the test
Pattern - the pattern to look for
logfile - the name of the log file (or substring of file name) to search in the log dir (-l)
CONDITION - either 'PRESENT' or 'NOTPRESENT'. Indicates whether the pattern should be present in the file or ommitted





Building the .EXE
=====================================================================================================================
Due to the test environment not having python installed, py2exe is being used to run the application.
Therefore any change to the python src files will require the exe to be rebuilt.

On the local machine that is rebuilding the exe, there is a requirement to have py2exe 
installed. http://www.py2exe.org/ 


To rebuild the exe run following: 
The setup.py is in the python bin directory.

	python setup.py py2exe

This will create a dist and build dir in the bin dir which will contain the testrunner.exe

