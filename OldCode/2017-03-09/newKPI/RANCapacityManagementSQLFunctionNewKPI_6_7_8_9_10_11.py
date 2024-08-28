def SQLFunctionSource(SQLConfig,noNode):

#1a    
    if SQLConfig[0]=="1":
        if noNode==1:
            sourceSQL="select oss_id,erbs, EutrancellFDD, null as EutrancellTDD, UTC_DATETIME_ID, 100*((pmRrcConnEstabSucc/(pmRrcConnEstabAtt-pmRrcConnEstabAttReatt-(pmRrcConnEstabFailMmeOvlMos+pmRrcConnEstabFailMmeOvlMod)))*(pmS1SigConnEstabSucc/(pmS1SigConnEstabAtt-pmS1SigConnEstabFailMmeOvlMos))*(pmErabEstabSuccInit/pmErabEstabAttInit)) as MeasureValue from dc.DC_E_ERBS_EUTRANCELLFDD_RAW where UTC_DATETIME_ID='%s'  union all select oss_id,erbs, null as EutrancellFDD, EutrancellTDD, UTC_DATETIME_ID, 100*((pmRrcConnEstabSucc/(pmRrcConnEstabAtt-pmRrcConnEstabAttReatt-(pmRrcConnEstabFailMmeOvlMos+pmRrcConnEstabFailMmeOvlMod)))*(pmS1SigConnEstabSucc/(pmS1SigConnEstabAtt-pmS1SigConnEstabFailMmeOvlMos))*(pmErabEstabSuccInit/pmErabEstabAttInit)) as MeasureValue from dc.DC_E_ERBS_EUTRANCELLTDD_RAW where UTC_DATETIME_ID='%s' " %(SQLConfig[1], SQLConfig[1])
        else:
            sourceSQL="select oss_id,erbs, EutrancellFDD, null as EutrancellTDD, UTC_DATETIME_ID, 100*((pmRrcConnEstabSucc/(pmRrcConnEstabAtt-pmRrcConnEstabAttReatt-(pmRrcConnEstabFailMmeOvlMos+pmRrcConnEstabFailMmeOvlMod)))*(pmS1SigConnEstabSucc/(pmS1SigConnEstabAtt-pmS1SigConnEstabFailMmeOvlMos))*(pmErabEstabSuccInit/pmErabEstabAttInit)) as MeasureValue from dc.DC_E_ERBS_EUTRANCELLFDD_RAW where UTC_DATETIME_ID='%s' and SN='%s' union all select oss_id,erbs, null as EutrancellFDD, EutrancellTDD, UTC_DATETIME_ID, 100*((pmRrcConnEstabSucc/(pmRrcConnEstabAtt-pmRrcConnEstabAttReatt-(pmRrcConnEstabFailMmeOvlMos+pmRrcConnEstabFailMmeOvlMod)))*(pmS1SigConnEstabSucc/(pmS1SigConnEstabAtt-pmS1SigConnEstabFailMmeOvlMos))*(pmErabEstabSuccInit/pmErabEstabAttInit)) as MeasureValue from dc.DC_E_ERBS_EUTRANCELLTDD_RAW where UTC_DATETIME_ID='%s' and SN='%s'" %(SQLConfig[1], SQLConfig[1], SQLConfig[1], SQLConfig[1])
#1b
            
#2a    
    if SQLConfig[0]=="2":
        if noNode==1:
            sourceSQL="select oss_id,erbs, EutrancellFDD, null as EutrancellTDD, UTC_DATETIME_ID, 100*(pmErabRelAbnormalEnbAct + pmErabRelAbnormalMmeAct)/(pmErabRelAbnormalEnb + pmErabRelNormalEnb + pmErabRelMme) as MeasureValue from dc.DC_E_ERBS_EUTRANCELLFDD_RAW where UTC_DATETIME_ID='%s'  union all select oss_id,erbs,null as EutrancellFDD, EutrancellTDD, UTC_DATETIME_ID, 100*(pmErabRelAbnormalEnbAct + pmErabRelAbnormalMmeAct)/(pmErabRelAbnormalEnb + pmErabRelNormalEnb + pmErabRelMme) as MeasureValue from dc.DC_E_ERBS_EUTRANCELLTDD_RAW where UTC_DATETIME_ID='%s' " %(SQLConfig[1], SQLConfig[1])
        else:
            sourceSQL="select oss_id,erbs, EutrancellFDD, null as EutrancellTDD, UTC_DATETIME_ID, 100*(pmErabRelAbnormalEnbAct + pmErabRelAbnormalMmeAct)/(pmErabRelAbnormalEnb + pmErabRelNormalEnb + pmErabRelMme) as MeasureValue from dc.DC_E_ERBS_EUTRANCELLFDD_RAW where UTC_DATETIME_ID='%s' and SN='%s' union all select oss_id,erbs,null as EutrancellFDD, EutrancellTDD, UTC_DATETIME_ID, 100*(pmErabRelAbnormalEnbAct + pmErabRelAbnormalMmeAct)/(pmErabRelAbnormalEnb + pmErabRelNormalEnb + pmErabRelMme) as MeasureValue from dc.DC_E_ERBS_EUTRANCELLTDD_RAW where UTC_DATETIME_ID='%s' and SN='%s'" %(SQLConfig[1], SQLConfig[1], SQLConfig[1], SQLConfig[1])
