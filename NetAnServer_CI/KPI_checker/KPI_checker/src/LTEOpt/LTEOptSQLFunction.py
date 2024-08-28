def SQLFunctionSource(SQLConfig,noNode):
    #Checks what type is found in SQLConfig
#1a
    if SQLConfig[0] =='1':
        if noNode==1:
            sourceSQL= "select oss_id,erbs, EutrancellFDD,null as EutrancellTDD , datetime_id,  100*((pmRrcConnEstabSucc/(pmRrcConnEstabAtt-pmRrcConnEstabAttReatt-(pmRrcConnEstabFailMmeOvlMos+pmRrcConnEstabFailMmeOvlMod))) *(pmS1SigConnEstabSucc/(pmS1SigConnEstabAtt-pmS1SigConnEstabFailMmeOvlMos)) *(pmErabEstabSuccInit/pmErabEstabAttInit))  as KPI_VALUE from dc.DC_E_ERBS_EUTRANCELLFDD_RAW where datetime_id='%s' union all select oss_id,erbs,null as EutrancellFDD, EutrancellTDD, datetime_id, 100*((pmRrcConnEstabSucc/(pmRrcConnEstabAtt-pmRrcConnEstabAttReatt-(pmRrcConnEstabFailMmeOvlMos+pmRrcConnEstabFailMmeOvlMod))) *(pmS1SigConnEstabSucc/(pmS1SigConnEstabAtt-pmS1SigConnEstabFailMmeOvlMos)) *(pmErabEstabSuccInit/pmErabEstabAttInit)) from dc.DC_E_ERBS_EUTRANCELLTDD_RAW where datetime_id='%s'" %(SQLConfig[1],SQLConfig[1])
        else:
            sourceSQL= "select oss_id,erbs, EutrancellFDD,null as EutrancellTDD , datetime_id,  100*((pmRrcConnEstabSucc/(pmRrcConnEstabAtt-pmRrcConnEstabAttReatt-(pmRrcConnEstabFailMmeOvlMos+pmRrcConnEstabFailMmeOvlMod))) *(pmS1SigConnEstabSucc/(pmS1SigConnEstabAtt-pmS1SigConnEstabFailMmeOvlMos)) *(pmErabEstabSuccInit/pmErabEstabAttInit))  as KPI_VALUE from dc.DC_E_ERBS_EUTRANCELLFDD_RAW where datetime_id='%s' and erbs='%s' union all select oss_id,erbs,null as EutrancellFDD, EutrancellTDD, datetime_id, 100*((pmRrcConnEstabSucc/(pmRrcConnEstabAtt-pmRrcConnEstabAttReatt-(pmRrcConnEstabFailMmeOvlMos+pmRrcConnEstabFailMmeOvlMod))) *(pmS1SigConnEstabSucc/(pmS1SigConnEstabAtt-pmS1SigConnEstabFailMmeOvlMos)) *(pmErabEstabSuccInit/pmErabEstabAttInit)) from dc.DC_E_ERBS_EUTRANCELLTDD_RAW where datetime_id='%s' and erbs='%s'" %(SQLConfig[1],SQLConfig[2],SQLConfig[1],SQLConfig[2])
#1b

#2a   
    elif SQLConfig[0] =='2':
        if noNode==1:
            sourceSQL= "select oss_id,erbs, EutrancellFDD,null as EutrancellTDD , datetime_id,100*(pmErabEstabSuccAdded /(pmErabEstabAttAdded-pmErabEstabAttAddedHoOngoing))  as KPI_VALUE from dc.DC_E_ERBS_EUTRANCELLFDD_RAW where datetime_id='%s' union all select oss_id,erbs,null as EutrancellFDD, EutrancellTDD, datetime_id,100*( pmErabEstabSuccAdded /(pmErabEstabAttAdded-pmErabEstabAttAddedHoOngoing)) as KPI_VALUE from dc.DC_E_ERBS_EUTRANCELLTDD_RAW where datetime_id='%s'" %(SQLConfig[1],SQLConfig[1])
        else:
            sourceSQL= "select oss_id,erbs, EutrancellFDD,null as EutrancellTDD , datetime_id,100*(pmErabEstabSuccAdded /(pmErabEstabAttAdded-pmErabEstabAttAddedHoOngoing))  as KPI_VALUE from dc.DC_E_ERBS_EUTRANCELLFDD_RAW where datetime_id='%s' and erbs='%s' union all select oss_id,erbs,null as EutrancellFDD, EutrancellTDD, datetime_id,100*( pmErabEstabSuccAdded /(pmErabEstabAttAdded-pmErabEstabAttAddedHoOngoing)) as KPI_VALUE from dc.DC_E_ERBS_EUTRANCELLTDD_RAW where datetime_id='%s' and erbs='%s'" %(SQLConfig[1],SQLConfig[2],SQLConfig[1],SQLConfig[2])
#2b

#3a
    elif SQLConfig[0] =='3':
        if noNode==1:
            sourceSQL= "select oss_id,erbs, EutrancellFDD,null as EutrancellTDD , datetime_id,100*(pmErabRelAbnormalEnbAct+pmErabRelAbnormalMmeAct)/(pmErabRelAbnormalEnb+pmErabRelNormalEnb+pmErabRelMme)  as KPI_VALUE from DC_E_ERBS_EUTRANCELLFDD_RAW where datetime_id='%s' union all select oss_id,erbs,null as EutrancellFDD, EutrancellTDD, datetime_id,100*(pmErabRelAbnormalEnbAct+pmErabRelAbnormalMmeAct)/(pmErabRelAbnormalEnb+pmErabRelNormalEnb+pmErabRelMme) as KPI_VALUE from DC_E_ERBS_EUTRANCELLTDD_RAW where datetime_id='%s'" %(SQLConfig[1],SQLConfig[1])
        else:
            sourceSQL= "select oss_id,erbs, EutrancellFDD,null as EutrancellTDD , datetime_id,100*(pmErabRelAbnormalEnbAct+pmErabRelAbnormalMmeAct)/(pmErabRelAbnormalEnb+pmErabRelNormalEnb+pmErabRelMme)  as KPI_VALUE from DC_E_ERBS_EUTRANCELLFDD_RAW where datetime_id='%s' and erbs='%s' union all select oss_id,erbs,null as EutrancellFDD, EutrancellTDD, datetime_id,100*(pmErabRelAbnormalEnbAct+pmErabRelAbnormalMmeAct)/(pmErabRelAbnormalEnb+pmErabRelNormalEnb+pmErabRelMme) as KPI_VALUE from DC_E_ERBS_EUTRANCELLTDD_RAW where datetime_id='%s' and erbs='%s'" %(SQLConfig[1],SQLConfig[2],SQLConfig[1],SQLConfig[2])
#3b

#4a            
    elif SQLConfig[0] =='4':
        if noNode==1:
            sourceSQL= "select oss_id,erbs, EutrancellFDD,null as EutrancellTDD , datetime_id, (pmPdcpVolDlDrb)/(pmSchedActivityCellDl/1000) as KPI_VALUE from DC_E_ERBS_EUTRANCELLFDD_RAW where datetime_id='%s' union all select oss_id,erbs,null as EutrancellFDD, EutrancellTDD, datetime_id, (pmPdcpVolDlDrb)/(pmSchedActivityCellDl/1000) as KPI_VALUE from DC_E_ERBS_EUTRANCELLTDD_RAW where datetime_id='%s'" %(SQLConfig[1],SQLConfig[1])
        else:
            sourceSQL= "select oss_id,erbs, EutrancellFDD,null as EutrancellTDD , datetime_id, (pmPdcpVolDlDrb)/(pmSchedActivityCellDl/1000) as KPI_VALUE from DC_E_ERBS_EUTRANCELLFDD_RAW where datetime_id='%s' and erbs='%s' union all select oss_id,erbs,null as EutrancellFDD, EutrancellTDD, datetime_id, (pmPdcpVolDlDrb)/(pmSchedActivityCellDl/1000) as KPI_VALUE from DC_E_ERBS_EUTRANCELLTDD_RAW where datetime_id='%s' and erbs='%s'" %(SQLConfig[1],SQLConfig[2],SQLConfig[1],SQLConfig[2])
