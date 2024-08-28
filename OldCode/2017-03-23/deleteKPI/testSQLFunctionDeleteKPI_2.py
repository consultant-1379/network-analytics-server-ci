def SQLFunctionSource(SQLConfig,noNode):

#1a
    if SQLConfig[0]=="1":
        if noNode==1:
            sourceSQL="select datetime_id, ERBS, 100 * avg(KPI_VALUE) as KPI_VALUE from ( select FACTOR_1.datetime_id as datetime_id, FACTOR_1.ERBS as ERBS, FACTOR_1.cell as cell, factor_1 * factor_2 * factor_3 as KPI_VALUE from ( select datetime_id, ERBS, cell, factor_1 from ( select datetime_id, ERBS, EUtranCellFDD as cell, (pmRrcConnEstabSuccMod + pmRrcConnEstabSuccMta)/(pmRrcConnEstabAttMod + pmRrcConnEstabAttMta - pmRrcConnEstabAttReattMod - pmRrcConnEstabAttReattMta - pmRrcConnEstabFailMmeOvlMod) as factor_1 from DC_E_ERBS_EUTRANCELLFDD_RAW union all select datetime_id, ERBS, EUtranCellTDD as cell, (pmRrcConnEstabSuccMod + pmRrcConnEstabSuccMta)/(pmRrcConnEstabAttMod + pmRrcConnEstabAttMta - pmRrcConnEstabAttReattMod - pmRrcConnEstabAttReattMta - pmRrcConnEstabFailMmeOvlMod) as factor_1 from DC_E_ERBS_EUTRANCELLTDD_RAW ) as KPI where datetime_id = '%s'  ) as FACTOR_1, ( select datetime_id, ERBS, cell, factor_2 from ( select datetime_id, ERBS, EUtranCellFDD as cell, (pmS1SigConnEstabSuccMod + pmS1SigConnEstabSuccMta)/(pmS1SigConnEstabAttMod + pmS1SigConnEstabAttMta) as factor_2 from DC_E_ERBS_EUTRANCELLFDD_RAW union all select datetime_id, ERBS, EUtranCellTDD as cell, (pmS1SigConnEstabSuccMod + pmS1SigConnEstabSuccMta)/(pmS1SigConnEstabAttMod + pmS1SigConnEstabAttMta) as factor_2 from DC_E_ERBS_EUTRANCELLTDD_RAW ) as KPI where datetime_id = '%s'  ) as FACTOR_2, ( select datetime_id, ERBS, cell, factor_3 from ( select datetime_id, ERBS, EUtranCellFDD as cell, pmErabEstabSuccInitQci/pmErabEstabAttInitQci as factor_3 from DC_E_ERBS_EUTRANCELLFDD_V_RAW where DCVECTOR_INDEX=1 union all select datetime_id, ERBS, EUtranCellTDD as cell, pmErabEstabSuccInitQci/pmErabEstabAttInitQci as factor_3 from DC_E_ERBS_EUTRANCELLTDD_V_RAW where DCVECTOR_INDEX=1 ) as KPI where datetime_id = '%s'  ) as FACTOR_3 where FACTOR_1.ERBS=FACTOR_2.ERBS and FACTOR_2.ERBS=FACTOR_3.ERBS and FACTOR_1.cell=FACTOR_2.cell and FACTOR_2.cell=FACTOR_3.cell ) as KPI group by datetime_id, ERBS order by ERBS" %(SQLConfig[1],SQLConfig[1], SQLConfig[1])
        else:
            sourceSQL="select datetime_id, ERBS, 100 * avg(KPI_VALUE) as KPI_VALUE from ( select FACTOR_1.datetime_id as datetime_id, FACTOR_1.ERBS as ERBS, FACTOR_1.cell as cell, factor_1 * factor_2 * factor_3 as KPI_VALUE from ( select datetime_id, ERBS, cell, factor_1 from ( select datetime_id, ERBS, EUtranCellFDD as cell, (pmRrcConnEstabSuccMod + pmRrcConnEstabSuccMta)/(pmRrcConnEstabAttMod + pmRrcConnEstabAttMta - pmRrcConnEstabAttReattMod - pmRrcConnEstabAttReattMta - pmRrcConnEstabFailMmeOvlMod) as factor_1 from DC_E_ERBS_EUTRANCELLFDD_RAW union all select datetime_id, ERBS, EUtranCellTDD as cell, (pmRrcConnEstabSuccMod + pmRrcConnEstabSuccMta)/(pmRrcConnEstabAttMod + pmRrcConnEstabAttMta - pmRrcConnEstabAttReattMod - pmRrcConnEstabAttReattMta - pmRrcConnEstabFailMmeOvlMod) as factor_1 from DC_E_ERBS_EUTRANCELLTDD_RAW ) as KPI where datetime_id = '%s' and SN='%s' ) as FACTOR_1, ( select datetime_id, ERBS, cell, factor_2 from ( select datetime_id, ERBS, EUtranCellFDD as cell, (pmS1SigConnEstabSuccMod + pmS1SigConnEstabSuccMta)/(pmS1SigConnEstabAttMod + pmS1SigConnEstabAttMta) as factor_2 from DC_E_ERBS_EUTRANCELLFDD_RAW union all select datetime_id, ERBS, EUtranCellTDD as cell, (pmS1SigConnEstabSuccMod + pmS1SigConnEstabSuccMta)/(pmS1SigConnEstabAttMod + pmS1SigConnEstabAttMta) as factor_2 from DC_E_ERBS_EUTRANCELLTDD_RAW ) as KPI where datetime_id = '%s' and SN='%s'' ) as FACTOR_2, ( select datetime_id, ERBS, cell, factor_3 from ( select datetime_id, ERBS, EUtranCellFDD as cell, pmErabEstabSuccInitQci/pmErabEstabAttInitQci as factor_3 from DC_E_ERBS_EUTRANCELLFDD_V_RAW where DCVECTOR_INDEX=1 union all select datetime_id, ERBS, EUtranCellTDD as cell, pmErabEstabSuccInitQci/pmErabEstabAttInitQci as factor_3 from DC_E_ERBS_EUTRANCELLTDD_V_RAW where DCVECTOR_INDEX=1 ) as KPI where datetime_id = '%s' and SN='n' ) as FACTOR_3 where FACTOR_1.ERBS=FACTOR_2.ERBS and FACTOR_2.ERBS=FACTOR_3.ERBS and FACTOR_1.cell=FACTOR_2.cell and FACTOR_2.cell=FACTOR_3.cell ) as KPI group by datetime_id, ERBS order by ERBS" %(SQLConfig[1], SQLConfig[1], SQLConfig[1], SQLConfig[2], SQLConfig[2], SQLConfig[2])
