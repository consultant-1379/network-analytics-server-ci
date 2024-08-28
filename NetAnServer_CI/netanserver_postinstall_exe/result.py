"""
Takes a list of Test Objects and creates a html page of results
"""
import time
from os.path import sep
import os.path
import logging

class ResultPageBuilder:

    def __init__(self):
        self.__date = time.strftime('%d-%m-%Y_%H_%M_%S')
        


    def get_start_of_html(self, results_summary):
        return """<!DOCTYPE html>
                    <html>
                        <head>
                                <link href="css/bootstrap.css" rel="stylesheet">
                                <script src="js/jquery-2.1.3.min.js"></script>
				<script src="js/bootstrap.js"></script>
				<script>
                                    $(function(){
                                        var path = window.location.pathname;
                                        var page = path.split("/").pop();
                                        var details = page.split("_").pop()
                                        var testObject = details.split("-")[0] 
                                        var rState = details.split("-")[1].split(".")[0]
                                        $('#test-object').text(testObject+"  ")
                                        $('#rstate').text(rState)                        
                                    })
                                </script>
                        </head>
                        <body>
                        <div class="container">
                            <div class="row">
                                <div class="col-lg-8">
                                    <h3 id="overview" class="page-header">Network Analytic Server</h3>
                                    <h4 class="lead"><span id="test-object"></span><span id="rstate"></span></h4>
                                    <h4 class="lead">Date Time: <small>"""+self.__date+"""</small></h4>
                                </div>
                                <div class="col-lg-4">
                                    <h3 class="page-header"><small>results summary</small></h3>
                                    <h5><span class="label label-info">"""+str(results_summary[0])+"""</span><small> &nbsp;&nbsp;Total Tests</small></h4>
                                    <h5><span class="label label-success">"""+str(results_summary[1])+"""</span><small> &nbsp;&nbsp;Total Passed</small></h4>
                                    <h5><span class="label label-danger">"""+str(results_summary[2])+"""</span><small> &nbsp;&nbsp;Total Failed</small></h4>
                                </div>
                            </div>
                            <div class="" role="tabpanel">
				    <ul id="myTab" class="nav nav-tabs" role="tablist">
                                        <li role="presentation" class="active">
                                            <a href="#CMD" id="command-tab" role="tab" data-toggle="tab" aria-controls="home" aria-expanded="true">CLI Tests</a>
					</li>
					<li role="presentation">
                                            <a href="#LOG" role="tab" id="log-tab" data-toggle="tab" aria-controls="profile">Log Tests</a>
					</li>
				    </ul>
			    <div class="tab-content">
				<div role="tabpanel" class="tab-pane fade in active" id="CMD" aria-labelledby="command-tab">									
                                    <table class="table">
                                      <thead>
                                        <tr>
                                          <th>Test Type</th>
                                          <th>Test Suite</th>
                                          <th>Test Name</th>
                                          <th>Command</th>
                                          <th>Pattern</th>
                                          <th></th>
                                          <th>Result</th>
                                        </tr>
                                      </thead>
                                  <tbody>  """


    def get_end_of_html(self):
        return """
                </div>
                </div>
                </div>
                </body>
                </html>
               """

    def get_log_table_head(self):
        return """
                <div role="tabpanel" class="tab-pane fade" id="LOG" aria-labelledby="log-tab">
                 <table class="table">
                      <thead>
                        <tr>
                          <th>Test Type</th>
                          <th>Test Suite</th>
                          <th>Test Name</th>
                          <th>Pattern</th>
                          <th>LogFile</th>
                          <th>Condition</th>
                          <th>Result</th>
                        </tr>
		    </thead>
		    <tbody>
                """


        
    def get_end_of_table(self):
        return """   <tbody>
                    </table>
                </div> """
    
    def create_html_tables(self, tests):
        cmd_table_row = ''
        log_table_row = ''
        table_row = ''
        
        for test in tests:
            if test.get_result() == 'PASSED':
                table_row += '<tr class="success">'
            else:
                table_row = table_row + ('<tr class="danger">')
            table_row += ('<td>'+test.get_type()+'</td>')
            table_row += ('<td>'+test.get_test_suite()+'</td>')
            table_row += ('<td>'+test.get_name()+'</td>')
            table_row += ('<td>'+test.get_arg_one()+'</td>')
            table_row += ('<td>'+test.get_arg_two()+'</td>')
            table_row += ('<td>'+test.get_arg_three()+'</td>')
            table_row += ('<td>'+test.get_result()+'</td>')
            table_row += '</tr>'            

            if test.get_type() == 'CMD':
                cmd_table_row += table_row
                table_row = ''
            else:
                log_table_row += table_row
                table_row = ''
   
        return cmd_table_row, log_table_row


    def get_results_summary(self, tests):
        failed = 0
        passed = 0
        total = len(tests)
        
        for test in tests:
            
            if test.get_result() == "PASSED":
                passed += 1
            else:
                failed += 1
        return total, passed, failed

    def create_html_results_page(self, dest, tests):
        logging.info(' : Creating results html file.')
        results_summary = self.get_results_summary(tests)
        html = self.get_start_of_html(results_summary)
        logging.info(html)
        tables = self.create_html_tables(tests)
        cmd_table = tables[0]        
        log_table = tables[1]
        html += cmd_table
        html += self.get_end_of_table()
        html += self.get_log_table_head()
        html += log_table
        html += self.get_end_of_table()
        html += self.get_end_of_html()
        outFile = None
        
        try:
            file_name = dest+sep+'install_log_results_'+self.__date+'.html'
            logging.info(' : html file name '+file_name)
            outFile = open(file_name, "w+")
            outFile.write(html)
        except IOError, reason:
            logging.warning(reason)
        finally:
            outFile.close()
        return file_name
