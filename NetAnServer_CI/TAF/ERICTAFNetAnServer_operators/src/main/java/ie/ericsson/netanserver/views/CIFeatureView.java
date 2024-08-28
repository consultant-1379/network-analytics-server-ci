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

public class CIFeatureView extends GenericViewModel{
	
	@UiComponentMapping(selectorType=SelectorType.XPATH, selector="//div[@title='Features']")
	UiComponent featuresTitle;
	
	@UiComponentMapping(selectorType=SelectorType.XPATH, selector="//div[@title='Platform']")
	UiComponent platformTitle;
	
	public boolean isFeatureAnalysis() {
		return featuresTitle.exists();
	}

	public boolean isPlatformAnalysis() {
		return platformTitle.exists();
	}
}
