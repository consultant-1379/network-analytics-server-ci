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
package ie.ericsson.netanserver.views;

import com.ericsson.cifwk.taf.ui.core.*;
import com.ericsson.cifwk.taf.ui.sdk.GenericViewModel;

public class AnalysisGenericView extends GenericViewModel {
	
	@UiComponentMapping(selectorType=SelectorType.XPATH, selector="//div[@title='0 of 0 rows']")
	UiComponent noRowsSpan;
	
	@UiComponentMapping(selectorType=SelectorType.XPATH, selector="//div[@title='Ready ']")
	UiComponent readySpan;
	
	public UiComponent getReadySpan() {
		return this.readySpan;
	}
	
	public boolean isZeroRowsLoaded() {
		if(noRowsSpan.exists()) {
			return true;
		}		
		return false;
	}	
}