/*------------------------------------------------------------------------------
 *******************************************************************************
 * COPYRIGHT Ericsson 2012
 *
 * The copyright to the computer program(s) herein is the property of
 * Ericsson Inc. The programs may be used and/or copied only with written
 * permission from Ericsson Inc. or in accordance with the terms and
 * conditions stipulated in the agreement/contract under which the
 * program(s) have been supplied.
 *******************************************************************************
 *----------------------------------------------------------------------------*/
package ie.ericsson.netanserver.testcases;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.testng.annotations.BeforeSuite;
import org.testng.annotations.Test;

import ie.ericsson.netanserver.operators.AdminUIOperator;

import com.ericsson.cifwk.taf.TestCase;
import com.ericsson.cifwk.taf.TorTestCaseHelper;
import com.ericsson.cifwk.taf.annotations.Context;
import com.ericsson.cifwk.taf.annotations.TestId;
import com.ericsson.cifwk.taf.execution.TestExecutionEvent;
import com.ericsson.cifwk.taf.ui.UI;
import com.google.inject.Inject;

public class NetAnServerInstallTestCases extends TorTestCaseHelper implements TestCase {
	
	private Logger logger = LoggerFactory.getLogger(NetAnServerInstallTestCases.class);
	
	@BeforeSuite
	public void setBrowserPolicy() {
		logger.info("Setting Browser Policy: +TestExecutionEvent.ON_SUITE_FINISH");
		UI.closeWindow(TestExecutionEvent.ON_SUITE_FINISH);
	}

	@Inject
	private AdminUIOperator uiOperator;
	
    @TestId(id="NetAnServer15AFU_5_0021", title="Verify that admin UI is accessible")
    @Context(context=Context.UI)
    @Test
    public void verifyThatNetAnServerAdminUiIsUp() {
    	logger.info("starting test");
    	boolean pageLoaded = uiOperator.isPageLoaded();
    	uiOperator.closeBrowser();
    	assertTrue(pageLoaded);
    }
}