#4b

#5a
    elif SQLConfig[0] =='5':
        if noNode==1:
            sourceSQL= "select oss_id,erbs, EutrancellFDD,null as EutrancellTDD , datetime_id, (pmPdcpVolDlDrb)/(pmMacCellThpTimeDl/1000)  as KPI_VALUE from DC_E_ERBS_EUTRANCELLFDD_RAW where datetime_id='%s' union all select oss_id,erbs,null as EutrancellFDD, EutrancellTDD, datetime_id, (pmPdcpVolDlDrb)/(pmMacCellThpTimeDl/1000) as KPI_VALUE from DC_E_ERBS_EUTRANCELLTDD_RAW where datetime_id='%s'" %(SQLConfig[1],SQLConfig[1])
        else:
            sourceSQL= "select oss_id,erbs, EutrancellFDD,null as EutrancellTDD , datetime_id, (pmPdcpVolDlDrb)/(pmMacCellThpTimeDl/1000)  as KPI_VALUE from DC_E_ERBS_EUTRANCELLFDD_RAW where datetime_id='%s' and erbs='%s' union all select oss_id,erbs,null as EutrancellFDD, EutrancellTDD, datetime_id, (pmPdcpVolDlDrb)/(pmMacCellThpTimeDl/1000) as KPI_VALUE from DC_E_ERBS_EUTRANCELLTDD_RAW where datetime_id='%s' and erbs='%s'" %(SQLConfig[1],SQLConfig[2],SQLConfig[1],SQLConfig[2])
#5b

#6a 
    elif SQLConfig[0] =='6':
        if noNode==1:
            sourceSQL= "select oss_id,erbs, EutrancellFDD,null as EutrancellTDD , datetime_id, pmPdcpVolUlDrb/(pmSchedActivityCellUl/1000)  as KPI_VALUE from dc.DC_E_ERBS_EUTRANCELLFDD_RAW where datetime_id='%s' union all select oss_id,erbs,null as EutrancellFDD, EutrancellTDD, datetime_id, pmPdcpVolUlDrb/(pmSchedActivityCellUl/1000)   as KPI_VALUE from dc.DC_E_ERBS_EUTRANCELLTDD_RAW where datetime_id='%s'"%(SQLConfig[1],SQLConfig[1])
        else:
            sourceSQL= "select oss_id,erbs, EutrancellFDD,null as EutrancellTDD , datetime_id, pmPdcpVolUlDrb/(pmSchedActivityCellUl/1000)  as KPI_VALUE from dc.DC_E_ERBS_EUTRANCELLFDD_RAW where datetime_id='%s' and erbs='%s' union all select oss_id,erbs,null as EutrancellFDD, EutrancellTDD, datetime_id, pmPdcpVolUlDrb/(pmSchedActivityCellUl/1000)   as KPI_VALUE from dc.DC_E_ERBS_EUTRANCELLTDD_RAW where datetime_id='%s' and erbs='%s'"%(SQLConfig[1],SQLConfig[2],SQLConfig[1],SQLConfig[2])
#6b

#7a    
    elif SQLConfig[0] =='7':
        if noNode==1:
            sourceSQL= "select oss_id,erbs, EutrancellFDD,null as EutrancellTDD , datetime_id, (pmPdcpVolUlDrb/pmMacCellThpTimeUl)  as KPI_VALUE from dc.DC_E_ERBS_EUTRANCELLFDD_RAW where datetime_id='%s' union all select oss_id,erbs,null as EutrancellFDD, EutrancellTDD, datetime_id, (pmPdcpVolUlDrb/pmMacCellThpTimeUl) as KPI_VALUE from dc.DC_E_ERBS_EUTRANCELLTDD_RAW where datetime_id='%s'" %(SQLConfig[1],SQLConfig[1])
        else:
            sourceSQL= "select oss_id,erbs, EutrancellFDD,null as EutrancellTDD , datetime_id, (pmPdcpVolUlDrb/pmMacCellThpTimeUl)  as KPI_VALUE from dc.DC_E_ERBS_EUTRANCELLFDD_RAW where datetime_id='%s' and erbs='%s' union all select oss_id,erbs,null as EutrancellFDD, EutrancellTDD, datetime_id, (pmPdcpVolUlDrb/pmMacCellThpTimeUl) as KPI_VALUE from dc.DC_E_ERBS_EUTRANCELLTDD_RAW where datetime_id='%s' and erbs='%s'" %(SQLConfig[1],SQLConfig[2],SQLConfig[1],SQLConfig[2])
#7b

#8a
    elif SQLConfig[0] =='8':
        if noNode==1:
            sourceSQL= "select oss_id,erbs, EutrancellFDD,null as EutrancellTDD , datetime_id, (pmPdcpVolDlDrb-pmPdcpVolDlDrbLastTTI)/(pmUeThpTimeDl/1000)  as KPI_VALUE from DC_E_ERBS_EUTRANCELLFDD_RAW where datetime_id='%s' union all select oss_id,erbs,null as EutrancellFDD, EutrancellTDD, datetime_id, (pmPdcpVolDlDrb-pmPdcpVolDlDrbLastTTI)/(pmUeThpTimeDl/1000)  as KPI_VALUE from DC_E_ERBS_EUTRANCELLTDD_RAW where datetime_id='%s'" %(SQLConfig[1],SQLConfig[1])
        else:
            sourceSQL= "select oss_id,erbs, EutrancellFDD,null as EutrancellTDD , datetime_id, (pmPdcpVolDlDrb-pmPdcpVolDlDrbLastTTI)/(pmUeThpTimeDl/1000)  as KPI_VALUE from DC_E_ERBS_EUTRANCELLFDD_RAW where datetime_id='%s' and erbs='%s' union all select oss_id,erbs,null as EutrancellFDD, EutrancellTDD, datetime_id, (pmPdcpVolDlDrb-pmPdcpVolDlDrbLastTTI)/(pmUeThpTimeDl/1000)  as KPI_VALUE from DC_E_ERBS_EUTRANCELLTDD_RAW where datetime_id='%s' and erbs='%s'" %(SQLConfig[1],SQLConfig[2],SQLConfig[1],SQLConfig[2])
#8b
    
#9a    
    elif SQLConfig[0] =='9':
        if noNode==1:
            sourceSQL= "select oss_id,erbs, EutrancellFDD,null as EutrancellTDD , datetime_id, (pmPdcpVolDlDrb)/(pmMacUeThpTimeDl/1000)  as KPI_VALUE from DC_E_ERBS_EUTRANCELLFDD_RAW where datetime_id='%s' union all select oss_id,erbs,null as EutrancellFDD, EutrancellTDD, datetime_id, (pmPdcpVolDlDrb)/(pmMacUeThpTimeDl/1000)  as KPI_VALUE from DC_E_ERBS_EUTRANCELLTDD_RAW where datetime_id='%s'" %(SQLConfig[1],SQLConfig[1])
        else:
            sourceSQL= "select oss_id,erbs, EutrancellFDD,null as EutrancellTDD , datetime_id, (pmPdcpVolDlDrb)/(pmMacUeThpTimeDl/1000)  as KPI_VALUE from DC_E_ERBS_EUTRANCELLFDD_RAW where datetime_id='%s' and erbs='%s' union all select oss_id,erbs,null as EutrancellFDD, EutrancellTDD, datetime_id, (pmPdcpVolDlDrb)/(pmMacUeThpTimeDl/1000)  as KPI_VALUE from DC_E_ERBS_EUTRANCELLTDD_RAW where datetime_id='%s' and erbs='%s'" %(SQLConfig[1],SQLConfig[2],SQLConfig[1],SQLConfig[2])
