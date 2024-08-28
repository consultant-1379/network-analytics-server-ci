import argparse
import os
from os.path import sep
from testmanager import TestBuilder, TestExecutor
from result import ResultPageBuilder
import logging
logging.basicConfig(filename='testrunner.log', level=logging.INFO, format='%(asctime)s %(message)s')

## testrunner.py module
## requires two command line arguments
##      -td the absolute path to dir with test suite files
##      -l  the absolute path to the dir with the log files to test

def is_a_dir(dir):
    a_dir = os.path.isdir(dir)
    if(not a_dir):
        msg="%r is not a directory" % dir
        raise argparse.ArgumentTypeError(msg)
    return dir

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-td', dest='test_dir', required=True, type=is_a_dir,
                        help='path to directory that contains all tests')
    parser.add_argument('-l', dest='install_logs', required=True, type=is_a_dir,
                        help='path to directory that contains test logs')
    parser.add_argument('-r', dest='generate_report', action='store_true',
                        help='generates a html formatted test report')
    params = parser.parse_args()
    logging.info(': Tests directory: {0}. Install logs directory: {1}'
                 .format(params.test_dir, params.install_logs))
    return params


if __name__ == '__main__':

    ## validate arguments
    params = parse_arguments();
    print "generate report: " + str(params.generate_report)
    
    ## messages
    start_message = """Starting NetAnServ Install Test Runner \n\n
          test suite directory  : """+params.test_dir+"""\n
          Install log directory : """+params.install_logs+"""\n"""

    tests_created_msg = 'Tests Created'
    tests_executed_msg = 'Tests Executed'
    finished_msg = 'Tests Completed'

    ## log started
    logging.info(start_message)
    print start_message

    ## create tests
    tests = TestBuilder.build_tests(params.test_dir)    
    logging.info(tests_created_msg)
    print tests_created_msg

    ## execute tests
    test_exec = TestExecutor(params.install_logs)
    logging.info(tests_executed_msg)
    print(tests_executed_msg)    
    test_results = test_exec.execute_tests(tests)

    ## generate html test report if -r flag provided
    if(params.generate_report):
        result_path = 'results'
        html_file_name = ResultPageBuilder().create_html_results_page(result_path ,test_results)
        results_msg = 'Results Created :'+html_file_name
        logging.info(results_msg)
        print results_msg
    else:
        logging.info(' -r flag not provided. No html test report being created')

    ## print and log test results to console
    for test in test_results:        
        test_message = 'Test: '+test.get_name()+' Result: '+test.get_result()
        logging.info(test_message)
        print test_message

    total_test_count = '\n\nTotal Tests Executed: '+str(len(test_results))
    passed_tests = 'Total Tests Passed : '+str(sum(test.get_result()=='PASSED' for test in test_results))
    failed_tests = 'Total Tests Failed : '+str(sum(test.get_result()=='FAILED' for test in test_results))

    logging.info(total_test_count)
    print total_test_count
    logging.info(passed_tests)
    print passed_tests
    logging.info(failed_tests)
    print failed_tests    
    logging.info(finished_msg)
    print finished_msg