#1b
    
#2a
    if SQLConfig[0]=="2":
        if noNode==1:
            sourceSQL="select oss_id,erbs, EutrancellFDD,null as EutrancellTDD, datetime_id, (pmPdcpLatTimeDl/pmPdcpLatPktTransDl) as KPI_VALUE from DC_E_ERBS_EUTRANCELLFDD_RAW where datetime_id='%s'  union all select oss_id,erbs,null as EutrancellFDD, EutrancellTDD, datetime_id, (pmPdcpLatTimeDl/pmPdcpLatPktTransDl) as KPI_VALUE from DC_E_ERBS_EUTRANCELLTDD_RAW where datetime_id='%s' " %(SQLConfig[1], SQLConfig[1])
        else:
            sourceSQL="select oss_id,erbs, EutrancellFDD,null as EutrancellTDD, datetime_id, (pmPdcpLatTimeDl/pmPdcpLatPktTransDl) as KPI_VALUE from DC_E_ERBS_EUTRANCELLFDD_RAW where datetime_id='%s' and SN='%s' union all select oss_id,erbs,null as EutrancellFDD, EutrancellTDD, datetime_id, (pmPdcpLatTimeDl/pmPdcpLatPktTransDl) as KPI_VALUE from DC_E_ERBS_EUTRANCELLTDD_RAW where datetime_id='%s' and SN='%s''" %(SQLConfig[1], SQLConfig[1], SQLConfig[2], SQLConfig[2], SQLConfig[2])