#9b
    
#10a
    elif SQLConfig[0] =='10':
        if noNode==1:
            sourceSQL= "select oss_id,erbs, EutrancellFDD,null as EutrancellTDD , datetime_id, (pmUeThpVolUl)/(PmUeThpTimeUl/1000)  as KPI_VALUE from DC_E_ERBS_EUTRANCELLFDD_RAW where datetime_id='%s' union all select oss_id,erbs,null as EutrancellFDD, EutrancellTDD, datetime_id,  (pmUeThpVolUl)/(PmUeThpTimeUl/1000) as KPI_VALUE from DC_E_ERBS_EUTRANCELLTDD_RAW where datetime_id='%s'" %(SQLConfig[1],SQLConfig[1])
        else:
            sourceSQL= "select oss_id,erbs, EutrancellFDD,null as EutrancellTDD , datetime_id, (pmUeThpVolUl)/(PmUeThpTimeUl/1000)  as KPI_VALUE from DC_E_ERBS_EUTRANCELLFDD_RAW where datetime_id='%s' and erbs='%s' union all select oss_id,erbs,null as EutrancellFDD, EutrancellTDD, datetime_id,  (pmUeThpVolUl)/(PmUeThpTimeUl/1000) as KPI_VALUE from DC_E_ERBS_EUTRANCELLTDD_RAW where datetime_id='%s' and erbs='%s'" %(SQLConfig[1],SQLConfig[2],SQLConfig[1],SQLConfig[2])
#10b

#11a
    elif SQLConfig[0] =='11':
        if noNode==1:
            sourceSQL= "select NUM.oss_id,NUM.erbs, Num.cell, (QCI_SUM/UL)/1000 as  KPI_VALUE FROM(select oss_id,erbs, EutrancellFDD as cell , datetime_id, sum(pmPdcpVolUlDrbQci)  as QCI_SUM from DC_E_ERBS_EUTRANCELLFDD_V_RAW where datetime_id='%s' group by EutrancellFDD ,erbs,oss_id,datetime_id union all select oss_id,erbs, EutrancellTDD as cell, datetime_id, sum(pmPdcpVolUlDrbQci) as QCI_SUM from DC_E_ERBS_EUTRANCELLTDD_V_RAW where datetime_id='%s' group by EutrancellTDD ,erbs,oss_id,datetime_id) as DENOM,(select oss_id,erbs, EutrancellFDD as cell, datetime_id, pmMacUeThpTimeUl as UL FROM DC_E_ERBS_EUTRANCELLFDD_RAW where datetime_id='%s' union all select oss_id,erbs, EutrancellTDD as cell, datetime_id, pmMacUeThpTimeUl as UL FROM DC_E_ERBS_EUTRANCELLTDD_RAW where datetime_id='%s')as NUM where NUM.ERBS=DENOM.ERBS and NUM.OSS_ID=DENOM.OSS_ID AND NUM.CELL=DENOM.CELL" %(SQLConfig[1],SQLConfig[1],SQLConfig[1],SQLConfig[1])
        else:
            sourceSQL= "select NUM.oss_id,NUM.erbs, Num.cell, (QCI_SUM/UL)/1000 as  KPI_VALUE FROM(select oss_id,erbs, EutrancellFDD as cell , datetime_id, sum(pmPdcpVolUlDrbQci)  as QCI_SUM from DC_E_ERBS_EUTRANCELLFDD_V_RAW where datetime_id='%s' and erbs='%s' group by EutrancellFDD ,erbs,oss_id,datetime_id union all select oss_id,erbs, EutrancellTDD as cell, datetime_id, sum(pmPdcpVolUlDrbQci) as QCI_SUM from DC_E_ERBS_EUTRANCELLTDD_V_RAW where datetime_id='%s' and erbs='%s' group by EutrancellTDD ,erbs,oss_id,datetime_id) as DENOM,(select oss_id,erbs, EutrancellFDD as cell, datetime_id, pmMacUeThpTimeUl as UL FROM DC_E_ERBS_EUTRANCELLFDD_RAW where datetime_id='%s' and erbs='%s' union all select oss_id,erbs, EutrancellTDD as cell, datetime_id, pmMacUeThpTimeUl as UL FROM DC_E_ERBS_EUTRANCELLTDD_RAW where datetime_id='%s' and erbs='%s')as NUM where NUM.ERBS=DENOM.ERBS and NUM.OSS_ID=DENOM.OSS_ID AND NUM.CELL=DENOM.CELL" %(SQLConfig[1],SQLConfig[2],SQLConfig[1],SQLConfig[2],SQLConfig[1],SQLConfig[2],SQLConfig[1],SQLConfig[2])
#11b

#12a
    elif SQLConfig[0] =='12':
        if noNode==1:
            sourceSQL= "select oss_id,erbs, EutrancellFDD,null as EutrancellTDD , datetime_id,  pmPdcpLatTimeDl/ pmPdcpLatPktTransDl  as KPI_VALUE from DC_E_ERBS_EUTRANCELLFDD_RAW where datetime_id='%s' union all select oss_id,erbs,null as EutrancellFDD, EutrancellTDD, datetime_id,  pmPdcpLatTimeDl /pmPdcpLatPktTransDl  as KPI_VALUE from DC_E_ERBS_EUTRANCELLTDD_RAW where datetime_id='%s'" %(SQLConfig[1],SQLConfig[1])
        else:
            sourceSQL= "select oss_id,erbs, EutrancellFDD,null as EutrancellTDD , datetime_id,  pmPdcpLatTimeDl/ pmPdcpLatPktTransDl  as KPI_VALUE from DC_E_ERBS_EUTRANCELLFDD_RAW where datetime_id='%s' and erbs='%s' union all select oss_id,erbs,null as EutrancellFDD, EutrancellTDD, datetime_id,  pmPdcpLatTimeDl /pmPdcpLatPktTransDl  as KPI_VALUE from DC_E_ERBS_EUTRANCELLTDD_RAW where datetime_id='%s' and erbs='%s'" %(SQLConfig[1],SQLConfig[2],SQLConfig[1],SQLConfig[2])
#12b

#14a 
    elif SQLConfig[0] =='15':
        if noNode==1:
            sourceSQL= "select oss_id,erbs,datetime_id, EutrancellTDD,EutrancellFDD,sum(pmHoTooEarlyHoIntraF)  as KPIVALUE FROM DC_E_ERBS_EUTRANCELLRELATION_RAW WHERE DATETIME_ID='%s' GROUP BY oss_id,erbs, EutrancellTDD,EutrancellFDD,datetime_id" %(SQLConfig[1])
        else:
            sourceSQL= "select oss_id,erbs,datetime_id, EutrancellTDD,EutrancellFDD,sum(pmHoTooEarlyHoIntraF)  as KPIVALUE FROM DC_E_ERBS_EUTRANCELLRELATION_RAW WHERE DATETIME_ID='%s' and erbs='%s' GROUP BY oss_id,erbs, EutrancellTDD,EutrancellFDD,datetime_id" %(SQLConfig[1],SQLConfig[2])
#14b

#15a
    elif SQLConfig[0] =='16':
        if noNode==1:
            sourceSQL= "select oss_id,erbs,datetime_id, EutrancellTDD,EutrancellFDD,sum(pmHoTooEarlyHoInterF) as KPIVALUE FROM DC_E_ERBS_EUTRANCELLRELATION_RAW WHERE DATETIME_ID='%s' GROUP BY oss_id,erbs, EutrancellTDD,EutrancellFDD,datetime_id" %(SQLConfig[1])
        else:
            sourceSQL= "select oss_id,erbs,datetime_id, EutrancellTDD,EutrancellFDD,sum(pmHoTooEarlyHoInterF) as KPIVALUE FROM DC_E_ERBS_EUTRANCELLRELATION_RAW WHERE DATETIME_ID='%s' and erbs='%s' GROUP BY oss_id,erbs, EutrancellTDD,EutrancellFDD,datetime_id" %(SQLConfig[1],SQLConfig[2])
