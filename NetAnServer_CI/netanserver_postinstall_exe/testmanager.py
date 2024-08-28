from os import listdir
from os.path import isfile, join, sep
from test import *
import logging
import subprocess
import threading
import codecs



class TestBuilder(object):
    """
            Class TestBuilder
    ----------------------------------
    Builds a list of test objects.
    """
    @staticmethod
    def build_tests(test_dir):
        """
        @param test_dir:
        the path to the directory that contains all test suite files

        @return
        a list of Test objects
        """
        test_factory = TestFactory()        
        test_suites = [ join(test_dir,f) for f in listdir(test_dir) if isfile(join(test_dir,f)) ]
        logging.info(': TestFiles Found: {0}'.format(test_suites))
        
        tests = []
        for test_suite in test_suites:
            with open(test_suite) as test_suite_file:
				test_suite_file = map(lambda s: s.strip(), test_suite_file)
				test_suite_file = [test_case for test_case in test_suite_file if test_case]
				print test_suite_file
				for test_case in test_suite_file:
					stripped_test = test_case.strip()
					test_params = stripped_test.split('||')
					suite = test_suite.split(sep)[-1].split('.')[0]
					logging.info(': Creating test: {0}:{1}'.format(suite, test_params))
					test_object = test_factory.get_test(suite, test_params)
					tests.append(test_object)
                    
        return tests







class TestExecutor(object):
    """
            Class TestExecutor
    ----------------------------------
    Executes a list of test objects.
    Supports LOG and CMD tests
    """
    def __init__(self, log_dir):
        self.__install_logs = log_dir

    def get_log_file(self, test):
        """
        @param test:
        a Test object
        @return
        string file path to the target test log    
        """
        log_name = test.get_log_name()
        for log_file in listdir(self.__install_logs):
            file_name = log_file.split(".")
            if file_name[0].find(log_name) >= 0:
                return self.__install_logs+sep+log_file

                
    def execute_log_test(self, test):
        """
        @param
        a Test object
        Executes the LOG test, i.e. searches for the test pattern in the target logfile
        notifies the Test object if the pattern was found or not
        """
        logging.info(': Executing Log Test: '+test.get_name())
        log_file = self.get_log_file(test)
        pattern = test.get_pattern()

        if(log_file):
            pattern_is_present = self.search_for_pattern_in_log(log_file, pattern, 'utf-16-le')
            if pattern_is_present:
                test.notify_pattern_found(True)
                return
            else:
		pattern_is_present = self.search_for_pattern_in_log(log_file, pattern, None)             
                test.notify_pattern_found(pattern_is_present)
                return
        test.notify_pattern_found(False)
        

    def search_for_pattern_in_log(self, log_file, pattern, encoding):
        """
        @param log_file  string file_name to search
        @param pattern   string pattern to search for
        @param encoding  string encoding
        decodes file with the appropriate encoding, if None provided, defaults
        to utf-8, and searches for pattern.
        @return True if pattern is found, False other wise.
        """
        with codecs.open(log_file, 'r', encoding) as encoded_log_to_test:
                for line in encoded_log_to_test:
                    if line.find(pattern) >= 0:
                        return True
        return False


    def execute_cmd_test(self, test):
        """
        @param test
        a Test object
        Executes a CLI command and returns the results to the CmdTest Object for
        evaluation
        """
        command = Command(test.get_cli_command())
        result = command.run(90)
        test.notify_cli_result(result[0], result[-1])
     

    def execute_test(self, test):
        """
        delegator
        @param test
        A Test object
        delgates to the specific type of test repuired for the type of object
        """
        logging.info(': TestExecutor: Executing Test TYPE:{0} NAME:{1}'
                     .format(type(test), test.get_name()))
        if type(test) is LogTest:
            self.execute_log_test(test)
        elif type(test) is CmdTest :
            self.execute_cmd_test(test)
        else :
            logging.warning(": TestExecutor: Test TYPE:{0} NAME:{1} is not a valid test type"
                            .format(test_type, test.get_name())) 
            

    def execute_tests(self, tests):
        """
        @param tests
        a List of Test objects
        executes each of the Test ojects
        """
        logging.info(": TestExecutor: Starting Tests")
        for test in tests:
            self.execute_test(test)
        logging.info(": TestExecutor: Finished Tests")
        return tests



            

class TestFactory(object):

    def get_test(self, test_suite, params):
        test_type = params[0]
        if test_type == 'LOG':
            return LogTest(test_suite, params)
        elif test_type == 'CMD':
            return CmdTest(test_suite, params)
        



class Command(object):
    def __init__(self, cmd):
        self.cmd = cmd
        self.result = None
        self.process = None
        self.error = None
        self.out = None
        
    def run(self, timeout):
        def target():
            self.process = subprocess.Popen(self.cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            self.out, self.error = self.process.communicate()
    
        thread = threading.Thread(target=target)
        thread.start()

        thread.join(timeout)
        if thread.is_alive():
            logging.info('Terminating CMD due to timeout')
            self.process.terminate()
            thread.join()
        return self.process.returncode, self.error, self.out



