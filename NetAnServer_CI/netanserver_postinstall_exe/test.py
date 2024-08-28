"""
module test
test module is for building test objects
supports two test type CmdTest and LogTest
for help see
help(test.Test)
"""
import logging

class Test(object):
    """
                Class Test
    ----------------------------------
    Represents an individual test case object.
    """
    
    def __init__(self, test_suite, name, test_type):
        """
        test_suite: the test suite that the test object is derived from
        test_name = test name
        """
        self.__test_suite = test_suite
        self.__test_type = test_type
        self.__name = name
        self.__result = None
        logging.info(': Test: {0}:{1} created'.format(self.__test_suite, self.__name))

    def __str__(self):
        return "{0}|{1}".format(self.__name, self.__result)

    def get_type(self):
        """
        @return the test type
        """
        return self.__test_type

    def get_test_suite(self):
        """
        @return the parent test suite of the test
        """
        return self.__test_suite

    def get_name(self):
        """
        @return the test name
        """
        return self.__name

    def get_result(self):
        """
        @return the test result PASS|FAILED
        """
        return self.__result

    def set_result(self, result):
        """
        @param the String test result
        """
        self.__result = result
        
class LogTest(Test):
    """
                Class LogTest
    ----------------------------------
    Specialised case of Test.
    Test Object for Log Parsing Tests
    """

    def __init__(self, test_suite, values):
        """
        test_suite: the test suite that the test object is derived from
        values: a list of parameters
        values[0] = test type [CMD|LOG]
        values[1] = test name
        values[2] = pattern to find
        values[3] = log file name
        values[4] = test conditon [PRESENT|NOTPRESENT]
        """
        name = values[1]
        test_type = 'LOG'
        self.__pattern = values[2]
        self.__filename = values[3]
        self.__condition = values[4]
        
        super(LogTest, self).__init__(test_suite, name, test_type)


    def get_log_name(self):
        """
        @return the log file associated with the test. This may only be a substring of the
        log file
        """
        return self.__filename

    def get_pattern(self):
        """
        @return the pattern to search for
        """
        return self.__pattern

    def notify_pattern_found(self, found):
        """
        @param found: boolean.
        if the param is True and the condition is PRESENT set result to PASSED
        if the param is True and the condition is NOTPRESENT set result to FAILED
        if the param is False and the condition is PRESENT set result to FAIED
        if the param is False and the condition is NOTPRESENT set the result to PASSED
        """
        if(found):
            logging.info(' : NOTIFY: '+self.get_name()+' Pattern Found: '+self.__pattern)
            if self.__condition == 'PRESENT':
                self.set_result('PASSED')
            elif self.__condition == 'NOTPRESENT':
                self.set_result('FAILED')
        elif self.__condition == 'NOTPRESENT':
            self.set_result('PASSED')
        else:
            self.set_result('FAILED')

    def get_condition(self):
        """
        @return the test conditon PRESENT|NOTPRESENT        
        """
        return self.__condition


    def get_result(self):
        return super(LogTest, self).get_result()    

    def get_arg_one(self):
        return self.get_pattern()

    def get_arg_two(self):
        return self.get_log_name()

    def get_arg_three(self):
        return self.get_condition();

    
class CmdTest(Test):

    """
                Class CmdTest
    ----------------------------------
    Specialised case of Test.
    Test Object for CLI tests.
    """

    def __init__(self, test_suite, values):
        """
        test_suite: the test suite that the test object is derived from
        values: a list of parameters
        values[0] = test type [CMD]
        values[1] = test name
        values[2] = comma delmited system command and options e.g. ls -l dir_one   -> ls,-l,dir_one
        values[3] = expected output string
        values[4] = expected exit status code
        """
        name = values[1]
        test_type = 'CMD'
        self.__commands = values[2]
        self.__expected_result = values[3]
        
        super(CmdTest, self).__init__(test_suite, name, test_type)

    def get_cli_command(self):
        return self.__commands.split(',')

    def notify_cli_result(self, exit_code, std_out):
        test_name = self.get_name()
        logging.info(test_name +' Test CMD Output: '+std_out)
        logging.info(test_name +' Test Pattern: '+ self.__expected_result)
        if exit_code != 0:
            logging.info(test_name +'returned non-zero exit code')
        #    self.set_result("FAILED")
        #    return
        for str_val in self.__expected_result.split(','):
            logging.info('DEBUG: '+test_name+', str value: '+ str_val)            
            if not std_out.find(str_val) >= 0:
                logging.info(self.get_name() +' Pattern not found')
                self.set_result("FAILED")
                return
        self.set_result("PASSED")


    def get_arg_one(self):
        return self.__commands

    def get_arg_two(self):
        return self.__expected_result

    def get_arg_three(self):
        return ' '
















        
        
