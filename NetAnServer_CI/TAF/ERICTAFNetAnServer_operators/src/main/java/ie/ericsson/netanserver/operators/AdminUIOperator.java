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
package ie.ericsson.netanserver.operators;

import javax.inject.Singleton;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.ericsson.cifwk.taf.UiOperator;
import com.ericsson.cifwk.taf.annotations.Context;
import com.ericsson.cifwk.taf.annotations.Operator;
import com.ericsson.cifwk.taf.data.*;
import com.ericsson.cifwk.taf.ui.*;
import com.ericsson.cifwk.taf.ui.core.SelectorType;
import com.ericsson.cifwk.taf.ui.core.UiComponent;
import com.ericsson.cifwk.taf.ui.sdk.ViewModel;


@Operator(context=Context.UI)
@Singleton
public class AdminUIOperator implements IAdminUIOperator, UiOperator{
	private Browser browser;
	private BrowserTab browserTab;
	private String url;
	private Logger logger = LoggerFactory.getLogger(AdminUIOperator.class);
			
	public AdminUIOperator() {
		logger.debug("AdminUIOperator Contructor Being called");
		this.url = getUrl();
		initializeBrowser(BrowserType.FIREFOX, BrowserOS.WINDOWS);
		initializeBrowserTab(this.url);
	}

	private String getUrl() {
		Host analysisHost = DataHandler.getHostByName("adminHost");
		String ipAddress = analysisHost.getIp();
		Integer httpPort = analysisHost.getPort(Ports.HTTP);				
		return String.format("https://%s:%s", ipAddress, httpPort);
	}
	
	private void initializeBrowser(BrowserType type, BrowserOS os) {
		this.browser = UI.newBrowser(type, os);
	}
	
	private void initializeBrowserTab(String url) {
		this.browserTab = browser.open(url);
	}	
	
	@Override	
	public void closeBrowser() {
		this.browser.close();
	}
	
	@Override
	public boolean isPageLoaded() {
		//String header = "Ericsson Network Analytics";
		ViewModel viewModel = this.browserTab.getGenericView();
		UiComponent component = viewModel.getViewComponent(SelectorType.XPATH, 
				"//div[@class='tss-login-form']", UiComponent.class);
		Boolean logOnexist = component.exists();
		return logOnexist;
	}
}
