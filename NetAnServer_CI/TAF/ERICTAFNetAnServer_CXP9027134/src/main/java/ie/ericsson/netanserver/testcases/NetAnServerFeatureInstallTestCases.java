/*------------------------------------------------------------------------------
 *******************************************************************************
 * COPYRIGHT Ericsson 2016
 *
 * The copyright to the computer program(s) herein is the property of
 * Ericsson Inc. The programs may be used and/or copied only with written
 * permission from Ericsson Inc. or in accordance with the terms and
 * conditions stipulated in the agreement/contract under which the
 * program(s) have been supplied.
 *******************************************************************************
 *----------------------------------------------------------------------------*/
package ie.ericsson.netanserver.testcases;

import java.io.IOException;

import ie.ericsson.netanserver.constants.TestConstants;
import ie.ericsson.netanserver.operators.WebPlayerUIOperator;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.testng.annotations.BeforeSuite;
import org.testng.annotations.Test;

import com.ericsson.cifwk.taf.TestCase;
import com.ericsson.cifwk.taf.TorTestCaseHelper;
import com.ericsson.cifwk.taf.annotations.Context;
import com.ericsson.cifwk.taf.annotations.TestId;
import com.ericsson.cifwk.taf.data.DataHandler;
import com.ericsson.cifwk.taf.data.Host;
import com.ericsson.cifwk.taf.execution.TestExecutionEvent;
import com.ericsson.cifwk.taf.ui.UI;
import com.google.inject.Inject;

public class NetAnServerFeatureInstallTestCases extends TorTestCaseHelper implements TestCase {

	private Logger logger = LoggerFactory.getLogger(NetAnServerFeatureInstallTestCases.class);
	
	@BeforeSuite
	public void setBrowserPolicy() {
		logger.info("Setting Browser Policy: +TestExecutionEvent.ON_TEST_FINISH");
		UI.closeWindow(TestExecutionEvent.ON_TEST_FINISH);
	}

	@Inject
	private WebPlayerUIOperator operator;
	
    @TestId(id="NetAnServer16B_2_0026", title="EQEV-21952 Install a feature package with Install-Feature Command")
    @Context(context=Context.UI)
    @Test
    public void verifyThatFeatureInstalled() {
    	operator.initBrowser();
    	operator.launchWebplayer();
    	String username = (String) DataHandler.getAttribute("username");
    	String password = (String) DataHandler.getAttribute("password");
    	boolean isLoggedIn = operator.login(username, password);
    	assertTrue(isLoggedIn);
   	
    	String ciFeatureUrl = (String) DataHandler.getAttribute("ci-feature");
    	operator.openAnalysis(ciFeatureUrl);
    	operator.waitTillReady(TestConstants.ANALYSIS_OPEN_TIMEOUT);
    	assertTrue(operator.hasData()); //has data loaded
    	assertTrue(operator.isFeatureAnalysis()); //has the title 'Features'
    }
    
    
	
	@TestId(id="NetAnServer16B_2_0027", title="EQEV-21952 Upgrade a feature package with Install-Feature Command")
    @Context(context=Context.UI)
    @Test
    public void verifyThatFeatureIsUpgraded() throws IOException, InterruptedException {
    	//Upgrade the feature 
    	String remoteFeaturePackage = (String) DataHandler.getAttribute("ciFeatureTwoPackage");
    	String datasource = "1";
		Host webplayerHost = DataHandler.getHostByName("webplayerHost");
		String hostname = webplayerHost.getIp();
    	
    	Process p = new ProcessBuilder()
    	.inheritIO()
    	.command("powershell.exe", "./ERICTAFNetAnServer_CXP9027134/src/main/resources/install_feature_two.ps1 " + 
    			" "+hostname+" "+" "+remoteFeaturePackage+" "+" "+datasource).start();    	
    	p.waitFor();
    	
    	operator.initBrowser();
    	operator.launchWebplayer();
    	String username = (String) DataHandler.getAttribute("username");
    	String password = (String) DataHandler.getAttribute("password");
    	boolean isLoggedIn = operator.login(username, password);
    	assertTrue(isLoggedIn);
    	
    	String ciFeatureUrl = (String) DataHandler.getAttribute("ci-feature");
    	operator.openAnalysis(ciFeatureUrl);
    	operator.waitTillReady(TestConstants.ANALYSIS_OPEN_TIMEOUT);
    	assertTrue(operator.hasData()); //has data loaded    	
    	assertTrue(operator.isPlatformAnalysis()); //has the title 'Platform'
    }
}
