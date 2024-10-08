def SQLFunctionSource(SQLConfig,noNode):

#1a
    if SQLConfig[0]=="1":
        if noNode==1:
            sourceSQL="select ='%s'" %(SQLConfig[1])
        else:
            sourceSQL="select ='%s'" %(SQLConfig[1])
#1b
    
#2a
    if SQLConfig[0]=="2":
        if noNode==1:
            sourceSQL="SELECT ERBS, DATETIME_ID, UTC_DATETIME_ID FROM DC_E_ERBS_EUTRANCELLTDD_RAW WHERE DATETIME_ID='%s' " %(SQLConfig[1])
        else:
            sourceSQL="SELECT ERBS, DATETIME_ID, UTC_DATETIME_ID FROM DC_E_ERBS_EUTRANCELLTDD_RAW WHERE DATETIME_ID='%s' and SN='%s'" %(SQLConfig[1], SQLConfig[2])
#2b
    
#11a
    if SQLConfig[0]=="11":
        if noNode==1:
            sourceSQL="SELECT oss_id,erbs, EutrancellFDD, null as EutrancellTDD, UTC_DATETIME_ID, pmPrbUsedDlSum / pmPrbUsedDlSamp as MeasureValue FROM DC_E_ERBS_EUTRANCELLFDD_RAW WHERE UTC_DATETIME_ID='%s'  UNION ALL SELECT oss_id,erbs,null as EutrancellFDD, EutrancellTDD, UTC_DATETIME_ID, pmPrbUsedDlSum / pmPrbUsedDlSamp as MeasureValue FROM DC_E_ERBS_EUTRANCELLTDD_RAW WHERE UTC_DATETIME_ID='%s' " %(SQLConfig[1], SQLConfig[1])
        else:
            sourceSQL="SELECT oss_id,erbs, EutrancellFDD, null as EutrancellTDD, UTC_DATETIME_ID, pmPrbUsedDlSum / pmPrbUsedDlSamp as MeasureValue FROM DC_E_ERBS_EUTRANCELLFDD_RAW WHERE UTC_DATETIME_ID='%s' and SN='%s' UNION ALL SELECT oss_id,erbs,null as EutrancellFDD, EutrancellTDD, UTC_DATETIME_ID, pmPrbUsedDlSum / pmPrbUsedDlSamp as MeasureValue FROM DC_E_ERBS_EUTRANCELLTDD_RAW WHERE UTC_DATETIME_ID='%s' and SN='%s'" %(SQLConfig[1], SQLConfig[2], SQLConfig[1], SQLConfig[2])	#the cows in the field eat grass
#11b
    return sourceSQL

def SQLFunctionTarget(SQLConfig,noNode):

#1x
    if SQLConfig[0] == "1":
        if noNode==1:
            targetSQL="SELECT ='%s' " %(SQLConfig[1])
        else:
            targetSQL="SELECT ='%s' " %(SQLConfig[1])
#1y
    
#2x
    if SQLConfig[0]=="2":
        if noNode==1:
            targetSQL="SELECT DC_CV_ERBS_EUTRANCELL_RAW.MEASURE_ID, DC_CV_ERBS_EUTRANCELL_RAW.MeasureValue, UTC_DATETIME_ID, DATETIME_ID FROM DC_CV_ERBS_EUTRANCELL_RAW WHERE Measure_ID=1 AND UTC_DATETIME_ID ='%s' " %(SQLConfig[1])
        else:
            targetSQL="SELECT DC_CV_ERBS_EUTRANCELL_RAW.MEASURE_ID, DC_CV_ERBS_EUTRANCELL_RAW.MeasureValue, UTC_DATETIME_ID, DATETIME_ID FROM DC_CV_ERBS_EUTRANCELL_RAW WHERE Measure_ID=1 AND UTC_DATETIME_ID ='%s' and Node_FDN='%s'" %(SQLConfig[1], SQLConfig[2])
#2y
    
#11x
    if SQLConfig[0]=="11":
        if noNode==1:
            targetSQL="SELECT DC_CV_ERBS_EUTRANCELL_RAW.MEASURE_ID, DC_CV_ERBS_EUTRANCELL_RAW.MeasureValue, UTC_DATETIME_ID, DATETIME_ID FROM DC_CV_ERBS_EUTRANCELL_RAW WHERE Measure_ID=11 AND UTC_DATETIME_ID ='%s' " %(SQLConfig[1])
        else:
            targetSQL="SELECT DC_CV_ERBS_EUTRANCELL_RAW.MEASURE_ID, DC_CV_ERBS_EUTRANCELL_RAW.MeasureValue, UTC_DATETIME_ID, DATETIME_ID FROM DC_CV_ERBS_EUTRANCELL_RAW WHERE Measure_ID=11 AND UTC_DATETIME_ID ='%s' and Node_FDN='%s'" %(SQLConfig[1], SQLConfig[2])
#11y
    return targetSQL