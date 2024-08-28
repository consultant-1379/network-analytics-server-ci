def SQLFunctionSource(SQLConfig,noNode):
#1a
    if SQLConfig[0] =='1':
        if noNode==1:
            sourceSQL="SELECT SN, OSS_ID, DATETIME_ID, SUM(pmEnergyConsumption) AS pmEnergyConsumption FROM (SELECT SN, OSS_ID, DATETIME_ID, pmEnergyConsumption FROM DC_E_CPP_ENERGYMEASUREMENT_RAW WHERE DATETIME_ID  = '%s' UNION ALL SELECT SN, OSS_ID, DATETIME_ID, pmEnergyConsumption FROM DC_E_TCU_ENERGYMEASUREMENT_RAW WHERE DATETIME_ID  = '%s') pmEnergyConsumption GROUP BY SN, OSS_ID, DATETIME_ID" %(SQLConfig[1],SQLConfig[1])
        else:
            SN="SubNetwork=ONRM_RootMo,SubNetwork=LRAN,MeContext=%s" %(SQLConfig[2])
            sourceSQL="SELECT SN, OSS_ID, DATETIME_ID, SUM(pmEnergyConsumption) AS pmEnergyConsumption FROM (SELECT SN, OSS_ID, DATETIME_ID, pmEnergyConsumption FROM DC_E_CPP_ENERGYMEASUREMENT_RAW WHERE DATETIME_ID  = '%s' and SN='%s' UNION ALL SELECT SN, OSS_ID, DATETIME_ID, pmEnergyConsumption FROM DC_E_TCU_ENERGYMEASUREMENT_RAW WHERE DATETIME_ID  = '%s' and SN='%s') pmEnergyConsumption GROUP BY SN, OSS_ID, DATETIME_ID" %(SQLConfig[1],SN,SQLConfig[1],SN)
#1b

#2a   
    elif SQLConfig[0] =='2':
        if noNode==1:
            sourceSQL="SELECT ERBS, OSS_ID, DATETIME_ID, SUM(pmPdcpVolDlDrb) AS pmPdcpVolDlDrb FROM (SELECT ERBS, OSS_ID, DATETIME_ID, MOID, pmPdcpVolDlDrb FROM DC_E_ERBS_EUTRANCELLFDD_RAW WHERE DATETIME_ID  = '%s' UNION ALL SELECT ERBS, OSS_ID, DATETIME_ID, MOID, pmPdcpVolDlDrb FROM DC_E_ERBS_EUTRANCELLTDD_RAW WHERE DATETIME_ID  = '%s') pmPdcpVolDlDrb GROUP BY ERBS, OSS_ID, DATETIME_ID" %(SQLConfig[1],SQLConfig[1])
        else:
            sourceSQL="SELECT ERBS, OSS_ID, DATETIME_ID, SUM(pmPdcpVolDlDrb) AS pmPdcpVolDlDrb FROM (SELECT ERBS, OSS_ID, DATETIME_ID, MOID, pmPdcpVolDlDrb FROM DC_E_ERBS_EUTRANCELLFDD_RAW WHERE DATETIME_ID  = '%s' and ERBS='%s' UNION ALL SELECT ERBS, OSS_ID, DATETIME_ID, MOID, pmPdcpVolDlDrb FROM DC_E_ERBS_EUTRANCELLTDD_RAW WHERE DATETIME_ID  = '%s' and ERBS='%s') pmPdcpVolDlDrb GROUP BY ERBS, OSS_ID, DATETIME_ID" %(SQLConfig[1],SQLConfig[2],SQLConfig[1],SQLConfig[2])
#2b