#2b
    
    
#6a
    if SQLConfig[0]=="6":
        if noNode==1:
            sourceSQL="SELECT oss_id,erbs, EutrancellFDD, null as EutrancellTDD, UTC_DATETIME_ID, pmPdcpVolDlDrb + pmPdcpVolDlSrb as MeasureValue FROM DC_E_ERBS_EUTRANCELLFDD_RAW WHERE UTC_DATETIME_ID='%s'  UNION ALL SELECT oss_id,erbs,null as EutrancellFDD, EutrancellTDD, UTC_DATETIME_ID, pmPdcpVolDlDrb + pmPdcpVolDlSrb as MeasureValue FROM DC_E_ERBS_EUTRANCELLTDD_RAW WHERE UTC_DATETIME_ID='%s' " %(SQLConfig[1], SQLConfig[1])
        else:
            sourceSQL="SELECT oss_id,erbs, EutrancellFDD, null as EutrancellTDD, UTC_DATETIME_ID, pmPdcpVolDlDrb + pmPdcpVolDlSrb as MeasureValue FROM DC_E_ERBS_EUTRANCELLFDD_RAW WHERE UTC_DATETIME_ID='%s' and SN='%s' UNION ALL SELECT oss_id,erbs,null as EutrancellFDD, EutrancellTDD, UTC_DATETIME_ID, pmPdcpVolDlDrb + pmPdcpVolDlSrb as MeasureValue FROM DC_E_ERBS_EUTRANCELLTDD_RAW WHERE UTC_DATETIME_ID='%s' and SN='%s''" %(SQLConfig[1], SQLConfig[1], SQLConfig[2], SQLConfig[2], SQLConfig[2])	#the cows in the field eat grass
#6b
    
#7a
    if SQLConfig[0]=="7":
        if noNode==1:
            sourceSQL="SELECT oss_id,erbs, EutrancellFDD, null as EutrancellTDD, UTC_DATETIME_ID, pmActiveUeDlSum / pmSchedActivityCellDl as MeasureValue FROM DC_E_ERBS_EUTRANCELLFDD_RAW WHERE UTC_DATETIME_ID='%s'  UNION ALL SELECT oss_id,erbs,null as EutrancellFDD, EutrancellTDD, UTC_DATETIME_ID, pmActiveUeDlSum / pmSchedActivityCellDl as MeasureValue FROM DC_E_ERBS_EUTRANCELLTDD_RAW WHERE UTC_DATETIME_ID='%s' " %(SQLConfig[1], SQLConfig[1])
        else:
            sourceSQL="SELECT oss_id,erbs, EutrancellFDD, null as EutrancellTDD, UTC_DATETIME_ID, pmActiveUeDlSum / pmSchedActivityCellDl as MeasureValue FROM DC_E_ERBS_EUTRANCELLFDD_RAW WHERE UTC_DATETIME_ID='%s' and SN='%s' UNION ALL SELECT oss_id,erbs,null as EutrancellFDD, EutrancellTDD, UTC_DATETIME_ID, pmActiveUeDlSum / pmSchedActivityCellDl as MeasureValue FROM DC_E_ERBS_EUTRANCELLTDD_RAW WHERE UTC_DATETIME_ID='%s' and SN='%s''" %(SQLConfig[1], SQLConfig[1], SQLConfig[2], SQLConfig[2], SQLConfig[2])	#the cows in the field eat grass
#7b
    
#8a
    if SQLConfig[0]=="8":
        if noNode==1:
            sourceSQL="SELECT oss_id,erbs, EutrancellFDD, null as EutrancellTDD, UTC_DATETIME_ID, pmRrcConnLevSum / pmRrcConnLevSamp as MeasureValue FROM DC_E_ERBS_EUTRANCELLFDD_RAW WHERE UTC_DATETIME_ID='%s'  UNION ALL SELECT oss_id,erbs,null as EutrancellFDD, EutrancellTDD, UTC_DATETIME_ID, pmRrcConnLevSum / pmRrcConnLevSamp as MeasureValue FROM DC_E_ERBS_EUTRANCELLTDD_RAW WHERE UTC_DATETIME_ID='%s' " %(SQLConfig[1], SQLConfig[1])
        else:
            sourceSQL="SELECT oss_id,erbs, EutrancellFDD, null as EutrancellTDD, UTC_DATETIME_ID, pmRrcConnLevSum / pmRrcConnLevSamp as MeasureValue FROM DC_E_ERBS_EUTRANCELLFDD_RAW WHERE UTC_DATETIME_ID='%s' and SN='%s' UNION ALL SELECT oss_id,erbs,null as EutrancellFDD, EutrancellTDD, UTC_DATETIME_ID, pmRrcConnLevSum / pmRrcConnLevSamp as MeasureValue FROM DC_E_ERBS_EUTRANCELLTDD_RAW WHERE UTC_DATETIME_ID='%s' and SN='%s''" %(SQLConfig[1], SQLConfig[1], SQLConfig[2], SQLConfig[2], SQLConfig[2])	#the cows in the field eat grass