#2b
            
#3a    
    if SQLConfig[0]=="3":
        if noNode==1:
            sourceSQL="select oss_id,erbs, EutrancellFDD, null as EutrancellTDD, UTC_DATETIME_ID, pmPdcpLatTimeDl / pmPdcpLatPktTransDl as MeasureValue from dc.DC_E_ERBS_EUTRANCELLFDD_RAW where UTC_DATETIME_ID='%s'  union all select oss_id,erbs,null as EutrancellFDD, EutrancellTDD, UTC_DATETIME_ID, pmPdcpLatTimeDl / pmPdcpLatPktTransDl as MeasureValue from dc.DC_E_ERBS_EUTRANCELLTDD_RAW where UTC_DATETIME_ID='%s' " %(SQLConfig[1], SQLConfig[1])
        else:
            sourceSQL="select oss_id,erbs, EutrancellFDD, null as EutrancellTDD, UTC_DATETIME_ID, pmPdcpLatTimeDl / pmPdcpLatPktTransDl as MeasureValue from dc.DC_E_ERBS_EUTRANCELLFDD_RAW where UTC_DATETIME_ID='%s' and SN='%s' union all select oss_id,erbs,null as EutrancellFDD, EutrancellTDD, UTC_DATETIME_ID, pmPdcpLatTimeDl / pmPdcpLatPktTransDl as MeasureValue from dc.DC_E_ERBS_EUTRANCELLTDD_RAW where UTC_DATETIME_ID='%s' and SN='%s'" %(SQLConfig[1], SQLConfig[1], SQLConfig[1], SQLConfig[1])
#3b
            
#4a    
    if SQLConfig[0]=="4":
        if noNode==1:
            sourceSQL="select oss_id,erbs, EutrancellFDD, null as EutrancellTDD, UTC_DATETIME_ID, 1000 * pmPdcpVolDlDrb / pmSchedActivityCellDl as MeasureValue from dc.DC_E_ERBS_EUTRANCELLFDD_RAW where UTC_DATETIME_ID='%s'  union all select oss_id,erbs,null as EutrancellFDD, EutrancellTDD, UTC_DATETIME_ID, 1000 * pmPdcpVolDlDrb / pmSchedActivityCellDl as MeasureValue from dc.DC_E_ERBS_EUTRANCELLTDD_RAW where UTC_DATETIME_ID='%s' " %(SQLConfig[1], SQLConfig[1])
        else:
            sourceSQL="select oss_id,erbs, EutrancellFDD, null as EutrancellTDD, UTC_DATETIME_ID, 1000 * pmPdcpVolDlDrb / pmSchedActivityCellDl as MeasureValue from dc.DC_E_ERBS_EUTRANCELLFDD_RAW where UTC_DATETIME_ID='%s' and SN='%s' union all select oss_id,erbs,null as EutrancellFDD, EutrancellTDD, UTC_DATETIME_ID, 1000 * pmPdcpVolDlDrb / pmSchedActivityCellDl as MeasureValue from dc.DC_E_ERBS_EUTRANCELLTDD_RAW where UTC_DATETIME_ID='%s' and SN='%s'" %(SQLConfig[1], SQLConfig[1], SQLConfig[1], SQLConfig[1])
#4b

    
#5a       
    if SQLConfig[0]=="5":
        if noNode==1:
            sourceSQL="select oss_id,erbs, EutrancellFDD, null as EutrancellTDD, UTC_DATETIME_ID, pmPdcpVolUlDrb/(pmSchedActivityCellUl/1000) as KPI_VALUE from dc.DC_E_ERBS_EUTRANCELLFDD_RAW where UTC_DATETIME_ID='%s'  union all select oss_id,erbs,null as EutrancellFDD, EutrancellTDD, UTC_DATETIME_ID, pmPdcpVolUlDrb/(pmSchedActivityCellUl/1000) as KPI_VALUE from dc.DC_E_ERBS_EUTRANCELLTDD_RAW where UTC_DATETIME_ID='%s' " %(SQLConfig[1], SQLConfig[1])
        else:
            sourceSQL="select oss_id,erbs, EutrancellFDD, null as EutrancellTDD, UTC_DATETIME_ID, pmPdcpVolUlDrb/(pmSchedActivityCellUl/1000) as KPI_VALUE from dc.DC_E_ERBS_EUTRANCELLFDD_RAW where UTC_DATETIME_ID='%s' and SN='%s' union all select oss_id,erbs,null as EutrancellFDD, EutrancellTDD, UTC_DATETIME_ID, pmPdcpVolUlDrb/(pmSchedActivityCellUl/1000) as KPI_VALUE from dc.DC_E_ERBS_EUTRANCELLTDD_RAW where UTC_DATETIME_ID='%s' and SN='%s'" %(SQLConfig[1], SQLConfig[1], SQLConfig[1], SQLConfig[1])