#3a
    elif SQLConfig[0] =='3':
        if noNode==1:
            sourceSQL="SELECT ERBS, OSS_ID, DATETIME_ID, SUM(pmPdcpVolUlDrb) AS pmPdcpVolUlDrb FROM(SELECT ERBS, OSS_ID, DATETIME_ID, pmPdcpVolUlDrb FROM DC_E_ERBS_EUTRANCELLFDD_RAW WHERE DATETIME_ID  = '%s' UNION ALL SELECT ERBS, OSS_ID, DATETIME_ID, pmPdcpVolUlDrb FROM DC_E_ERBS_EUTRANCELLTDD_RAW WHERE DATETIME_ID  = '%s') pmPdcpVolUlDrb GROUP BY ERBS, OSS_ID, DATETIME_ID" %(SQLConfig[1],SQLConfig[1])
        else:
            sourceSQL="SELECT ERBS, OSS_ID, DATETIME_ID, SUM(pmPdcpVolUlDrb) AS pmPdcpVolUlDrb FROM(SELECT ERBS, OSS_ID, DATETIME_ID, pmPdcpVolUlDrb FROM DC_E_ERBS_EUTRANCELLFDD_RAW WHERE DATETIME_ID  = '%s' and ERBS='%s' UNION ALL SELECT ERBS, OSS_ID, DATETIME_ID, pmPdcpVolUlDrb FROM DC_E_ERBS_EUTRANCELLTDD_RAW WHERE DATETIME_ID  = '%s' and ERBS='%s') pmPdcpVolUlDrb GROUP BY ERBS, OSS_ID, DATETIME_ID" %(SQLConfig[1],SQLConfig[2],SQLConfig[1],SQLConfig[2])
#3b

#4a            
    elif SQLConfig[0] =='4':
        if noNode==1:
            sourceSQL="SELECT ERBS, OSS_ID, DATETIME_ID, 100 * AVG(pmMicroTxSleepTime)/900 AS pmMicroTxSleepTime FROM (SELECT ERBS, OSS_ID, DATETIME_ID, pmMicroTxSleepTime FROM DC_E_ERBS_SECTORCARRIER_RAW WHERE DATETIME_ID  = '%s') pmMicroTxSleepTime GROUP BY ERBS, OSS_ID, DATETIME_ID" %(SQLConfig[1])
        else:
            sourceSQL="SELECT ERBS, OSS_ID, DATETIME_ID, 100 * AVG(pmMicroTxSleepTime)/900 AS pmMicroTxSleepTime FROM (SELECT ERBS, OSS_ID, DATETIME_ID, pmMicroTxSleepTime FROM DC_E_ERBS_SECTORCARRIER_RAW WHERE DATETIME_ID  = '%s' and ERBS='%s') pmMicroTxSleepTime GROUP BY ERBS, OSS_ID, DATETIME_ID" %(SQLConfig[1],SQLConfig[2])
#4b

#5a
    elif SQLConfig[0] =='5':
        if noNode==1:
            sourceSQL="SELECT ERBS, OSS_ID, DATETIME_ID, EUTRANCELLFDD, SUM(100 * pmMimoSleepTime)/900 AS pmMimoSleepTime FROM(SELECT ERBS, OSS_ID, DATETIME_ID, EUTRANCELLFDD, pmMimoSleepTime FROM DC_E_ERBS_EUTRANCELLFDD_RAW WHERE DATETIME_ID  = '%s'UNION ALL SELECT ERBS, OSS_ID, DATETIME_ID,EUTRANCELLTDD, pmMimoSleepTime FROM DC_E_ERBS_EUTRANCELLTDD_RAW WHERE DATETIME_ID  = '%s') pmMimoSleepTime GROUP BY ERBS, OSS_ID,EUTRANCELLFDD, DATETIME_ID" %(SQLConfig[1],SQLConfig[1])
        else:
            sourceSQL="SELECT ERBS, OSS_ID, DATETIME_ID, EUTRANCELLFDD, SUM(100 * pmMimoSleepTime)/900 AS pmMimoSleepTime FROM(SELECT ERBS, OSS_ID, DATETIME_ID, EUTRANCELLFDD, pmMimoSleepTime FROM DC_E_ERBS_EUTRANCELLFDD_RAW WHERE DATETIME_ID  = '%s' and ERBS='%s' UNION ALL SELECT ERBS, OSS_ID, DATETIME_ID,EUTRANCELLTDD, pmMimoSleepTime FROM DC_E_ERBS_EUTRANCELLTDD_RAW WHERE DATETIME_ID  = '%s' and ERBS='%s') pmMimoSleepTime GROUP BY ERBS, OSS_ID,EUTRANCELLFDD, DATETIME_ID" %(SQLConfig[1],SQLConfig[2],SQLConfig[1],SQLConfig[2])