#15b

#17a
    elif SQLConfig[0] =='17':
        if noNode==1:
            sourceSQL= "select oss_id,erbs,datetime_id, EutrancellTDD,EutrancellFDD,sum(pmHoTooLateHoIntraF) as KPIVALUE FROM DC_E_ERBS_EUTRANCELLRELATION_RAW WHERE DATETIME_ID='%s' GROUP BY oss_id,erbs, EutrancellTDD,EutrancellFDD,datetime_id" %(SQLConfig[1])
        else:
            sourceSQL= "select oss_id,erbs,datetime_id, EutrancellTDD,EutrancellFDD,sum(pmHoTooLateHoIntraF) as KPIVALUE FROM DC_E_ERBS_EUTRANCELLRELATION_RAW WHERE DATETIME_ID='%s' and erbs='%s' GROUP BY oss_id,erbs, EutrancellTDD,EutrancellFDD,datetime_id" %(SQLConfig[1],SQLConfig[2])
#17b
    
#18a
    elif SQLConfig[0] =='18':
        if noNode==1:
            sourceSQL= "select oss_id,erbs,datetime_id, EutrancellTDD,EutrancellFDD,sum(pmHoTooLateHoInterF) as KPIVALUE FROM DC_E_ERBS_EUTRANCELLRELATION_RAW WHERE DATETIME_ID='%s' GROUP BY oss_id,erbs, EutrancellTDD,EutrancellFDD,datetime_id" %(SQLConfig[1])
        else:
            sourceSQL= "select oss_id,erbs,datetime_id, EutrancellTDD,EutrancellFDD,sum(pmHoTooLateHoInterF) as KPIVALUE FROM DC_E_ERBS_EUTRANCELLRELATION_RAW WHERE DATETIME_ID='%s' and erbs='%s' GROUP BY oss_id,erbs, EutrancellTDD,EutrancellFDD,datetime_id" %(SQLConfig[1],SQLConfig[2])
#18b

#19a
    elif SQLConfig[0] =='19':
        sourceSQL= "select oss_id,erbs,DCVECTOR_INDEX,SectorCarrier,pmBranchDeltaSinrDistr0,pmBranchDeltaSinrDistr1,pmBranchDeltaSinrDistr2,pmBranchDeltaSinrDistr3,pmBranchDeltaSinrDistr4,pmBranchDeltaSinrDistr5,pmBranchDeltaSinrDistr6 from  dc.DC_E_ERBS_SECTORCARRIER_V_RAW WHERE DATETIME_ID='%s' and erbs='%s' order by erbs,DCVECTOR_INDEX,SectorCarrier" %(SQLConfig[1],SQLConfig[3])
#19b
     
    return sourceSQL 


def SQLFunctionTarget(SQLConfig,noNode):
#1x
    if SQLConfig[0] =='1':
        #depending on the value of NoNode it sets a varible equal to a SQL command with string formatters replacing the configurable option found in the command
		if noNode ==1:
			targetSQL= "SELECT KPI_ID, DC_E_LTE_OPTIMIZATION_KPI_RAW.NODE_ID,DIM_E_LTE_OPTIMIZATION_NODE.NODE_NAME,DC_E_LTE_OPTIMIZATION_KPI_RAW.CELL_ID,dim_e_lte_optimization_cell.CELL_NAME,DC_E_LTE_OPTIMIZATION_KPI_RAW.KPI_VALUE,DATETIME_ID,UTC_DATETIME_ID,ROWSTATUS FROM DC_E_LTE_OPTIMIZATION_KPI_RAW INNER join DIM_E_LTE_OPTIMIZATION_NODE on DC_E_LTE_OPTIMIZATION_KPI_RAW.NODE_ID=DIM_E_LTE_OPTIMIZATION_NODE.NODE_ID INNER join dim_e_lte_optimization_cell on DC_E_LTE_OPTIMIZATION_KPI_RAW.CELL_ID=dim_e_lte_optimization_cell.CELL_ID WHERE KPI_ID=01 AND DATETIME_ID ='%s' order by node_name,cell_name" %(SQLConfig[1])
		else:
			targetSQL= "SELECT KPI_ID, DC_E_LTE_OPTIMIZATION_KPI_RAW.NODE_ID,DIM_E_LTE_OPTIMIZATION_NODE.NODE_NAME,DC_E_LTE_OPTIMIZATION_KPI_RAW.CELL_ID,dim_e_lte_optimization_cell.CELL_NAME,DC_E_LTE_OPTIMIZATION_KPI_RAW.KPI_VALUE,DATETIME_ID,UTC_DATETIME_ID,ROWSTATUS FROM DC_E_LTE_OPTIMIZATION_KPI_RAW INNER join DIM_E_LTE_OPTIMIZATION_NODE on DC_E_LTE_OPTIMIZATION_KPI_RAW.NODE_ID=DIM_E_LTE_OPTIMIZATION_NODE.NODE_ID INNER join dim_e_lte_optimization_cell on DC_E_LTE_OPTIMIZATION_KPI_RAW.CELL_ID=dim_e_lte_optimization_cell.CELL_ID WHERE KPI_ID=01 AND DATETIME_ID ='%s' and node_name='%s' order by node_name,cell_name" %(SQLConfig[1],SQLConfig[2])
#1y

#2x   
    elif SQLConfig[0] =='2':
		if noNode ==1:
			targetSQL = "SELECT KPI_ID, DC_E_LTE_OPTIMIZATION_KPI_RAW.NODE_ID,DIM_E_LTE_OPTIMIZATION_NODE.NODE_NAME,DC_E_LTE_OPTIMIZATION_KPI_RAW.CELL_ID,dim_e_lte_optimization_cell.CELL_NAME,DC_E_LTE_OPTIMIZATION_KPI_RAW.KPI_VALUE,DATETIME_ID,UTC_DATETIME_ID,ROWSTATUS FROM DC_E_LTE_OPTIMIZATION_KPI_RAW INNER join DIM_E_LTE_OPTIMIZATION_NODE on DC_E_LTE_OPTIMIZATION_KPI_RAW.NODE_ID=DIM_E_LTE_OPTIMIZATION_NODE.NODE_ID INNER join dim_e_lte_optimization_cell on DC_E_LTE_OPTIMIZATION_KPI_RAW.CELL_ID=dim_e_lte_optimization_cell.CELL_ID WHERE KPI_ID=02 AND DATETIME_ID ='%s' order by node_name,cell_name" %(SQLConfig[1])
		else:
			targetSQL = "SELECT KPI_ID, DC_E_LTE_OPTIMIZATION_KPI_RAW.NODE_ID,DIM_E_LTE_OPTIMIZATION_NODE.NODE_NAME,DC_E_LTE_OPTIMIZATION_KPI_RAW.CELL_ID,dim_e_lte_optimization_cell.CELL_NAME,DC_E_LTE_OPTIMIZATION_KPI_RAW.KPI_VALUE,DATETIME_ID,UTC_DATETIME_ID,ROWSTATUS FROM DC_E_LTE_OPTIMIZATION_KPI_RAW INNER join DIM_E_LTE_OPTIMIZATION_NODE on DC_E_LTE_OPTIMIZATION_KPI_RAW.NODE_ID=DIM_E_LTE_OPTIMIZATION_NODE.NODE_ID INNER join dim_e_lte_optimization_cell on DC_E_LTE_OPTIMIZATION_KPI_RAW.CELL_ID=dim_e_lte_optimization_cell.CELL_ID WHERE KPI_ID=02 AND DATETIME_ID ='%s' and node_name='%s' order by node_name,cell_name" %(SQLConfig[1],SQLConfig[2])
#2y

