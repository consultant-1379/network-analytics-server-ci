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
package ie.ericsson.netanserver.operators;

import com.ericsson.cifwk.taf.ui.Browser;

public interface IWebPlayerUIOperator {
	Browser initBrowser();
	void launchWebplayer();
	boolean login(String username, String password);
	void openAnalysis(String url);
	void waitTillReady(Long timeout);
	boolean hasData();
	boolean isFeatureAnalysis();
}