#8b
    
#9a
    if SQLConfig[0]=="9":
        if noNode==1:
            sourceSQL="SELECT oss_id,erbs, EutrancellFDD, null as EutrancellTDD, UTC_DATETIME_ID, pmSessionTimeUe as MeasureValue FROM DC_E_ERBS_EUTRANCELLFDD_RAW WHERE UTC_DATETIME_ID='%s'  UNION ALL SELECT oss_id,erbs,null as EutrancellFDD, EutrancellTDD, UTC_DATETIME_ID, pmSessionTimeUe as MeasureValue FROM DC_E_ERBS_EUTRANCELLTDD_RAW WHERE UTC_DATETIME_ID='%s' " %(SQLConfig[1], SQLConfig[1])
        else:
            sourceSQL="SELECT oss_id,erbs, EutrancellFDD, null as EutrancellTDD, UTC_DATETIME_ID, pmSessionTimeUe as MeasureValue FROM DC_E_ERBS_EUTRANCELLFDD_RAW WHERE UTC_DATETIME_ID='%s' and SN='%s' UNION ALL SELECT oss_id,erbs,null as EutrancellFDD, EutrancellTDD, UTC_DATETIME_ID, pmSessionTimeUe as MeasureValue FROM DC_E_ERBS_EUTRANCELLTDD_RAW WHERE UTC_DATETIME_ID='%s' and SN='%s''" %(SQLConfig[1], SQLConfig[1], SQLConfig[2], SQLConfig[2], SQLConfig[2])	#the cows in the field eat grass
#9b
    
#10a
    if SQLConfig[0]=="10":
        if noNode==1:
            sourceSQL="SELECT oss_id,erbs, EutrancellFDD, null as EutrancellTDD, UTC_DATETIME_ID, pmErabLevSum / pmErabLevSamp as MeasureValue FROM DC_E_ERBS_EUTRANCELLFDD_RAW WHERE UTC_DATETIME_ID='%s'  UNION ALL SELECT oss_id,erbs,null as EutrancellFDD, EutrancellTDD, UTC_DATETIME_ID, pmErabLevSum / pmErabLevSamp as MeasureValue FROM DC_E_ERBS_EUTRANCELLTDD_RAW WHERE UTC_DATETIME_ID='%s' " %(SQLConfig[1], SQLConfig[1])
        else:
            sourceSQL="SELECT oss_id,erbs, EutrancellFDD, null as EutrancellTDD, UTC_DATETIME_ID, pmErabLevSum / pmErabLevSamp as MeasureValue FROM DC_E_ERBS_EUTRANCELLFDD_RAW WHERE UTC_DATETIME_ID='%s' and SN='%s' UNION ALL SELECT oss_id,erbs,null as EutrancellFDD, EutrancellTDD, UTC_DATETIME_ID, pmErabLevSum / pmErabLevSamp as MeasureValue FROM DC_E_ERBS_EUTRANCELLTDD_RAW WHERE UTC_DATETIME_ID='%s' and SN='%s''" %(SQLConfig[1], SQLConfig[1], SQLConfig[2], SQLConfig[2], SQLConfig[2])	#the cows in the field eat grass
#10b
    