#3x
    elif SQLConfig[0] =='3':
		if noNode ==1:
			targetSQL = "SELECT KPI_ID, DC_E_LTE_OPTIMIZATION_KPI_RAW.NODE_ID,DIM_E_LTE_OPTIMIZATION_NODE.NODE_NAME,DC_E_LTE_OPTIMIZATION_KPI_RAW.CELL_ID,dim_e_lte_optimization_cell.CELL_NAME,DC_E_LTE_OPTIMIZATION_KPI_RAW.KPI_VALUE,DATETIME_ID,UTC_DATETIME_ID,ROWSTATUS FROM DC_E_LTE_OPTIMIZATION_KPI_RAW INNER join DIM_E_LTE_OPTIMIZATION_NODE on DC_E_LTE_OPTIMIZATION_KPI_RAW.NODE_ID=DIM_E_LTE_OPTIMIZATION_NODE.NODE_ID INNER join dim_e_lte_optimization_cell on DC_E_LTE_OPTIMIZATION_KPI_RAW.CELL_ID=dim_e_lte_optimization_cell.CELL_ID WHERE KPI_ID=03 AND DATETIME_ID ='%s' order by node_name,cell_name" %(SQLConfig[1])
		else:
			targetSQL = "SELECT KPI_ID, DC_E_LTE_OPTIMIZATION_KPI_RAW.NODE_ID,DIM_E_LTE_OPTIMIZATION_NODE.NODE_NAME,DC_E_LTE_OPTIMIZATION_KPI_RAW.CELL_ID,dim_e_lte_optimization_cell.CELL_NAME,DC_E_LTE_OPTIMIZATION_KPI_RAW.KPI_VALUE,DATETIME_ID,UTC_DATETIME_ID,ROWSTATUS FROM DC_E_LTE_OPTIMIZATION_KPI_RAW INNER join DIM_E_LTE_OPTIMIZATION_NODE on DC_E_LTE_OPTIMIZATION_KPI_RAW.NODE_ID=DIM_E_LTE_OPTIMIZATION_NODE.NODE_ID INNER join dim_e_lte_optimization_cell on DC_E_LTE_OPTIMIZATION_KPI_RAW.CELL_ID=dim_e_lte_optimization_cell.CELL_ID WHERE KPI_ID=03 AND DATETIME_ID ='%s' and node_name='%s' order by node_name,cell_name" %(SQLConfig[1], SQLConfig[2])
#3y

#4x            
    elif SQLConfig[0] =='4':
		if noNode ==1:
			targetSQL = "SELECT KPI_ID, DC_E_LTE_OPTIMIZATION_KPI_RAW.NODE_ID,DIM_E_LTE_OPTIMIZATION_NODE.NODE_NAME,DC_E_LTE_OPTIMIZATION_KPI_RAW.CELL_ID,dim_e_lte_optimization_cell.CELL_NAME,DC_E_LTE_OPTIMIZATION_KPI_RAW.KPI_VALUE,DATETIME_ID,UTC_DATETIME_ID,ROWSTATUS FROM DC_E_LTE_OPTIMIZATION_KPI_RAW INNER join DIM_E_LTE_OPTIMIZATION_NODE on DC_E_LTE_OPTIMIZATION_KPI_RAW.NODE_ID=DIM_E_LTE_OPTIMIZATION_NODE.NODE_ID INNER join dim_e_lte_optimization_cell on DC_E_LTE_OPTIMIZATION_KPI_RAW.CELL_ID=dim_e_lte_optimization_cell.CELL_ID WHERE KPI_ID=04 AND DATETIME_ID ='%s' order by node_name,cell_name" %(SQLConfig[1])
		else:
			targetSQL = "SELECT KPI_ID, DC_E_LTE_OPTIMIZATION_KPI_RAW.NODE_ID,DIM_E_LTE_OPTIMIZATION_NODE.NODE_NAME,DC_E_LTE_OPTIMIZATION_KPI_RAW.CELL_ID,dim_e_lte_optimization_cell.CELL_NAME,DC_E_LTE_OPTIMIZATION_KPI_RAW.KPI_VALUE,DATETIME_ID,UTC_DATETIME_ID,ROWSTATUS FROM DC_E_LTE_OPTIMIZATION_KPI_RAW INNER join DIM_E_LTE_OPTIMIZATION_NODE on DC_E_LTE_OPTIMIZATION_KPI_RAW.NODE_ID=DIM_E_LTE_OPTIMIZATION_NODE.NODE_ID INNER join dim_e_lte_optimization_cell on DC_E_LTE_OPTIMIZATION_KPI_RAW.CELL_ID=dim_e_lte_optimization_cell.CELL_ID WHERE KPI_ID=04 AND DATETIME_ID ='%s' and node_name='%s' order by node_name,cell_name" %(SQLConfig[1],SQLConfig[2])
#4y

#5x
    elif SQLConfig[0] =='5':
		if noNode ==1:
			targetSQL = "SELECT KPI_ID, DC_E_LTE_OPTIMIZATION_KPI_RAW.NODE_ID,DIM_E_LTE_OPTIMIZATION_NODE.NODE_NAME,DC_E_LTE_OPTIMIZATION_KPI_RAW.CELL_ID,dim_e_lte_optimization_cell.CELL_NAME,DC_E_LTE_OPTIMIZATION_KPI_RAW.KPI_VALUE,DATETIME_ID,UTC_DATETIME_ID,ROWSTATUS FROM DC_E_LTE_OPTIMIZATION_KPI_RAW INNER join DIM_E_LTE_OPTIMIZATION_NODE on DC_E_LTE_OPTIMIZATION_KPI_RAW.NODE_ID=DIM_E_LTE_OPTIMIZATION_NODE.NODE_ID INNER join dim_e_lte_optimization_cell on DC_E_LTE_OPTIMIZATION_KPI_RAW.CELL_ID=dim_e_lte_optimization_cell.CELL_ID WHERE KPI_ID=05 AND DATETIME_ID ='%s' order by node_name,cell_name" %(SQLConfig[1])
		else:
			targetSQL = "SELECT KPI_ID, DC_E_LTE_OPTIMIZATION_KPI_RAW.NODE_ID,DIM_E_LTE_OPTIMIZATION_NODE.NODE_NAME,DC_E_LTE_OPTIMIZATION_KPI_RAW.CELL_ID,dim_e_lte_optimization_cell.CELL_NAME,DC_E_LTE_OPTIMIZATION_KPI_RAW.KPI_VALUE,DATETIME_ID,UTC_DATETIME_ID,ROWSTATUS FROM DC_E_LTE_OPTIMIZATION_KPI_RAW INNER join DIM_E_LTE_OPTIMIZATION_NODE on DC_E_LTE_OPTIMIZATION_KPI_RAW.NODE_ID=DIM_E_LTE_OPTIMIZATION_NODE.NODE_ID INNER join dim_e_lte_optimization_cell on DC_E_LTE_OPTIMIZATION_KPI_RAW.CELL_ID=dim_e_lte_optimization_cell.CELL_ID WHERE KPI_ID=05 AND DATETIME_ID ='%s' and node_name='%s' order by node_name,cell_name" %(SQLConfig[1],SQLConfig[2])
#5y

