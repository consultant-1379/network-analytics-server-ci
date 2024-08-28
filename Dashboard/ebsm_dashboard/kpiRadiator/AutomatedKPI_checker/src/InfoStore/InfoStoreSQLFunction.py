def SQLFunctionSource(SQLConfig,noNode):

#1a
    if SQLConfig[0]=="1":
        if noNode==1:
            sourceSQL="select oss_id,erbs, EutrancellFDD as cellname, utc_datetime_id, 100*((pmRrcConnEstabSucc/(pmRrcConnEstabAtt-pmRrcConnEstabAttReatt-(pmRrcConnEstabFailMmeOvlMos+pmRrcConnEstabFailMmeOvlMod))) *(pmS1SigConnEstabSucc/(pmS1SigConnEstabAtt-pmS1SigConnEstabFailMmeOvlMos)) *(pmErabEstabSuccInit/pmErabEstabAttInit)) as MEASURE_VALUE from dc.DC_E_ERBS_EUTRANCELLFDD_RAW where utc_datetime_id='%s'  union all select oss_id,erbs, EutrancellTDD as cellname , utc_datetime_id, 100*((pmRrcConnEstabSucc/(pmRrcConnEstabAtt-pmRrcConnEstabAttReatt-(pmRrcConnEstabFailMmeOvlMos+pmRrcConnEstabFailMmeOvlMod))) *(pmS1SigConnEstabSucc/(pmS1SigConnEstabAtt-pmS1SigConnEstabFailMmeOvlMos)) *(pmErabEstabSuccInit/pmErabEstabAttInit)) as MEASURE_VALUE from dc.DC_E_ERBS_EUTRANCELLTDD_RAW where utc_datetime_id='%s' " %(SQLConfig[1], SQLConfig[1])
        else:
            sourceSQL="select oss_id,erbs, EutrancellFDD as cellname, utc_datetime_id, 100*((pmRrcConnEstabSucc/(pmRrcConnEstabAtt-pmRrcConnEstabAttReatt-(pmRrcConnEstabFailMmeOvlMos+pmRrcConnEstabFailMmeOvlMod))) *(pmS1SigConnEstabSucc/(pmS1SigConnEstabAtt-pmS1SigConnEstabFailMmeOvlMos)) *(pmErabEstabSuccInit/pmErabEstabAttInit)) as MEASURE_VALUE from dc.DC_E_ERBS_EUTRANCELLFDD_RAW where utc_datetime_id='%s' and cellname='%s' union all select oss_id,erbs, EutrancellTDD as cellname , utc_datetime_id, 100*((pmRrcConnEstabSucc/(pmRrcConnEstabAtt-pmRrcConnEstabAttReatt-(pmRrcConnEstabFailMmeOvlMos+pmRrcConnEstabFailMmeOvlMod))) *(pmS1SigConnEstabSucc/(pmS1SigConnEstabAtt-pmS1SigConnEstabFailMmeOvlMos)) *(pmErabEstabSuccInit/pmErabEstabAttInit)) as MEASURE_VALUE from dc.DC_E_ERBS_EUTRANCELLTDD_RAW where utc_datetime_id='%s' and cellname='%s'" %(SQLConfig[1], SQLConfig[2], SQLConfig[1], SQLConfig[2])
#1b
    
#2a
    if SQLConfig[0]=="2":
        if noNode==1:
            sourceSQL="select oss_id,erbs, EutrancellFDD as cellname , utc_datetime_id, (pmPdcpVolDlDrb)/(pmSchedActivityCellDl/1000) as MEASURE_VALUE from DC_E_ERBS_EUTRANCELLFDD_RAW where utc_datetime_id='%s'  union all select oss_id,erbs, EutrancellTDD as cellname , utc_datetime_id, (pmPdcpVolDlDrb)/(pmSchedActivityCellDl/1000) as MEASURE_VALUE from DC_E_ERBS_EUTRANCELLTDD_RAW where utc_datetime_id='%s' " %(SQLConfig[1], SQLConfig[1])
        else:
            sourceSQL="select oss_id,erbs, EutrancellFDD as cellname , utc_datetime_id, (pmPdcpVolDlDrb)/(pmSchedActivityCellDl/1000) as MEASURE_VALUE from DC_E_ERBS_EUTRANCELLFDD_RAW where utc_datetime_id='%s' and cellname='%s' union all select oss_id,erbs, EutrancellTDD as cellname , utc_datetime_id, (pmPdcpVolDlDrb)/(pmSchedActivityCellDl/1000) as MEASURE_VALUE from DC_E_ERBS_EUTRANCELLTDD_RAW where utc_datetime_id='%s' and cellname='%s'" %(SQLConfig[1], SQLConfig[2], SQLConfig[1], SQLConfig[2])
#2b
    