#5b

#6a 
    elif SQLConfig[0] =='6':
        if noNode==1:
            sourceSQL="SELECT ERBS, OSS_ID, DATETIME_ID, EUTRANCELLFDD, SUM(100 * pmCellSleepTime)/900 AS pmCellSleepTime FROM(SELECT ERBS, OSS_ID, DATETIME_ID, EUTRANCELLFDD, pmCellSleepTime FROM DC_E_ERBS_EUTRANCELLFDD_RAW WHERE DATETIME_ID  = '%s' UNION ALL SELECT ERBS, OSS_ID, DATETIME_ID, EUTRANCELLTDD, pmCellSleepTime FROM DC_E_ERBS_EUTRANCELLTDD_RAW WHERE DATETIME_ID  = '%s') pmCellSleepTime GROUP BY ERBS, OSS_ID, DATETIME_ID,EUTRANCELLFDD" %(SQLConfig[1],SQLConfig[1])
        else:
            sourceSQL="SELECT ERBS, OSS_ID, DATETIME_ID, EUTRANCELLFDD, SUM(100 * pmCellSleepTime)/900 AS pmCellSleepTime FROM(SELECT ERBS, OSS_ID, DATETIME_ID, EUTRANCELLFDD, pmCellSleepTime FROM DC_E_ERBS_EUTRANCELLFDD_RAW WHERE DATETIME_ID  = '%s' and ERBS='%s' UNION ALL SELECT ERBS, OSS_ID, DATETIME_ID, EUTRANCELLTDD, pmCellSleepTime FROM DC_E_ERBS_EUTRANCELLTDD_RAW WHERE DATETIME_ID  = '%s' and ERBS='%s') pmCellSleepTime GROUP BY ERBS, OSS_ID, DATETIME_ID,EUTRANCELLFDD" %(SQLConfig[1],SQLConfig[2],SQLConfig[1],SQLConfig[2])
#6b

#7a    
    elif SQLConfig[0] =='7':
        if noNode==1:
            sourceSQL="SELECT ERBS, DATETIME_ID,EUtranCellFDD, SUM(100 * pmCellDowntimeMan)/900 AS pmCellDowntimeMan FROM (SELECT ERBS, DATETIME_ID,EUtranCellFDD, pmCellDowntimeMan FROM DC_E_ERBS_EUTRANCELLFDD_RAW WHERE DATETIME_ID  = '%s' UNION ALL SELECT ERBS, DATETIME_ID, EUtranCellTDD, pmCellDowntimeMan FROM DC_E_ERBS_EUTRANCELLTDD_RAW WHERE DATETIME_ID  = '%s') pmCellDowntimeMan GROUP BY ERBS,DATETIME_ID,EUtranCellFDD" %(SQLConfig[1],SQLConfig[1])
        else:
            sourceSQL="SELECT ERBS, DATETIME_ID,EUtranCellFDD, SUM(100 * pmCellDowntimeMan)/900 AS pmCellDowntimeMan FROM (SELECT ERBS, DATETIME_ID,EUtranCellFDD, pmCellDowntimeMan FROM DC_E_ERBS_EUTRANCELLFDD_RAW WHERE DATETIME_ID  = '%s' and ERBS='%s' UNION ALL SELECT ERBS, DATETIME_ID, EUtranCellTDD, pmCellDowntimeMan FROM DC_E_ERBS_EUTRANCELLTDD_RAW WHERE DATETIME_ID  = '%s'  and ERBS='%s') pmCellDowntimeMan GROUP BY ERBS,DATETIME_ID,EUtranCellFDD" %(SQLConfig[1],SQLConfig[2],SQLConfig[1],SQLConfig[2])
#7b
    return sourceSQL
   