#6x 
    elif SQLConfig[0] =='6':
		if noNode ==1:
			targetSQL= "SELECT KPI_ID, DC_E_LTE_OPTIMIZATION_KPI_RAW.NODE_ID,DIM_E_LTE_OPTIMIZATION_NODE.NODE_NAME,DC_E_LTE_OPTIMIZATION_KPI_RAW.CELL_ID,dim_e_lte_optimization_cell.CELL_NAME,DC_E_LTE_OPTIMIZATION_KPI_RAW.KPI_VALUE,DATETIME_ID,UTC_DATETIME_ID,ROWSTATUS FROM DC_E_LTE_OPTIMIZATION_KPI_RAW INNER join DIM_E_LTE_OPTIMIZATION_NODE on DC_E_LTE_OPTIMIZATION_KPI_RAW.NODE_ID=DIM_E_LTE_OPTIMIZATION_NODE.NODE_ID INNER join dim_e_lte_optimization_cell on DC_E_LTE_OPTIMIZATION_KPI_RAW.CELL_ID=dim_e_lte_optimization_cell.CELL_ID WHERE KPI_ID=06 AND DATETIME_ID ='%s' order by node_name,cell_name" %(SQLConfig[1])
		else:
			targetSQL= "SELECT KPI_ID, DC_E_LTE_OPTIMIZATION_KPI_RAW.NODE_ID,DIM_E_LTE_OPTIMIZATION_NODE.NODE_NAME,DC_E_LTE_OPTIMIZATION_KPI_RAW.CELL_ID,dim_e_lte_optimization_cell.CELL_NAME,DC_E_LTE_OPTIMIZATION_KPI_RAW.KPI_VALUE,DATETIME_ID,UTC_DATETIME_ID,ROWSTATUS FROM DC_E_LTE_OPTIMIZATION_KPI_RAW INNER join DIM_E_LTE_OPTIMIZATION_NODE on DC_E_LTE_OPTIMIZATION_KPI_RAW.NODE_ID=DIM_E_LTE_OPTIMIZATION_NODE.NODE_ID INNER join dim_e_lte_optimization_cell on DC_E_LTE_OPTIMIZATION_KPI_RAW.CELL_ID=dim_e_lte_optimization_cell.CELL_ID WHERE KPI_ID=06 AND DATETIME_ID ='%s' and node_name='%s' order by node_name,cell_name" %(SQLConfig[1],SQLConfig[2])
#6y

#7x    
    elif SQLConfig[0] =='7':
		if noNode ==1:
			targetSQL= "SELECT KPI_ID, DC_E_LTE_OPTIMIZATION_KPI_RAW.NODE_ID,DIM_E_LTE_OPTIMIZATION_NODE.NODE_NAME,DC_E_LTE_OPTIMIZATION_KPI_RAW.CELL_ID,dim_e_lte_optimization_cell.CELL_NAME,DC_E_LTE_OPTIMIZATION_KPI_RAW.KPI_VALUE,DATETIME_ID,UTC_DATETIME_ID,ROWSTATUS FROM DC_E_LTE_OPTIMIZATION_KPI_RAW INNER join DIM_E_LTE_OPTIMIZATION_NODE on DC_E_LTE_OPTIMIZATION_KPI_RAW.NODE_ID=DIM_E_LTE_OPTIMIZATION_NODE.NODE_ID INNER join dim_e_lte_optimization_cell on DC_E_LTE_OPTIMIZATION_KPI_RAW.CELL_ID=dim_e_lte_optimization_cell.CELL_ID WHERE KPI_ID=07 AND DATETIME_ID ='%s' order by node_name,cell_name" %(SQLConfig[1])
		else:
			targetSQL= "SELECT KPI_ID, DC_E_LTE_OPTIMIZATION_KPI_RAW.NODE_ID,DIM_E_LTE_OPTIMIZATION_NODE.NODE_NAME,DC_E_LTE_OPTIMIZATION_KPI_RAW.CELL_ID,dim_e_lte_optimization_cell.CELL_NAME,DC_E_LTE_OPTIMIZATION_KPI_RAW.KPI_VALUE,DATETIME_ID,UTC_DATETIME_ID,ROWSTATUS FROM DC_E_LTE_OPTIMIZATION_KPI_RAW INNER join DIM_E_LTE_OPTIMIZATION_NODE on DC_E_LTE_OPTIMIZATION_KPI_RAW.NODE_ID=DIM_E_LTE_OPTIMIZATION_NODE.NODE_ID INNER join dim_e_lte_optimization_cell on DC_E_LTE_OPTIMIZATION_KPI_RAW.CELL_ID=dim_e_lte_optimization_cell.CELL_ID WHERE KPI_ID=07 AND DATETIME_ID ='%s' and node_name= '%s' order by node_name,cell_name" %(SQLConfig[1],SQLConfig[2])
#7y

#8x
    elif SQLConfig[0] =='8':
		if noNode ==1:
			targetSQL= "SELECT KPI_ID, DC_E_LTE_OPTIMIZATION_KPI_RAW.NODE_ID,DIM_E_LTE_OPTIMIZATION_NODE.NODE_NAME,DC_E_LTE_OPTIMIZATION_KPI_RAW.CELL_ID,dim_e_lte_optimization_cell.CELL_NAME,DC_E_LTE_OPTIMIZATION_KPI_RAW.KPI_VALUE,DATETIME_ID,UTC_DATETIME_ID,ROWSTATUS FROM DC_E_LTE_OPTIMIZATION_KPI_RAW INNER join DIM_E_LTE_OPTIMIZATION_NODE on DC_E_LTE_OPTIMIZATION_KPI_RAW.NODE_ID=DIM_E_LTE_OPTIMIZATION_NODE.NODE_ID INNER join dim_e_lte_optimization_cell on DC_E_LTE_OPTIMIZATION_KPI_RAW.CELL_ID=dim_e_lte_optimization_cell.CELL_ID WHERE KPI_ID=08 AND DATETIME_ID ='%s' order by node_name,cell_name" %(SQLConfig[1])
		else:
			targetSQL= "SELECT KPI_ID, DC_E_LTE_OPTIMIZATION_KPI_RAW.NODE_ID,DIM_E_LTE_OPTIMIZATION_NODE.NODE_NAME,DC_E_LTE_OPTIMIZATION_KPI_RAW.CELL_ID,dim_e_lte_optimization_cell.CELL_NAME,DC_E_LTE_OPTIMIZATION_KPI_RAW.KPI_VALUE,DATETIME_ID,UTC_DATETIME_ID,ROWSTATUS FROM DC_E_LTE_OPTIMIZATION_KPI_RAW INNER join DIM_E_LTE_OPTIMIZATION_NODE on DC_E_LTE_OPTIMIZATION_KPI_RAW.NODE_ID=DIM_E_LTE_OPTIMIZATION_NODE.NODE_ID INNER join dim_e_lte_optimization_cell on DC_E_LTE_OPTIMIZATION_KPI_RAW.CELL_ID=dim_e_lte_optimization_cell.CELL_ID WHERE KPI_ID=08 AND DATETIME_ID ='%s' and node_name='%s' order by node_name,cell_name" %(SQLConfig[1],SQLConfig[2])
#8y
    
#9x    
    elif SQLConfig[0] =='9':
		if noNode ==1:
			targetSQL = "SELECT KPI_ID, DC_E_LTE_OPTIMIZATION_KPI_RAW.NODE_ID,DIM_E_LTE_OPTIMIZATION_NODE.NODE_NAME,DC_E_LTE_OPTIMIZATION_KPI_RAW.CELL_ID,dim_e_lte_optimization_cell.CELL_NAME,DC_E_LTE_OPTIMIZATION_KPI_RAW.KPI_VALUE,DATETIME_ID,UTC_DATETIME_ID,ROWSTATUS FROM DC_E_LTE_OPTIMIZATION_KPI_RAW INNER join DIM_E_LTE_OPTIMIZATION_NODE on DC_E_LTE_OPTIMIZATION_KPI_RAW.NODE_ID=DIM_E_LTE_OPTIMIZATION_NODE.NODE_ID INNER join dim_e_lte_optimization_cell on DC_E_LTE_OPTIMIZATION_KPI_RAW.CELL_ID=dim_e_lte_optimization_cell.CELL_ID WHERE KPI_ID=09 AND DATETIME_ID ='%s' order by node_name,cell_name" %(SQLConfig[1])
		else:
			targetSQL = "SELECT KPI_ID, DC_E_LTE_OPTIMIZATION_KPI_RAW.NODE_ID,DIM_E_LTE_OPTIMIZATION_NODE.NODE_NAME,DC_E_LTE_OPTIMIZATION_KPI_RAW.CELL_ID,dim_e_lte_optimization_cell.CELL_NAME,DC_E_LTE_OPTIMIZATION_KPI_RAW.KPI_VALUE,DATETIME_ID,UTC_DATETIME_ID,ROWSTATUS FROM DC_E_LTE_OPTIMIZATION_KPI_RAW INNER join DIM_E_LTE_OPTIMIZATION_NODE on DC_E_LTE_OPTIMIZATION_KPI_RAW.NODE_ID=DIM_E_LTE_OPTIMIZATION_NODE.NODE_ID INNER join dim_e_lte_optimization_cell on DC_E_LTE_OPTIMIZATION_KPI_RAW.CELL_ID=dim_e_lte_optimization_cell.CELL_ID WHERE KPI_ID=09 AND DATETIME_ID ='%s' and node_name='%s' order by node_name,cell_name" %(SQLConfig[1],SQLConfig[2])