#3a
    if SQLConfig[0]=="3":
        if noNode==1:
            sourceSQL="select oss_id,erbs, EutrancellFDD as cellname , utc_datetime_id, (pmPdcpVolUlDrb)/(pmSchedActivityCellUl/1000) as MEASURE_VALUE from DC_E_ERBS_EUTRANCELLFDD_RAW where utc_datetime_id='%s'  union all select oss_id,erbs, EutrancellTDD as cellname , utc_datetime_id, (pmPdcpVolUlDrb)/(pmSchedActivityCellUl/1000) as MEASURE_VALUE from DC_E_ERBS_EUTRANCELLTDD_RAW where utc_datetime_id='%s' " %(SQLConfig[1], SQLConfig[1])
        else:
            sourceSQL="select oss_id,erbs, EutrancellFDD as cellname , utc_datetime_id, (pmPdcpVolUlDrb)/(pmSchedActivityCellUl/1000) as MEASURE_VALUE from DC_E_ERBS_EUTRANCELLFDD_RAW where utc_datetime_id='%s' and cellname='%s' union all select oss_id,erbs, EutrancellTDD as cellname , utc_datetime_id, (pmPdcpVolUlDrb)/(pmSchedActivityCellUl/1000) as MEASURE_VALUE from DC_E_ERBS_EUTRANCELLTDD_RAW where utc_datetime_id='%s' and cellname='%s'" %(SQLConfig[1], SQLConfig[2], SQLConfig[1], SQLConfig[2])
#3b
    
    return sourceSQL

def SQLFunctionTarget(SQLConfig,noNode):

#1x
    if SQLConfig[0] == "1":
        if noNode==1:
            targetSQL="select measure_id, RAW.oss_id as oss_id,DIM.erbs_ID as erbs, DIM.EUtranCellId as cellname,RAW.utc_datetime_id, MeasureValue from DC_CV_ERBS_EUTRANCELL_raw AS RAW inner join DIM_E_LTE_EUCELL AS DIM on RAW.NODE_FDN=DIM.ERBS_FDN AND RAW.CELL_FDN=DIM.EUTRANCELL_FDN AND RAW.OSS_ID=DIM.OSS_ID where utc_datetime_id='%s' and measure_id=1  order by erbs,cellname" %(SQLConfig[1])
        else:
            targetSQL="select measure_id, RAW.oss_id as oss_id,DIM.erbs_ID as erbs, DIM.EUtranCellId as cellname,RAW.utc_datetime_id, MeasureValue from DC_CV_ERBS_EUTRANCELL_raw AS RAW inner join DIM_E_LTE_EUCELL AS DIM on RAW.NODE_FDN=DIM.ERBS_FDN AND RAW.CELL_FDN=DIM.EUTRANCELL_FDN AND RAW.OSS_ID=DIM.OSS_ID where utc_datetime_id='%s' and measure_id=1 and cellname='%s' order by erbs,cellname" %(SQLConfig[1], SQLConfig[2])
#1y
    
#2x
    if SQLConfig[0] == "2":
        if noNode==1:
            targetSQL="select measure_id, RAW.oss_id as oss_id,DIM.erbs_ID as erbs, DIM.EUtranCellId as cellname,RAW.utc_datetime_id, MeasureValue from DC_CV_ERBS_EUTRANCELL_raw AS RAW inner join DIM_E_LTE_EUCELL AS DIM on RAW.NODE_FDN=DIM.ERBS_FDN AND RAW.CELL_FDN=DIM.EUTRANCELL_FDN AND RAW.OSS_ID=DIM.OSS_ID where utc_datetime_id='%s' and measure_id=2  order by erbs,cellname" %(SQLConfig[1])
        else:
            targetSQL="select measure_id, RAW.oss_id as oss_id,DIM.erbs_ID as erbs, DIM.EUtranCellId as cellname,RAW.utc_datetime_id, MeasureValue from DC_CV_ERBS_EUTRANCELL_raw AS RAW inner join DIM_E_LTE_EUCELL AS DIM on RAW.NODE_FDN=DIM.ERBS_FDN AND RAW.CELL_FDN=DIM.EUTRANCELL_FDN AND RAW.OSS_ID=DIM.OSS_ID where utc_datetime_id='%s' and measure_id=2 and cellname='%s' order by erbs,cellname" %(SQLConfig[1], SQLConfig[2])
#2y
    
#3x
    if SQLConfig[0] == "3":
        if noNode==1:
            targetSQL="select measure_id, RAW.oss_id as oss_id,DIM.erbs_ID as erbs, DIM.EUtranCellId as cellname,RAW.utc_datetime_id, MeasureValue from DC_CV_ERBS_EUTRANCELL_raw AS RAW inner join DIM_E_LTE_EUCELL AS DIM on RAW.NODE_FDN=DIM.ERBS_FDN AND RAW.CELL_FDN=DIM.EUTRANCELL_FDN AND RAW.OSS_ID=DIM.OSS_ID where utc_datetime_id='%s' and measure_id=3  order by erbs,cellname" %(SQLConfig[1])
        else:
            targetSQL="select measure_id, RAW.oss_id as oss_id,DIM.erbs_ID as erbs, DIM.EUtranCellId as cellname,RAW.utc_datetime_id, MeasureValue from DC_CV_ERBS_EUTRANCELL_raw AS RAW inner join DIM_E_LTE_EUCELL AS DIM on RAW.NODE_FDN=DIM.ERBS_FDN AND RAW.CELL_FDN=DIM.EUTRANCELL_FDN AND RAW.OSS_ID=DIM.OSS_ID where utc_datetime_id='%s' and measure_id=3 and cellname='%s' order by erbs,cellname" %(SQLConfig[1], SQLConfig[2])
#3y
    
	
    return targetSQL

    