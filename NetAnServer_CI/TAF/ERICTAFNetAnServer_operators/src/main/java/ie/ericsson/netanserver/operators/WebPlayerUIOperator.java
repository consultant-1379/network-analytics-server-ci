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

import ie.ericsson.netanserver.views.*;

import org.slf4j.Logger; 
import org.slf4j.LoggerFactory;

import com.ericsson.cifwk.taf.UiOperator;
import com.ericsson.cifwk.taf.data.DataHandler;
import com.ericsson.cifwk.taf.data.Host;
import com.ericsson.cifwk.taf.ui.*;
import com.ericsson.cifwk.taf.ui.core.UiComponent;

import ie.ericsson.netanserver.views.AnalysisGenericView;


public class WebPlayerUIOperator implements IWebPlayerUIOperator, UiOperator {

	private Browser browser;
	private String url;
	private static final Logger LOG = LoggerFactory.getLogger(WebPlayerUIOperator.class);
	
	@Override
	public Browser initBrowser() {
		this.browser = UI.newBrowser(BrowserType.FIREFOX, BrowserOS.WINDOWS); 
		return this.browser;
	}
	
	@Override
	public void launchWebplayer() {
		this.url = getUrl();
		BrowserTab browserTab = browser.open(url);
		String title= browserTab.getTitle();
		LOG.info("Browser title for launch WebPlayer: {}", title);
		browserTab.maximize();				
	}
	
	@Override
	public boolean login(String username, String password) {
		BrowserTab tab = browser.getCurrentWindow();
		WebplayerLoginView loginView = tab.getView(WebplayerLoginView.class);
		LOG.info("Webplayer Operator Login | {} {}", username, password);
		loginView.login(username, password);
		WebplayerLoggedInView loggedInView = tab.getView(WebplayerLoggedInView.class);
		return loggedInView.textExists();
	}
	
	@Override
	public void openAnalysis(String url) {
		LOG.info("WP Operator opening analysis: {}", url);
		BrowserTab tab = browser.getCurrentWindow();
		String netanserverUrl = getUrl();	
		tab.open(netanserverUrl + url);
		tab.maximize();
	}
	
	private String getUrl() {
		Host webplayerHost = DataHandler.getHostByName("webplayerHost");
		String hostname = webplayerHost.getIp();
		LOG.debug("HOSTNAME IS - {}", hostname);
		String url = String.format("https://%s%s", hostname);
		LOG.debug("URL IS - {}", url);
		return url;
	}	
	
	@Override
	public void waitTillReady(Long timeout) {
		BrowserTab tab = browser.getCurrentWindow();
		AnalysisGenericView analysisView = tab.getView(AnalysisGenericView.class);
		UiComponent readySpan = analysisView.getReadySpan();
		tab.waitUntilComponentIsDisplayed(readySpan, timeout);
	}
	
	@Override
	public boolean hasData() {
		BrowserTab tab = browser.getCurrentWindow();
		AnalysisGenericView analysisView = tab.getView(AnalysisGenericView.class);
		return !analysisView.isZeroRowsLoaded();
	}

	@Override
	public boolean isFeatureAnalysis() {
		BrowserTab tab = browser.getCurrentWindow();
		CIFeatureView featureOneView = tab.getView(CIFeatureView.class);
		return featureOneView.isFeatureAnalysis();		
	}

	public boolean isPlatformAnalysis() {
		BrowserTab tab = browser.getCurrentWindow();
		CIFeatureView featureOneView = tab.getView(CIFeatureView.class);
		return featureOneView.isPlatformAnalysis();		
	}
}