#9y
    
#10x
    elif SQLConfig[0] =='10':
		if noNode ==1:
			targetSQL = "SELECT KPI_ID, DC_E_LTE_OPTIMIZATION_KPI_RAW.NODE_ID,DIM_E_LTE_OPTIMIZATION_NODE.NODE_NAME,DC_E_LTE_OPTIMIZATION_KPI_RAW.CELL_ID,dim_e_lte_optimization_cell.CELL_NAME,DC_E_LTE_OPTIMIZATION_KPI_RAW.KPI_VALUE,DATETIME_ID,UTC_DATETIME_ID,ROWSTATUS FROM DC_E_LTE_OPTIMIZATION_KPI_RAW INNER join DIM_E_LTE_OPTIMIZATION_NODE on DC_E_LTE_OPTIMIZATION_KPI_RAW.NODE_ID=DIM_E_LTE_OPTIMIZATION_NODE.NODE_ID INNER join dim_e_lte_optimization_cell on DC_E_LTE_OPTIMIZATION_KPI_RAW.CELL_ID=dim_e_lte_optimization_cell.CELL_ID WHERE KPI_ID=10 AND DATETIME_ID ='%s' order by node_name,cell_name" %(SQLConfig[1])
		else:
			targetSQL = "SELECT KPI_ID, DC_E_LTE_OPTIMIZATION_KPI_RAW.NODE_ID,DIM_E_LTE_OPTIMIZATION_NODE.NODE_NAME,DC_E_LTE_OPTIMIZATION_KPI_RAW.CELL_ID,dim_e_lte_optimization_cell.CELL_NAME,DC_E_LTE_OPTIMIZATION_KPI_RAW.KPI_VALUE,DATETIME_ID,UTC_DATETIME_ID,ROWSTATUS FROM DC_E_LTE_OPTIMIZATION_KPI_RAW INNER join DIM_E_LTE_OPTIMIZATION_NODE on DC_E_LTE_OPTIMIZATION_KPI_RAW.NODE_ID=DIM_E_LTE_OPTIMIZATION_NODE.NODE_ID INNER join dim_e_lte_optimization_cell on DC_E_LTE_OPTIMIZATION_KPI_RAW.CELL_ID=dim_e_lte_optimization_cell.CELL_ID WHERE KPI_ID=10 AND DATETIME_ID ='%s' and node_name='%s' order by node_name,cell_name" %(SQLConfig[1],SQLConfig[2])
#10y

#11x
    elif SQLConfig[0] =='11':
		if noNode ==1:
			targetSQL= "SELECT KPI_ID, DC_E_LTE_OPTIMIZATION_KPI_RAW.NODE_ID,DIM_E_LTE_OPTIMIZATION_NODE.NODE_NAME,DC_E_LTE_OPTIMIZATION_KPI_RAW.CELL_ID,dim_e_lte_optimization_cell.CELL_NAME,DC_E_LTE_OPTIMIZATION_KPI_RAW.KPI_VALUE,DATETIME_ID,UTC_DATETIME_ID,ROWSTATUS FROM DC_E_LTE_OPTIMIZATION_KPI_RAW INNER join DIM_E_LTE_OPTIMIZATION_NODE on DC_E_LTE_OPTIMIZATION_KPI_RAW.NODE_ID=DIM_E_LTE_OPTIMIZATION_NODE.NODE_ID INNER join dim_e_lte_optimization_cell on DC_E_LTE_OPTIMIZATION_KPI_RAW.CELL_ID=dim_e_lte_optimization_cell.CELL_ID WHERE KPI_ID=11 AND DATETIME_ID ='%s' order by node_name,cell_name" %(SQLConfig[1])
		else:
			targetSQL= "SELECT KPI_ID, DC_E_LTE_OPTIMIZATION_KPI_RAW.NODE_ID,DIM_E_LTE_OPTIMIZATION_NODE.NODE_NAME,DC_E_LTE_OPTIMIZATION_KPI_RAW.CELL_ID,dim_e_lte_optimization_cell.CELL_NAME,DC_E_LTE_OPTIMIZATION_KPI_RAW.KPI_VALUE,DATETIME_ID,UTC_DATETIME_ID,ROWSTATUS FROM DC_E_LTE_OPTIMIZATION_KPI_RAW INNER join DIM_E_LTE_OPTIMIZATION_NODE on DC_E_LTE_OPTIMIZATION_KPI_RAW.NODE_ID=DIM_E_LTE_OPTIMIZATION_NODE.NODE_ID INNER join dim_e_lte_optimization_cell on DC_E_LTE_OPTIMIZATION_KPI_RAW.CELL_ID=dim_e_lte_optimization_cell.CELL_ID WHERE KPI_ID=11 AND DATETIME_ID ='%s' and node_name='%s' order by node_name,cell_name" %(SQLConfig[1],SQLConfig[2])
#11y

#12x
    elif SQLConfig[0] =='12':
		if noNode ==1:
			targetSQL = "SELECT KPI_ID, DC_E_LTE_OPTIMIZATION_KPI_RAW.NODE_ID,DIM_E_LTE_OPTIMIZATION_NODE.NODE_NAME,DC_E_LTE_OPTIMIZATION_KPI_RAW.CELL_ID,dim_e_lte_optimization_cell.CELL_NAME,DC_E_LTE_OPTIMIZATION_KPI_RAW.KPI_VALUE,DATETIME_ID,UTC_DATETIME_ID,ROWSTATUS FROM DC_E_LTE_OPTIMIZATION_KPI_RAW INNER join DIM_E_LTE_OPTIMIZATION_NODE on DC_E_LTE_OPTIMIZATION_KPI_RAW.NODE_ID=DIM_E_LTE_OPTIMIZATION_NODE.NODE_ID INNER join dim_e_lte_optimization_cell on DC_E_LTE_OPTIMIZATION_KPI_RAW.CELL_ID=dim_e_lte_optimization_cell.CELL_ID WHERE KPI_ID=12 AND DATETIME_ID ='%s' order by node_name,cell_name" %(SQLConfig[1])
		else:
			targetSQL = "SELECT KPI_ID, DC_E_LTE_OPTIMIZATION_KPI_RAW.NODE_ID,DIM_E_LTE_OPTIMIZATION_NODE.NODE_NAME,DC_E_LTE_OPTIMIZATION_KPI_RAW.CELL_ID,dim_e_lte_optimization_cell.CELL_NAME,DC_E_LTE_OPTIMIZATION_KPI_RAW.KPI_VALUE,DATETIME_ID,UTC_DATETIME_ID,ROWSTATUS FROM DC_E_LTE_OPTIMIZATION_KPI_RAW INNER join DIM_E_LTE_OPTIMIZATION_NODE on DC_E_LTE_OPTIMIZATION_KPI_RAW.NODE_ID=DIM_E_LTE_OPTIMIZATION_NODE.NODE_ID INNER join dim_e_lte_optimization_cell on DC_E_LTE_OPTIMIZATION_KPI_RAW.CELL_ID=dim_e_lte_optimization_cell.CELL_ID WHERE KPI_ID=12 AND DATETIME_ID ='%s' and node_name='%s' order by node_name,cell_name" %(SQLConfig[1],SQLConfig[2])
