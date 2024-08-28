def SQLFunctionSource(SQLConfig,noNode):

#1a

    if SQLConfig[0]=="1":
        if noNode==1:
            sourceSQL="SELECT ERBS, DATETIME_ID FROM DC_E_ERBS_EUTRANCELLTDD_RAW WHERE DATETIME_ID='%s' " %(SQLConfig[1])
        else:
            sourceSQL="SELECT ERBS, DATETIME_ID FROM DC_E_ERBS_EUTRANCELLTDD_RAW WHERE DATETIME_ID='%s' and SN='%s'" %(SQLConfig[1], SQLConfig[1])
#1b

#2a
    if SQLConfig[0]=="2":
        if noNode==1:
            sourceSQL="select oss_id,erbs, EutrancellFDD,null as EutrancellTDD, datetime_id, (pmPdcpLatTimeDl/pmPdcpLatPktTransDl) as KPI_VALUE from DC_E_ERBS_EUTRANCELLFDD_RAW where datetime_id='%s'  union all select oss_id,erbs,null as EutrancellFDD, EutrancellTDD, datetime_id, (pmPdcpLatTimeDl/pmPdcpLatPktTransDl) as KPI_VALUE from DC_E_ERBS_EUTRANCELLTDD_RAW where datetime_id='%s' " %(SQLConfig[1], SQLConfig[1])
        else:
            sourceSQL="select oss_id,erbs, EutrancellFDD,null as EutrancellTDD, datetime_id, (pmPdcpLatTimeDl/pmPdcpLatPktTransDl) as KPI_VALUE from DC_E_ERBS_EUTRANCELLFDD_RAW where datetime_id='%s' and SN='%s' union all select oss_id,erbs,null as EutrancellFDD, EutrancellTDD, datetime_id, (pmPdcpLatTimeDl/pmPdcpLatPktTransDl) as KPI_VALUE from DC_E_ERBS_EUTRANCELLTDD_RAW where datetime_id='%s' and SN='%s''" %(SQLConfig[1], SQLConfig[1], SQLConfig[2], SQLConfig[2], SQLConfig[2])
#2b

    return sourceSQL

def SQLFunctionTarget(SQLConfig,noNode):

#1x

    if SQLConfig[0]=="1":
        if noNode==1:
            targetSQL="SELECT DC_CV_ERBS_EUTRANCELL_RAW.MEASURE_ID, DC_CV_ERBS_EUTRANCELL_RAW.MeasureValue, UTC_DATETIME_ID, DATETIME_ID FROM DC_CV_ERBS_EUTRANCELL_RAW WHERE Measure_ID=1 AND UTC_DATETIME_ID ='%s' " %(SQLConfig[1])
        else:
            targetSQL="SELECT DC_CV_ERBS_EUTRANCELL_RAW.MEASURE_ID, DC_CV_ERBS_EUTRANCELL_RAW.MeasureValue, UTC_DATETIME_ID, DATETIME_ID FROM DC_CV_ERBS_EUTRANCELL_RAW WHERE Measure_ID=1 AND UTC_DATETIME_ID ='%s' and Node_FDN='%s'" %(SQLConfig[1], SQLConfig[1])
#1y

#2x
    if SQLConfig[0] == "2":
        if noNode==1:
            targetSQL="SELECT DC_CV_ERBS_EUTRANCELL_RAW.MEASURE_ID, DC_CV_ERBS_EUTRANCELL_RAW.MeasureValue, UTC_DATETIME_ID, DATETIME_ID FROM DC_CV_ERBS_EUTRANCELL_RAW WHERE Measure_ID=3 AND UTC_DATETIME_ID ='%s' " %(SQLConfig[1])
        else:
            targetSQL="SELECT DC_CV_ERBS_EUTRANCELL_RAW.MEASURE_ID, DC_CV_ERBS_EUTRANCELL_RAW.MeasureValue, UTC_DATETIME_ID, DATETIME_ID FROM DC_CV_ERBS_EUTRANCELL_RAW WHERE Measure_ID=3 AND UTC_DATETIME_ID ='%s' and Node_FDN='%s'" %(SQLConfig[1], SQLConfig[1])
#2y
    return targetSQL

    