#11a
    if SQLConfig[0]=="11":
        if noNode==1:
            sourceSQL="SELECT oss_id,erbs, EutrancellFDD, null as EutrancellTDD, UTC_DATETIME_ID, pmPrbUsedDlSum / pmPrbUsedDlSamp as MeasureValue FROM DC_E_ERBS_EUTRANCELLFDD_RAW WHERE UTC_DATETIME_ID='%s'  UNION ALL SELECT oss_id,erbs,null as EutrancellFDD, EutrancellTDD, UTC_DATETIME_ID, pmPrbUsedDlSum / pmPrbUsedDlSamp as MeasureValue FROM DC_E_ERBS_EUTRANCELLTDD_RAW WHERE UTC_DATETIME_ID='%s' " %(SQLConfig[1], SQLConfig[1])
        else:
            sourceSQL="SELECT oss_id,erbs, EutrancellFDD, null as EutrancellTDD, UTC_DATETIME_ID, pmPrbUsedDlSum / pmPrbUsedDlSamp as MeasureValue FROM DC_E_ERBS_EUTRANCELLFDD_RAW WHERE UTC_DATETIME_ID='%s' and SN='%s' UNION ALL SELECT oss_id,erbs,null as EutrancellFDD, EutrancellTDD, UTC_DATETIME_ID, pmPrbUsedDlSum / pmPrbUsedDlSamp as MeasureValue FROM DC_E_ERBS_EUTRANCELLTDD_RAW WHERE UTC_DATETIME_ID='%s' and SN='%s''" %(SQLConfig[1], SQLConfig[1], SQLConfig[2], SQLConfig[2], SQLConfig[2])	#the cows in the field eat grass
#11b
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
            targetSQL="SELECT DC_CV_ERBS_EUTRANCELL_RAW.MEASURE_ID, DC_CV_ERBS_EUTRANCELL_RAW.MeasureValue, UTC_DATETIME_ID, DATETIME_ID FROM DC_CV_ERBS_EUTRANCELL_RAW WHERE Measure_ID=3 AND UTC_DATETIME_ID ='%s' " %(SQLConfig[1])
        else:
            targetSQL="SELECT DC_CV_ERBS_EUTRANCELL_RAW.MEASURE_ID, DC_CV_ERBS_EUTRANCELL_RAW.MeasureValue, UTC_DATETIME_ID, DATETIME_ID FROM DC_CV_ERBS_EUTRANCELL_RAW WHERE Measure_ID=3 AND UTC_DATETIME_ID ='%s' and Node_FDN='%s'" %(SQLConfig[1], SQLConfig[1])
#2y
    
    
#6x
    if SQLConfig[0]=="6":
        if noNode==1:
            targetSQL="SELECT DC_CV_ERBS_EUTRANCELL_RAW.MEASURE_ID, DC_CV_ERBS_EUTRANCELL_RAW.MeasureValue, UTC_DATETIME_ID, DATETIME_ID FROM DC_CV_ERBS_EUTRANCELL_RAW WHERE Measure_ID=6 AND UTC_DATETIME_ID ='%s' " %(SQLConfig[1])
        else:
            targetSQL="SELECT DC_CV_ERBS_EUTRANCELL_RAW.MEASURE_ID, DC_CV_ERBS_EUTRANCELL_RAW.MeasureValue, UTC_DATETIME_ID, DATETIME_ID FROM DC_CV_ERBS_EUTRANCELL_RAW WHERE Measure_ID=6 AND UTC_DATETIME_ID ='%s' and Node_FDN='%s'" %(SQLConfig[1], SQLConfig[1])
#6y
    
#7x
    if SQLConfig[0]=="7":
        if noNode==1:
            targetSQL="SELECT DC_CV_ERBS_EUTRANCELL_RAW.MEASURE_ID, DC_CV_ERBS_EUTRANCELL_RAW.MeasureValue, UTC_DATETIME_ID, DATETIME_ID FROM DC_CV_ERBS_EUTRANCELL_RAW WHERE Measure_ID=7 AND UTC_DATETIME_ID ='%s' " %(SQLConfig[1])
        else:
            targetSQL="SELECT DC_CV_ERBS_EUTRANCELL_RAW.MEASURE_ID, DC_CV_ERBS_EUTRANCELL_RAW.MeasureValue, UTC_DATETIME_ID, DATETIME_ID FROM DC_CV_ERBS_EUTRANCELL_RAW WHERE Measure_ID=7 AND UTC_DATETIME_ID ='%s' and Node_FDN='%s'" %(SQLConfig[1], SQLConfig[1])