#12y

#14x 
    elif SQLConfig[0] =='15':
		if noNode ==1:
			targetSQL = "SELECT KPI_ID, DC_E_LTE_OPTIMIZATION_KPI_RAW.NODE_ID,DIM_E_LTE_OPTIMIZATION_NODE.NODE_NAME,CELL_ID,DC_E_LTE_OPTIMIZATION_KPI_RAW.KPI_VALUE,DATETIME_ID,DATETIME_ID FROM DC_E_LTE_OPTIMIZATION_KPI_RAW INNER join DIM_E_LTE_OPTIMIZATION_NODE on DC_E_LTE_OPTIMIZATION_KPI_RAW.NODE_ID=DIM_E_LTE_OPTIMIZATION_NODE.NODE_ID WHERE KPI_ID=15 AND DATETIME_ID ='%s' order by node_name" %(SQLConfig[1])
		else:
			targetSQL = "SELECT KPI_ID, DC_E_LTE_OPTIMIZATION_KPI_RAW.NODE_ID,DIM_E_LTE_OPTIMIZATION_NODE.NODE_NAME,CELL_ID,DC_E_LTE_OPTIMIZATION_KPI_RAW.KPI_VALUE,DATETIME_ID,DATETIME_ID FROM DC_E_LTE_OPTIMIZATION_KPI_RAW INNER join DIM_E_LTE_OPTIMIZATION_NODE on DC_E_LTE_OPTIMIZATION_KPI_RAW.NODE_ID=DIM_E_LTE_OPTIMIZATION_NODE.NODE_ID WHERE KPI_ID=15 AND DATETIME_ID ='%s' and node_name ='%s' order by node_name" %(SQLConfig[1],SQLConfig[2])
#14y

#15x
    elif SQLConfig[0] =='16':
		if noNode ==1:
			targetSQL = "SELECT KPI_ID, DC_E_LTE_OPTIMIZATION_KPI_RAW.NODE_ID,DIM_E_LTE_OPTIMIZATION_NODE.NODE_NAME,CELL_ID,DC_E_LTE_OPTIMIZATION_KPI_RAW.KPI_VALUE,DATETIME_ID,DATETIME_ID FROM DC_E_LTE_OPTIMIZATION_KPI_RAW INNER join DIM_E_LTE_OPTIMIZATION_NODE on DC_E_LTE_OPTIMIZATION_KPI_RAW.NODE_ID=DIM_E_LTE_OPTIMIZATION_NODE.NODE_ID WHERE KPI_ID=16 AND DATETIME_ID ='%s' order by node_name" %(SQLConfig[1])
		else:
			targetSQL = "SELECT KPI_ID, DC_E_LTE_OPTIMIZATION_KPI_RAW.NODE_ID,DIM_E_LTE_OPTIMIZATION_NODE.NODE_NAME,CELL_ID,DC_E_LTE_OPTIMIZATION_KPI_RAW.KPI_VALUE,DATETIME_ID,DATETIME_ID FROM DC_E_LTE_OPTIMIZATION_KPI_RAW INNER join DIM_E_LTE_OPTIMIZATION_NODE on DC_E_LTE_OPTIMIZATION_KPI_RAW.NODE_ID=DIM_E_LTE_OPTIMIZATION_NODE.NODE_ID WHERE KPI_ID=16 AND DATETIME_ID ='%s' and node_name ='%s' order by node_name" %(SQLConfig[1],SQLConfig[2])
#15y

#17x
    elif SQLConfig[0] =='17':
		if noNode ==1:
			targetSQL = "SELECT KPI_ID, DC_E_LTE_OPTIMIZATION_KPI_RAW.NODE_ID,DIM_E_LTE_OPTIMIZATION_NODE.NODE_NAME,CELL_ID,DC_E_LTE_OPTIMIZATION_KPI_RAW.KPI_VALUE,DATETIME_ID,DATETIME_ID FROM DC_E_LTE_OPTIMIZATION_KPI_RAW INNER join DIM_E_LTE_OPTIMIZATION_NODE on DC_E_LTE_OPTIMIZATION_KPI_RAW.NODE_ID=DIM_E_LTE_OPTIMIZATION_NODE.NODE_ID WHERE KPI_ID=17 AND DATETIME_ID ='%s' order by node_name" %(SQLConfig[1])
		else:
			targetSQL = "SELECT KPI_ID, DC_E_LTE_OPTIMIZATION_KPI_RAW.NODE_ID,DIM_E_LTE_OPTIMIZATION_NODE.NODE_NAME,CELL_ID,DC_E_LTE_OPTIMIZATION_KPI_RAW.KPI_VALUE,DATETIME_ID,DATETIME_ID FROM DC_E_LTE_OPTIMIZATION_KPI_RAW INNER join DIM_E_LTE_OPTIMIZATION_NODE on DC_E_LTE_OPTIMIZATION_KPI_RAW.NODE_ID=DIM_E_LTE_OPTIMIZATION_NODE.NODE_ID WHERE KPI_ID=17 AND DATETIME_ID ='%s' and node_name ='%s' order by node_name" %(SQLConfig[1],SQLConfig[2])
#17y
    
#18x
    elif SQLConfig[0] =='18':
		if noNode ==1:
			targetSQL = "SELECT KPI_ID, DC_E_LTE_OPTIMIZATION_KPI_RAW.NODE_ID,DIM_E_LTE_OPTIMIZATION_NODE.NODE_NAME,CELL_ID,DC_E_LTE_OPTIMIZATION_KPI_RAW.KPI_VALUE,DATETIME_ID,DATETIME_ID FROM DC_E_LTE_OPTIMIZATION_KPI_RAW INNER join DIM_E_LTE_OPTIMIZATION_NODE on DC_E_LTE_OPTIMIZATION_KPI_RAW.NODE_ID=DIM_E_LTE_OPTIMIZATION_NODE.NODE_ID WHERE KPI_ID=18 AND DATETIME_ID ='%s' order by node_name" %(SQLConfig[1])
		else:
			targetSQL = "SELECT KPI_ID, DC_E_LTE_OPTIMIZATION_KPI_RAW.NODE_ID,DIM_E_LTE_OPTIMIZATION_NODE.NODE_NAME,CELL_ID,DC_E_LTE_OPTIMIZATION_KPI_RAW.KPI_VALUE,DATETIME_ID,DATETIME_ID FROM DC_E_LTE_OPTIMIZATION_KPI_RAW INNER join DIM_E_LTE_OPTIMIZATION_NODE on DC_E_LTE_OPTIMIZATION_KPI_RAW.NODE_ID=DIM_E_LTE_OPTIMIZATION_NODE.NODE_ID WHERE KPI_ID=18 AND DATETIME_ID ='%s' and node_name ='%s' order by node_name" %(SQLConfig[1],SQLConfig[2])
#18y

#19x
    elif SQLConfig[0] =='19':
		targetSQL= "select DC_E_LTE_OPTIMIZATION_NODE_SINR_RAW.NODE_ID,DIM_E_LTE_OPTIMIZATION_NODE.NODE_NAME,DC_E_LTE_OPTIMIZATION_NODE_SINR_RAW.OSS_ID,RANGE_ID, Sector_Carrier,ANTENNA_PAIR, COUNT from DC_E_LTE_OPTIMIZATION_NODE_SINR_RAW INNER join DIM_E_LTE_OPTIMIZATION_NODE on DC_E_LTE_OPTIMIZATION_NODE_SINR_RAW.NODE_ID=DIM_E_LTE_OPTIMIZATION_NODE.NODE_ID WHERE DATETIME_ID='%s' and node_name='%s' order by node_name, RANGE_ID,Sector_Carrier,ANTENNA_PAIR" %(SQLConfig[1],SQLConfig[3])
#19y
    return targetSQL