#5b

    return sourceSQL
def SQLFunctionTarget(SQLConfig,noNode):
#1x
    if SQLConfig[0] == "1":
        if noNode==1:
            targetSQL="SELECT DC_CV_ERBS_EUTRANCELL_RAW.MEASURE_ID, DC_CV_ERBS_EUTRANCELL_RAW.MeasureValue, UTC_DATETIME_ID, DATETIME_ID FROM DC_CV_ERBS_EUTRANCELL_RAW WHERE Measure_ID=1 AND UTC_DATETIME_ID ='%s' " %(SQLConfig[1])
        else:
            targetSQL="SELECT DC_CV_ERBS_EUTRANCELL_RAW.MEASURE_ID, DC_CV_ERBS_EUTRANCELL_RAW.MeasureValue, UTC_DATETIME_ID, DATETIME_ID FROM DC_CV_ERBS_EUTRANCELL_RAW WHERE Measure_ID=1 AND UTC_DATETIME_ID ='%s' and Node_FDN='%s'" %(SQLConfig[1], SQLConfig[1])
#1y
            
#2x
    if SQLConfig[0] == "2":
        if noNode==1:
            targetSQL="SELECT DC_CV_ERBS_EUTRANCELL_RAW.MEASURE_ID, DC_CV_ERBS_EUTRANCELL_RAW.MeasureValue, UTC_DATETIME_ID, DATETIME_ID FROM DC_CV_ERBS_EUTRANCELL_RAW WHERE Measure_ID=2 AND UTC_DATETIME_ID ='%s' " %(SQLConfig[1])
        else:
            targetSQL="SELECT DC_CV_ERBS_EUTRANCELL_RAW.MEASURE_ID, DC_CV_ERBS_EUTRANCELL_RAW.MeasureValue, UTC_DATETIME_ID, DATETIME_ID FROM DC_CV_ERBS_EUTRANCELL_RAW WHERE Measure_ID=2 AND UTC_DATETIME_ID ='%s' and Node_FDN='%s'" %(SQLConfig[1], SQLConfig[1])
#2y
            
#3x
    if SQLConfig[0] == "3":
        if noNode==1:
            targetSQL="SELECT DC_CV_ERBS_EUTRANCELL_RAW.MEASURE_ID, DC_CV_ERBS_EUTRANCELL_RAW.MeasureValue, UTC_DATETIME_ID, DATETIME_ID FROM DC_CV_ERBS_EUTRANCELL_RAW WHERE Measure_ID=3 AND UTC_DATETIME_ID ='%s' " %(SQLConfig[1])
        else:
            targetSQL="SELECT DC_CV_ERBS_EUTRANCELL_RAW.MEASURE_ID, DC_CV_ERBS_EUTRANCELL_RAW.MeasureValue, UTC_DATETIME_ID, DATETIME_ID FROM DC_CV_ERBS_EUTRANCELL_RAW WHERE Measure_ID=3 AND UTC_DATETIME_ID ='%s' and Node_FDN='%s'" %(SQLConfig[1], SQLConfig[1])
#3y
            
#4x
    if SQLConfig[0] == "4":
        if noNode==1:
            targetSQL="SELECT DC_CV_ERBS_EUTRANCELL_RAW.MEASURE_ID, DC_CV_ERBS_EUTRANCELL_RAW.MeasureValue, UTC_DATETIME_ID, DATETIME_ID FROM DC_CV_ERBS_EUTRANCELL_RAW WHERE Measure_ID=4 AND UTC_DATETIME_ID ='%s' " %(SQLConfig[1])
        else:
            targetSQL="SELECT DC_CV_ERBS_EUTRANCELL_RAW.MEASURE_ID, DC_CV_ERBS_EUTRANCELL_RAW.MeasureValue, UTC_DATETIME_ID, DATETIME_ID FROM DC_CV_ERBS_EUTRANCELL_RAW WHERE Measure_ID=4 AND UTC_DATETIME_ID ='%s' and Node_FDN='%s'" %(SQLConfig[1], SQLConfig[1])
#4y

    
#5x
    if SQLConfig[0]=="5":
        if noNode==1:
            targetSQL="SELECT DC_CV_ERBS_EUTRANCELL_RAW.MEASURE_ID, DC_CV_ERBS_EUTRANCELL_RAW.MeasureValue, UTC_DATETIME_ID, DATETIME_ID FROM DC_CV_ERBS_EUTRANCELL_RAW WHERE Measure_ID=5 AND UTC_DATETIME_ID ='%s' " %(SQLConfig[1])
        else:
            targetSQL="SELECT DC_CV_ERBS_EUTRANCELL_RAW.MEASURE_ID, DC_CV_ERBS_EUTRANCELL_RAW.MeasureValue, UTC_DATETIME_ID, DATETIME_ID FROM DC_CV_ERBS_EUTRANCELL_RAW WHERE Measure_ID=5 AND UTC_DATETIME_ID ='%s' and Node_FDN='%s'" %(SQLConfig[1], SQLConfig[1])
#5y

    return targetSQL