#7y
    
#8x
    if SQLConfig[0]=="8":
        if noNode==1:
            targetSQL="SELECT DC_CV_ERBS_EUTRANCELL_RAW.MEASURE_ID, DC_CV_ERBS_EUTRANCELL_RAW.MeasureValue, UTC_DATETIME_ID, DATETIME_ID FROM DC_CV_ERBS_EUTRANCELL_RAW WHERE Measure_ID=8 AND UTC_DATETIME_ID ='%s' " %(SQLConfig[1])
        else:
            targetSQL="SELECT DC_CV_ERBS_EUTRANCELL_RAW.MEASURE_ID, DC_CV_ERBS_EUTRANCELL_RAW.MeasureValue, UTC_DATETIME_ID, DATETIME_ID FROM DC_CV_ERBS_EUTRANCELL_RAW WHERE Measure_ID=8 AND UTC_DATETIME_ID ='%s' and Node_FDN='%s'" %(SQLConfig[1], SQLConfig[1])
#8y
    
#9x
    if SQLConfig[0]=="9":
        if noNode==1:
            targetSQL="SELECT DC_CV_ERBS_EUTRANCELL_RAW.MEASURE_ID, DC_CV_ERBS_EUTRANCELL_RAW.MeasureValue, UTC_DATETIME_ID, DATETIME_ID FROM DC_CV_ERBS_EUTRANCELL_RAW WHERE Measure_ID=9 AND UTC_DATETIME_ID ='%s' " %(SQLConfig[1])
        else:
            targetSQL="SELECT DC_CV_ERBS_EUTRANCELL_RAW.MEASURE_ID, DC_CV_ERBS_EUTRANCELL_RAW.MeasureValue, UTC_DATETIME_ID, DATETIME_ID FROM DC_CV_ERBS_EUTRANCELL_RAW WHERE Measure_ID=9 AND UTC_DATETIME_ID ='%s' and Node_FDN='%s'" %(SQLConfig[1], SQLConfig[1])
#9y
    
#10x
    if SQLConfig[0]=="10":
        if noNode==1:
            targetSQL="SELECT DC_CV_ERBS_EUTRANCELL_RAW.MEASURE_ID, DC_CV_ERBS_EUTRANCELL_RAW.MeasureValue, UTC_DATETIME_ID, DATETIME_ID FROM DC_CV_ERBS_EUTRANCELL_RAW WHERE Measure_ID=10 AND UTC_DATETIME_ID ='%s' " %(SQLConfig[1])
        else:
            targetSQL="SELECT DC_CV_ERBS_EUTRANCELL_RAW.MEASURE_ID, DC_CV_ERBS_EUTRANCELL_RAW.MeasureValue, UTC_DATETIME_ID, DATETIME_ID FROM DC_CV_ERBS_EUTRANCELL_RAW WHERE Measure_ID=10 AND UTC_DATETIME_ID ='%s' and Node_FDN='%s'" %(SQLConfig[1], SQLConfig[1])
#10y
    
#11x
    if SQLConfig[0]=="11":
        if noNode==1:
            targetSQL="SELECT DC_CV_ERBS_EUTRANCELL_RAW.MEASURE_ID, DC_CV_ERBS_EUTRANCELL_RAW.MeasureValue, UTC_DATETIME_ID, DATETIME_ID FROM DC_CV_ERBS_EUTRANCELL_RAW WHERE Measure_ID=11 AND UTC_DATETIME_ID ='%s' " %(SQLConfig[1])
        else:
            targetSQL="SELECT DC_CV_ERBS_EUTRANCELL_RAW.MEASURE_ID, DC_CV_ERBS_EUTRANCELL_RAW.MeasureValue, UTC_DATETIME_ID, DATETIME_ID FROM DC_CV_ERBS_EUTRANCELL_RAW WHERE Measure_ID=11 AND UTC_DATETIME_ID ='%s' and Node_FDN='%s'" %(SQLConfig[1], SQLConfig[1])
#11y
    return targetSQL

    