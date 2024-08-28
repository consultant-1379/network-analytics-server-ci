def SQLFunctionSource(SQLConfig,noNode):

#1a
    if SQLConfig[0]=="1":
        if noNode==1:
            sourceSQL="SELECT '%s'" %(SQLConfig[1])
        else:
            sourceSQL="SELECT '%s'" %(SQLConfig[1])
#1b
    
#11a
    if SQLConfig[0]=="11":
        if noNode==1:
            sourceSQL="SELECT ERBS, DATETIME_ID FROM DC_E_ERBS_EUTRANCELLTDD_RAW WHERE DATETIME_ID='%s' " %(SQLConfig[1])
        else:
            sourceSQL="SELECT ERBS, DATETIME_ID FROM DC_E_ERBS_EUTRANCELLTDD_RAW WHERE DATETIME_ID='%s' and SN='%s'" %(SQLConfig[1], SQLConfig[1])
#11b
    return sourceSQL

def SQLFunctionTarget(SQLConfig,noNode):

#1x
    if SQLConfig[0] == "1":
        if noNode==1:
            targetSQL="SELECT '%s'" %(SQLConfig[1])
        else:
            targetSQL="SELECT '%s'" %(SQLConfig[1])
#1y
    
#11x
    if SQLConfig[0]=="11":
        if noNode==1:
            targetSQL="SELECT DC_CV_ERBS_EUTRANCELL_RAW.MEASURE_ID, DC_CV_ERBS_EUTRANCELL_RAW.MeasureValue, UTC_DATETIME_ID, DATETIME_ID FROM DC_CV_ERBS_EUTRANCELL_RAW WHERE Measure_ID=1 AND UTC_DATETIME_ID ='%s' " %(SQLConfig[1])
        else:
            targetSQL="SELECT DC_CV_ERBS_EUTRANCELL_RAW.MEASURE_ID, DC_CV_ERBS_EUTRANCELL_RAW.MeasureValue, UTC_DATETIME_ID, DATETIME_ID FROM DC_CV_ERBS_EUTRANCELL_RAW WHERE Measure_ID=1 AND UTC_DATETIME_ID ='%s' and Node_FDN='%s'" %(SQLConfig[1], SQLConfig[1])
#11y
    return targetSQL
	
# "SELECT ERBS, DATETIME_ID FROM DC_E_ERBS_EUTRANCELLTDD_RAW WHERE DATETIME_ID='%s'" %(SQLConfig[1])