def SQLFunctionTarget(SQLConfig,noNode):
#1x
    if SQLConfig[0] =='1':
        #depending on the value of NoNode it sets a varible equal to a SQL command with string formatters replacing the configurable option found in the command
        if noNode ==1:
            targetSQL="SELECT dim_node.NODE_ID AS NODE_ID, dim_node.NODE_FDN AS SN, dim_node.NODE_NAME, dc_raw.OSS_ID AS OSS_ID, DATETIME_ID, MEASURE_VALUE FROM DC_E_ENERGY_NODE_RAW dc_raw, DIM_E_ENERGY_NODE dim_node WHERE DATETIME_ID = '%s' AND dim_node.NODE_ID = dc_raw.NODE_ID AND MEASURE_ID = 1 GROUP BY NODE_ID, SN,NODE_NAME, OSS_ID, DATETIME_ID, MEASURE_VALUE" %(SQLConfig[1])
        else:
            targetSQL="SELECT dim_node.NODE_ID AS NODE_ID, dim_node.NODE_FDN AS SN, dim_node.NODE_NAME, dc_raw.OSS_ID AS OSS_ID, DATETIME_ID, MEASURE_VALUE FROM DC_E_ENERGY_NODE_RAW dc_raw, DIM_E_ENERGY_NODE dim_node WHERE DATETIME_ID = '%s' AND dim_node.NODE_ID = dc_raw.NODE_ID AND MEASURE_ID = 1 and NODE_NAME='%s' GROUP BY NODE_ID, SN,NODE_NAME, OSS_ID, DATETIME_ID, MEASURE_VALUE" %(SQLConfig[1],SQLConfig[2])
#1y

#2x   
    elif SQLConfig[0] =='2':
        if noNode ==1:
            targetSQL="SELECT dim_node.NODE_ID AS NODE_ID, dim_node.NODE_FDN AS SN, dim_node.NODE_NAME AS NODE_NAME, dc_raw.OSS_ID AS OSS_ID, DATETIME_ID, MEASURE_VALUE FROM DC_E_ENERGY_NODE_RAW dc_raw, DIM_E_ENERGY_NODE dim_node WHERE DATETIME_ID = '%s' AND dim_node.NODE_ID = dc_raw.NODE_ID AND MEASURE_ID = 2 GROUP BY NODE_ID, SN, OSS_ID, DATETIME_ID, MEASURE_VALUE,NODE_NAME" %(SQLConfig[1])
        else:
            targetSQL="SELECT dim_node.NODE_ID AS NODE_ID, dim_node.NODE_FDN AS SN, dim_node.NODE_NAME AS NODE_NAME, dc_raw.OSS_ID AS OSS_ID, DATETIME_ID, MEASURE_VALUE FROM DC_E_ENERGY_NODE_RAW dc_raw, DIM_E_ENERGY_NODE dim_node WHERE DATETIME_ID = '%s' AND dim_node.NODE_ID = dc_raw.NODE_ID AND MEASURE_ID = 2 and NODE_NAME='%s' GROUP BY NODE_ID, SN, OSS_ID, DATETIME_ID, MEASURE_VALUE,NODE_NAME" %(SQLConfig[1],SQLConfig[2])
#2y

#3x
    elif SQLConfig[0] =='3':
        if noNode ==1:
            targetSQL="SELECT dim_node.NODE_ID AS NODE_ID, dim_node.NODE_FDN AS SN, dc_raw.OSS_ID AS OSS_ID, dim_node.NODE_NAME AS NODE_NAME, DATETIME_ID, MEASURE_VALUE FROM DC_E_ENERGY_NODE_RAW dc_raw, DIM_E_ENERGY_NODE dim_node WHERE DATETIME_ID = '%s' AND dim_node.NODE_ID = dc_raw.NODE_ID AND MEASURE_ID = 3 GROUP BY NODE_ID, SN, OSS_ID, DATETIME_ID, MEASURE_VALUE,NODE_NAME" %(SQLConfig[1])
        else:
            targetSQL="SELECT dim_node.NODE_ID AS NODE_ID, dim_node.NODE_FDN AS SN, dc_raw.OSS_ID AS OSS_ID, dim_node.NODE_NAME AS NODE_NAME, DATETIME_ID, MEASURE_VALUE FROM DC_E_ENERGY_NODE_RAW dc_raw, DIM_E_ENERGY_NODE dim_node WHERE DATETIME_ID = '%s' AND dim_node.NODE_ID = dc_raw.NODE_ID AND MEASURE_ID = 3 and NODE_NAME='%s' GROUP BY NODE_ID, SN, OSS_ID, DATETIME_ID, MEASURE_VALUE,NODE_NAME" %(SQLConfig[1],SQLConfig[2])
