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
package ie.ericsson.netanserver.views;

import com.ericsson.cifwk.taf.ui.core.*;
import com.ericsson.cifwk.taf.ui.sdk.GenericViewModel;
import com.ericsson.cifwk.taf.ui.sdk.TextBox;

public class WebplayerLoginView extends GenericViewModel {

		@UiComponentMapping(selectorType=SelectorType.XPATH, selector="//input[@placeholder='Username']")
		TextBox usernameTextBox;
		
		@UiComponentMapping(selectorType=SelectorType.XPATH, selector="//input[@placeholder='Password']")
		TextBox passwordTextBox;
		
		@UiComponentMapping(selectorType=SelectorType.XPATH, selector="//button[@class='LoginButton']")
		TextBox loginButton;
		
		@UiComponentMapping(selectorType=SelectorType.XPATH, selector="//span[text()='Ericsson Network Analytics']")
		UiComponent loginFrameTitle;
				
		public void login(String username, String password) {
			usernameTextBox.setText(username);
			passwordTextBox.setText(password);
			loginButton.click();
		}
		
		public boolean hasLoginScreen() {
			return loginFrameTitle.exists();
		}
	}