#3y

#4x            
    elif SQLConfig[0] =='4':
        if noNode ==1:
            targetSQL="SELECT dim_node.NODE_ID AS NODE_ID, dim_node.NODE_FDN AS SN, dc_raw.OSS_ID AS OSS_ID, dim_node.NODE_NAME AS NODE_NAME, DATETIME_ID, MEASURE_VALUE FROM DC_E_ENERGY_NODE_RAW dc_raw, DIM_E_ENERGY_NODE dim_node WHERE DATETIME_ID = '%s' AND dim_node.NODE_ID = dc_raw.NODE_ID AND MEASURE_ID = 4 GROUP BY NODE_ID, SN, OSS_ID, DATETIME_ID, MEASURE_VALUE,NODE_NAME" %(SQLConfig[1])
        else:
            targetSQL="SELECT dim_node.NODE_ID AS NODE_ID, dim_node.NODE_FDN AS SN, dc_raw.OSS_ID AS OSS_ID, dim_node.NODE_NAME AS NODE_NAME, DATETIME_ID, MEASURE_VALUE FROM DC_E_ENERGY_NODE_RAW dc_raw, DIM_E_ENERGY_NODE dim_node WHERE DATETIME_ID = '%s' AND dim_node.NODE_ID = dc_raw.NODE_ID AND MEASURE_ID = 4 and NODE_NAME='%s' GROUP BY NODE_ID, SN, OSS_ID, DATETIME_ID, MEASURE_VALUE,NODE_NAME" %(SQLConfig[1],SQLConfig[2])
#4y

#5x
    elif SQLConfig[0] =='5':
        targetSQL="SELECT NODE_ID, OSS_ID,CELL_ID, DATETIME_ID, SUM(MEASURE_VALUE) AS MEASURE_VALUE FROM ( SELECT NODE_ID, OSS_ID,CELL_ID, DATETIME_ID, MEASURE_VALUE FROM DC_E_ENERGY_CELL_RAW WHERE DATETIME_ID  = '%s'AND MEASURE_ID   = 5) MEASURE_VALUE GROUP BY NODE_ID, OSS_ID,CELL_ID, DATETIME_ID" %(SQLConfig[1])
#5y

#6x 
    elif SQLConfig[0] =='6':
        targetSQL="SELECT NODE_ID, OSS_ID, DATETIME_ID, CELL_ID, SUM(MEASURE_VALUE) AS MEASURE_VALUE FROM (SELECT NODE_ID, OSS_ID, DATETIME_ID, CELL_ID, MEASURE_VALUE FROM DC_E_ENERGY_CELL_RAW WHERE DATETIME_ID  = '%s'AND MEASURE_ID   = 6) MEASURE_VALUE GROUP BY NODE_ID, OSS_ID, CELL_ID, DATETIME_ID" %(SQLConfig[1])
#6y

#7x    
    elif SQLConfig[0] =='7':
        targetSQL="SELECT NODE_ID, DATETIME_ID, CELL_ID, SUM(MEASURE_VALUE) AS MEASURE_VALUE FROM (SELECT NODE_ID, DATETIME_ID, CELL_ID,  MEASURE_VALUE FROM DC_E_ENERGY_CELL_RAW  WHERE DATETIME_ID  = '%s' AND MEASURE_ID   = 7) MEASURE_VALUE GROUP BY NODE_ID,DATETIME_ID,CELL_ID" %(SQLConfig[1])
#7y
    return targetSQL

