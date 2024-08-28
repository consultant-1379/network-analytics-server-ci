def SQLFunctionSource(SQLConfig,noNode):
#1a
    if SQLConfig[0] =='1':
        if noNode==1:
            sourceSQL="select UTC_DATETIME_ID, NE_ID, OSS_ID, 100*avg(ISNULL(sbgSipNetIncSessionEstabNetworkSuccess,0)/ISNULL(sbgSipTotalIncSessSetups,0)) as KPI_VALUE from DC_E_IMSSBG_SIP_RAW where UTC_DATETIME_ID ='%s' GROUP BY UTC_DATETIME_ID, NE_ID, OSS_ID order by ne_id" %(SQLConfig[1])
        else:
            sourceSQL="select UTC_DATETIME_ID, NE_ID, OSS_ID, 100*avg(ISNULL(sbgSipNetIncSessionEstabNetworkSuccess,0)/ISNULL(sbgSipTotalIncSessSetups,0)) as KPI_VALUE from DC_E_IMSSBG_SIP_RAW where UTC_DATETIME_ID ='%s' and NE_ID='%s' GROUP BY UTC_DATETIME_ID, NE_ID, OSS_ID order by ne_id" %(SQLConfig[1],SQLConfig[2])
#1b

#2a   
    elif SQLConfig[0] =='2':
        if noNode==1:
            sourceSQL="select UTC_DATETIME_ID, NE_ID, OSS_ID, 100*avg(ISNULL(sbgSipNetOutSessionEstabNetworkSuccess,0)/ISNULL(sbgSipTotalOutSessSetups,0)) as KPI_VALUE from DC_E_IMSSBG_SIP_RAW where UTC_DATETIME_ID ='%s' GROUP BY UTC_DATETIME_ID, NE_ID, OSS_ID order by ne_id" %(SQLConfig[1])
        else:
            sourceSQL="select UTC_DATETIME_ID, NE_ID, OSS_ID, 100*avg(ISNULL(sbgSipNetOutSessionEstabNetworkSuccess,0)/ISNULL(sbgSipTotalOutSessSetups,0)) as KPI_VALUE from DC_E_IMSSBG_SIP_RAW where UTC_DATETIME_ID ='%s' and NE_ID='%s' GROUP BY UTC_DATETIME_ID, NE_ID, OSS_ID order by ne_id" %(SQLConfig[1],SQLConfig[2])
#2b

#3a
    elif SQLConfig[0] =='3':
        if noNode==1:
            sourceSQL="drop procedure if exists calculate_kpi_3; create procedure calculate_kpi_3( in dt datetime, in node_id varchar(35)) begin select Success.g3ManagedElement as g3ManagedElement, Success.UTC_DATETIME_ID as UTC_DATETIME_ID, 100 * ( ISNULL(MtasMmtOrigNetworkSuccessSessionEstablish,0) + ISNULL(MtasMmtOrigUnregNetworkSuccessSessionEstablish,0) + ISNULL(MtasMmtOrigFailedAttemptCause_403,0) + ISNULL(MtasMmtOrigUnregFailedAttemptCause_403,0) + ISNULL(MtasMmtOrigFailedAttemptCause_404,0) + ISNULL(MtasMmtOrigUnregFailedAttemptCause_404,0) + ISNULL(MtasMmtOrigFailedAttemptCause_407,0) + ISNULL(MtasMmtOrigUnregFailedAttemptCause_407,0) + ISNULL(MtasMmtOrigFailedAttemptCause_484,0) + ISNULL(MtasMmtOrigUnregFailedAttemptCause_484,0) + ISNULL(MtasMmtOrigFailedAttemptCause_486,0) + ISNULL(MtasMmtOrigUnregFailedAttemptCause_486,0) + ISNULL(MtasMmtOrigFailedAttemptCause_600,0) + ISNULL(MtasMmtOrigUnregFailedAttemptCause_600,0))/( ISNULL(MtasMmtOrigNetworkSuccessSessionEstablish,0) + ISNULL(MtasMmtOrigUnregNetworkSuccessSessionEstablish,0) + ISNULL(MtasMmtOrigFailedAttempt,0) + ISNULL(MtasMmtOrigUnregFailedAttempt,0)) as KPI_Value from (select g3ManagedElement,UTC_DATETIME_ID, sum(ISNULL(MtasMmtOrigNetworkSuccessSessionEstablish,0)) as MtasMmtOrigNetworkSuccessSessionEstablish, sum(ISNULL(MtasMmtOrigUnregNetworkSuccessSessionEstablish,0)) as MtasMmtOrigUnregNetworkSuccessSessionEstablish FROM DC_E_MTAS_MTASMMT_RAW where UTC_DATETIME_ID = dt and g3ManagedElement = node_id group by g3ManagedElement, UTC_DATETIME_ID) as Success, (select g3ManagedElement, MOID, UTC_DATETIME_ID, ISNULL(MtasMmtOrigFailedAttemptCause,0) as MtasMmtOrigFailedAttemptCause_403, MtasMmtOrigUnregFailedAttemptCause as MtasMmtOrigUnregFailedAttemptCause_403 FROM DC_E_MTAS_MTASMMT_RAW where UTC_DATETIME_ID = dt and g3ManagedElement = node_id and MOID like '403%%') as _403,(select g3ManagedElement, MOID, UTC_DATETIME_ID, MtasMmtOrigFailedAttemptCause as MtasMmtOrigFailedAttemptCause_404, MtasMmtOrigUnregFailedAttemptCause as MtasMmtOrigUnregFailedAttemptCause_404 FROM DC_E_MTAS_MTASMMT_RAW where UTC_DATETIME_ID = dt and g3ManagedElement = node_id and MOID like '404%%') as _404,(select g3ManagedElement, MOID, UTC_DATETIME_ID, MtasMmtOrigFailedAttemptCause as MtasMmtOrigFailedAttemptCause_407, MtasMmtOrigUnregFailedAttemptCause as MtasMmtOrigUnregFailedAttemptCause_407 FROM DC_E_MTAS_MTASMMT_RAW where UTC_DATETIME_ID = dt and g3ManagedElement = node_id and MOID like '407%%') as _407,(select g3ManagedElement, MOID, UTC_DATETIME_ID, MtasMmtOrigFailedAttemptCause as MtasMmtOrigFailedAttemptCause_484, MtasMmtOrigUnregFailedAttemptCause as MtasMmtOrigUnregFailedAttemptCause_484 FROM DC_E_MTAS_MTASMMT_RAW where UTC_DATETIME_ID = dt and g3ManagedElement = node_id and MOID like '484%%') as _484,(select g3ManagedElement, MOID, UTC_DATETIME_ID, MtasMmtOrigFailedAttemptCause as MtasMmtOrigFailedAttemptCause_486, MtasMmtOrigUnregFailedAttemptCause as MtasMmtOrigUnregFailedAttemptCause_486 FROM DC_E_MTAS_MTASMMT_RAW where UTC_DATETIME_ID = dt and g3ManagedElement = node_id and MOID like '486%%') as _486,(select g3ManagedElement, MOID, UTC_DATETIME_ID, MtasMmtOrigFailedAttemptCause as MtasMmtOrigFailedAttemptCause_600, MtasMmtOrigUnregFailedAttemptCause as MtasMmtOrigUnregFailedAttemptCause_600 FROM DC_E_MTAS_MTASMMT_RAW where UTC_DATETIME_ID = dt and g3ManagedElement = node_id and MOID like '600%%') as _600,(select g3ManagedElement, UTC_DATETIME_ID, sum(ISNULL(MtasMmtOrigFailedAttempt,0)) as MtasMmtOrigFailedAttempt, sum(ISNULL(MtasMmtOrigUnregFailedAttempt,0)) as MtasMmtOrigUnregFailedAttempt FROM DC_E_MTAS_MTASMMT_RAW where UTC_DATETIME_ID = dt and g3ManagedElement = node_id group by g3ManagedElement, UTC_DATETIME_ID) as FailedAttempts, end; call calculate_kpi_3('%s', 'mtas_05');" %(SQLConfig[1])
        else:
            sourceSQL="drop procedure if exists calculate_kpi_3; create procedure calculate_kpi_3( in dt datetime, in node_id varchar(35)) begin select Success.g3ManagedElement as g3ManagedElement, Success.UTC_DATETIME_ID as UTC_DATETIME_ID, 100 * ( ISNULL(MtasMmtOrigNetworkSuccessSessionEstablish,0) + ISNULL(MtasMmtOrigUnregNetworkSuccessSessionEstablish,0) + ISNULL(MtasMmtOrigFailedAttemptCause_403,0) + ISNULL(MtasMmtOrigUnregFailedAttemptCause_403,0) + ISNULL(MtasMmtOrigFailedAttemptCause_404,0) + ISNULL(MtasMmtOrigUnregFailedAttemptCause_404,0) + ISNULL(MtasMmtOrigFailedAttemptCause_407,0) + ISNULL(MtasMmtOrigUnregFailedAttemptCause_407,0) + ISNULL(MtasMmtOrigFailedAttemptCause_484,0) + ISNULL(MtasMmtOrigUnregFailedAttemptCause_484,0) + ISNULL(MtasMmtOrigFailedAttemptCause_486,0) + ISNULL(MtasMmtOrigUnregFailedAttemptCause_486,0) + ISNULL(MtasMmtOrigFailedAttemptCause_600,0) + ISNULL(MtasMmtOrigUnregFailedAttemptCause_600,0))/( ISNULL(MtasMmtOrigNetworkSuccessSessionEstablish,0) + ISNULL(MtasMmtOrigUnregNetworkSuccessSessionEstablish,0) + ISNULL(MtasMmtOrigFailedAttempt,0) + ISNULL(MtasMmtOrigUnregFailedAttempt,0)) as KPI_Value from (select g3ManagedElement,UTC_DATETIME_ID, sum(ISNULL(MtasMmtOrigNetworkSuccessSessionEstablish,0)) as MtasMmtOrigNetworkSuccessSessionEstablish, sum(ISNULL(MtasMmtOrigUnregNetworkSuccessSessionEstablish,0)) as MtasMmtOrigUnregNetworkSuccessSessionEstablish FROM DC_E_MTAS_MTASMMT_RAW where UTC_DATETIME_ID = dt and g3ManagedElement = node_id group by g3ManagedElement, UTC_DATETIME_ID) as Success, (select g3ManagedElement, MOID, UTC_DATETIME_ID, ISNULL(MtasMmtOrigFailedAttemptCause,0) as MtasMmtOrigFailedAttemptCause_403, MtasMmtOrigUnregFailedAttemptCause as MtasMmtOrigUnregFailedAttemptCause_403 FROM DC_E_MTAS_MTASMMT_RAW where UTC_DATETIME_ID = dt and g3ManagedElement = node_id and MOID like '403%%') as _403,(select g3ManagedElement, MOID, UTC_DATETIME_ID, MtasMmtOrigFailedAttemptCause as MtasMmtOrigFailedAttemptCause_404, MtasMmtOrigUnregFailedAttemptCause as MtasMmtOrigUnregFailedAttemptCause_404 FROM DC_E_MTAS_MTASMMT_RAW where UTC_DATETIME_ID = dt and g3ManagedElement = node_id and MOID like '404%%') as _404,(select g3ManagedElement, MOID, UTC_DATETIME_ID, MtasMmtOrigFailedAttemptCause as MtasMmtOrigFailedAttemptCause_407, MtasMmtOrigUnregFailedAttemptCause as MtasMmtOrigUnregFailedAttemptCause_407 FROM DC_E_MTAS_MTASMMT_RAW where UTC_DATETIME_ID = dt and g3ManagedElement = node_id and MOID like '407%%') as _407,(select g3ManagedElement, MOID, UTC_DATETIME_ID, MtasMmtOrigFailedAttemptCause as MtasMmtOrigFailedAttemptCause_484, MtasMmtOrigUnregFailedAttemptCause as MtasMmtOrigUnregFailedAttemptCause_484 FROM DC_E_MTAS_MTASMMT_RAW where UTC_DATETIME_ID = dt and g3ManagedElement = node_id and MOID like '484%%') as _484,(select g3ManagedElement, MOID, UTC_DATETIME_ID, MtasMmtOrigFailedAttemptCause as MtasMmtOrigFailedAttemptCause_486, MtasMmtOrigUnregFailedAttemptCause as MtasMmtOrigUnregFailedAttemptCause_486 FROM DC_E_MTAS_MTASMMT_RAW where UTC_DATETIME_ID = dt and g3ManagedElement = node_id and MOID like '486%%') as _486,(select g3ManagedElement, MOID, UTC_DATETIME_ID, MtasMmtOrigFailedAttemptCause as MtasMmtOrigFailedAttemptCause_600, MtasMmtOrigUnregFailedAttemptCause as MtasMmtOrigUnregFailedAttemptCause_600 FROM DC_E_MTAS_MTASMMT_RAW where UTC_DATETIME_ID = dt and g3ManagedElement = node_id and MOID like '600%%') as _600,(select g3ManagedElement, UTC_DATETIME_ID, sum(ISNULL(MtasMmtOrigFailedAttempt,0)) as MtasMmtOrigFailedAttempt, sum(ISNULL(MtasMmtOrigUnregFailedAttempt,0)) as MtasMmtOrigUnregFailedAttempt FROM DC_E_MTAS_MTASMMT_RAW where UTC_DATETIME_ID = dt and g3ManagedElement = node_id group by g3ManagedElement, UTC_DATETIME_ID) as FailedAttempts, end; call calculate_kpi_3('%s', '%s');" %(SQLConfig[1],SQLConfig[2])
#3b

#4a            
    elif SQLConfig[0] =='4':
        if noNode==1:
            sourceSQL="drop procedure if exists calculate_kpi_4; create procedure calculate_kpi_4( in dt datetime, in node_id varchar(35)) begin select Success.g3ManagedElement as g3ManagedElement, Success.UTC_DATETIME_ID as UTC_DATETIME_ID, 100 * ( ISNULL(MtasMmtTermNetworkSuccessSessionEstablish,0) + ISNULL(MtasMmtTermUnregNetworkSuccessSessionEstablish,0) + ISNULL(MtasMmtTermFailedAttemptCause_403,0) + ISNULL(MtasMmtTermUnregFailedAttemptCause_403,0) + ISNULL(MtasMmtTermFailedAttemptCause_404,0) + ISNULL(MtasMmtTermUnregFailedAttemptCause_404,0) + ISNULL(MtasMmtTermFailedAttemptCause_407,0) + ISNULL(MtasMmtTermUnregFailedAttemptCause_407,0) + ISNULL(MtasMmtTermFailedAttemptCause_484,0) + ISNULL(MtasMmtTermUnregFailedAttemptCause_484,0) + ISNULL(MtasMmtTermFailedAttemptCause_486,0) + ISNULL(MtasMmtTermUnregFailedAttemptCause_486,0) + ISNULL(MtasMmtTermFailedAttemptCause_600,0) + ISNULL(MtasMmtTermUnregFailedAttemptCause_600,0))/( ISNULL(MtasMmtTermNetworkSuccessSessionEstablish,0) + ISNULL(MtasMmtTermUnregNetworkSuccessSessionEstablish,0) + ISNULL(MtasMmtTermFailedAttempt,0) + ISNULL(MtasMmtTermUnregFailedAttempt,0)) as KPI_Value from( select g3ManagedElement, UTC_DATETIME_ID, sum(ISNULL(MtasMmtTermNetworkSuccessSessionEstablish,0)) as MtasMmtTermNetworkSuccessSessionEstablish, sum(ISNULL(MtasMmtTermUnregNetworkSuccessSessionEstablish,0)) as MtasMmtTermUnregNetworkSuccessSessionEstablish FROM DC_E_MTAS_MTASMMT_RAW where UTC_DATETIME_ID = dt and g3ManagedElement = node_id group by g3ManagedElement, UTC_DATETIME_ID) as Success,(select g3ManagedElement, MOID, UTC_DATETIME_ID, MtasMmtTermFailedAttemptCause as MtasMmtTermFailedAttemptCause_403, MtasMmtTermUnregFailedAttemptCause as MtasMmtTermUnregFailedAttemptCause_403 FROM DC_E_MTAS_MTASMMT_RAW where UTC_DATETIME_ID = dt and g3ManagedElement = node_id and MOID like '403%%') as _403,(select g3ManagedElement, MOID, UTC_DATETIME_ID, MtasMmtTermFailedAttemptCause as MtasMmtTermFailedAttemptCause_404, MtasMmtTermUnregFailedAttemptCause as MtasMmtTermUnregFailedAttemptCause_404 FROM DC_E_MTAS_MTASMMT_RAW where UTC_DATETIME_ID = dt and g3ManagedElement = node_id and MOID like '404%%') as _404,( select g3ManagedElement, MOID, UTC_DATETIME_ID, MtasMmtTermFailedAttemptCause as MtasMmtTermFailedAttemptCause_407, MtasMmtTermUnregFailedAttemptCause as MtasMmtTermUnregFailedAttemptCause_407 FROM DC_E_MTAS_MTASMMT_RAW where UTC_DATETIME_ID = dt and g3ManagedElement = node_id and MOID like '407%%') as _407,(select g3ManagedElement, MOID, UTC_DATETIME_ID, MtasMmtTermFailedAttemptCause as MtasMmtTermFailedAttemptCause_484, MtasMmtTermUnregFailedAttemptCause as MtasMmtTermUnregFailedAttemptCause_484 FROM DC_E_MTAS_MTASMMT_RAW where UTC_DATETIME_ID = dt and g3ManagedElement = node_id and MOID like '484%%') as _484,( select g3ManagedElement, MOID, UTC_DATETIME_ID, MtasMmtTermFailedAttemptCause as MtasMmtTermFailedAttemptCause_486, MtasMmtTermUnregFailedAttemptCause as MtasMmtTermUnregFailedAttemptCause_486 FROM DC_E_MTAS_MTASMMT_RAW where UTC_DATETIME_ID = dt and g3ManagedElement = node_id and MOID like '486%%') as _486,( select g3ManagedElement, MOID, UTC_DATETIME_ID, MtasMmtTermFailedAttemptCause as MtasMmtTermFailedAttemptCause_600, MtasMmtTermUnregFailedAttemptCause as MtasMmtTermUnregFailedAttemptCause_600 FROM DC_E_MTAS_MTASMMT_RAW where UTC_DATETIME_ID = dt and g3ManagedElement = node_id and MOID like '600%%') as _600,(select g3ManagedElement, UTC_DATETIME_ID, sum(ISNULL(MtasMmtTermFailedAttempt,0)) as MtasMmtTermFailedAttempt, sum(ISNULL(MtasMmtTermUnregFailedAttempt,0)) as MtasMmtTermUnregFailedAttempt FROM DC_E_MTAS_MTASMMT_RAW where UTC_DATETIME_ID = dt and g3ManagedElement = node_id group by g3ManagedElement, UTC_DATETIME_ID) as FailedAttempts,end; call calculate_kpi_4('%s', 'mtas_05');" %(SQLConfig[1])
        else:
            sourceSQL="drop procedure if exists calculate_kpi_4; create procedure calculate_kpi_4( in dt datetime, in node_id varchar(35)) begin select Success.g3ManagedElement as g3ManagedElement, Success.UTC_DATETIME_ID as UTC_DATETIME_ID, 100 * ( ISNULL(MtasMmtTermNetworkSuccessSessionEstablish,0) + ISNULL(MtasMmtTermUnregNetworkSuccessSessionEstablish,0) + ISNULL(MtasMmtTermFailedAttemptCause_403,0) + ISNULL(MtasMmtTermUnregFailedAttemptCause_403,0) + ISNULL(MtasMmtTermFailedAttemptCause_404,0) + ISNULL(MtasMmtTermUnregFailedAttemptCause_404,0) + ISNULL(MtasMmtTermFailedAttemptCause_407,0) + ISNULL(MtasMmtTermUnregFailedAttemptCause_407,0) + ISNULL(MtasMmtTermFailedAttemptCause_484,0) + ISNULL(MtasMmtTermUnregFailedAttemptCause_484,0) + ISNULL(MtasMmtTermFailedAttemptCause_486,0) + ISNULL(MtasMmtTermUnregFailedAttemptCause_486,0) + ISNULL(MtasMmtTermFailedAttemptCause_600,0) + ISNULL(MtasMmtTermUnregFailedAttemptCause_600,0))/( ISNULL(MtasMmtTermNetworkSuccessSessionEstablish,0) + ISNULL(MtasMmtTermUnregNetworkSuccessSessionEstablish,0) + ISNULL(MtasMmtTermFailedAttempt,0) + ISNULL(MtasMmtTermUnregFailedAttempt,0)) as KPI_Value from( select g3ManagedElement, UTC_DATETIME_ID, sum(ISNULL(MtasMmtTermNetworkSuccessSessionEstablish,0)) as MtasMmtTermNetworkSuccessSessionEstablish, sum(ISNULL(MtasMmtTermUnregNetworkSuccessSessionEstablish,0)) as MtasMmtTermUnregNetworkSuccessSessionEstablish FROM DC_E_MTAS_MTASMMT_RAW where UTC_DATETIME_ID = dt and g3ManagedElement = node_id group by g3ManagedElement, UTC_DATETIME_ID) as Success,(select g3ManagedElement, MOID, UTC_DATETIME_ID, MtasMmtTermFailedAttemptCause as MtasMmtTermFailedAttemptCause_403, MtasMmtTermUnregFailedAttemptCause as MtasMmtTermUnregFailedAttemptCause_403 FROM DC_E_MTAS_MTASMMT_RAW where UTC_DATETIME_ID = dt and g3ManagedElement = node_id and MOID like '403%%') as _403,(select g3ManagedElement, MOID, UTC_DATETIME_ID, MtasMmtTermFailedAttemptCause as MtasMmtTermFailedAttemptCause_404, MtasMmtTermUnregFailedAttemptCause as MtasMmtTermUnregFailedAttemptCause_404 FROM DC_E_MTAS_MTASMMT_RAW where UTC_DATETIME_ID = dt and g3ManagedElement = node_id and MOID like '404%%') as _404,( select g3ManagedElement, MOID, UTC_DATETIME_ID, MtasMmtTermFailedAttemptCause as MtasMmtTermFailedAttemptCause_407, MtasMmtTermUnregFailedAttemptCause as MtasMmtTermUnregFailedAttemptCause_407 FROM DC_E_MTAS_MTASMMT_RAW where UTC_DATETIME_ID = dt and g3ManagedElement = node_id and MOID like '407%%') as _407,(select g3ManagedElement, MOID, UTC_DATETIME_ID, MtasMmtTermFailedAttemptCause as MtasMmtTermFailedAttemptCause_484, MtasMmtTermUnregFailedAttemptCause as MtasMmtTermUnregFailedAttemptCause_484 FROM DC_E_MTAS_MTASMMT_RAW where UTC_DATETIME_ID = dt and g3ManagedElement = node_id and MOID like '484%%') as _484,( select g3ManagedElement, MOID, UTC_DATETIME_ID, MtasMmtTermFailedAttemptCause as MtasMmtTermFailedAttemptCause_486, MtasMmtTermUnregFailedAttemptCause as MtasMmtTermUnregFailedAttemptCause_486 FROM DC_E_MTAS_MTASMMT_RAW where UTC_DATETIME_ID = dt and g3ManagedElement = node_id and MOID like '486%%') as _486,( select g3ManagedElement, MOID, UTC_DATETIME_ID, MtasMmtTermFailedAttemptCause as MtasMmtTermFailedAttemptCause_600, MtasMmtTermUnregFailedAttemptCause as MtasMmtTermUnregFailedAttemptCause_600 FROM DC_E_MTAS_MTASMMT_RAW where UTC_DATETIME_ID = dt and g3ManagedElement = node_id and MOID like '600%%') as _600,(select g3ManagedElement, UTC_DATETIME_ID, sum(ISNULL(MtasMmtTermFailedAttempt,0)) as MtasMmtTermFailedAttempt, sum(ISNULL(MtasMmtTermUnregFailedAttempt,0)) as MtasMmtTermUnregFailedAttempt FROM DC_E_MTAS_MTASMMT_RAW where UTC_DATETIME_ID = dt and g3ManagedElement = node_id group by g3ManagedElement, UTC_DATETIME_ID) as FailedAttempts,end; call calculate_kpi_4('%s', '%s');" %(SQLConfig[1],SQLConfig[2])
#4b

#5a
    elif SQLConfig[0] =='5':
        if noNode==1:
            sourceSQL="select g3ManagedElement,UTC_DATETIME_ID,100*sum(A)*sum(B) KPI_VALUE from(select UTC_DATETIME_ID,g3ManagedElement, OSS_ID,((ISNULL(MtasSccInitOrigSessCsOk,0)+ISNULL(MtasSccInitOrigUnregSessCsOk,0))/(ISNULL(MtasSccInitOrigSessCsOk,0)+ISNULL(MtasSccInitOrigUnregSessCsOk,0)+ISNULL(MtasSccInitOrigSessCsNOkE,0)+ISNULL(MtasSccInitOrigSessCsNOkI,0)+ISNULL(MtasSccInitOrigUnregSessCsNOkI,0)+ISNULL(MtasSccInitOrigUnregSessCsNOkE,0))) as A,0.0 as B from DC_E_MTAS_MTASSCC_RAW where  UTC_DATETIME_ID ='%s' union all select UTC_DATETIME_ID,g3ManagedElement, OSS_ID,0.0 as A ,((MtasSdsCapInitDPOk)/(MtasSdsCapInitDPOk+MtasSdsCapInitDPNOkE+MtasSdsCapInitDPNOkI)) as B from DC_E_MTAS_MTASSDS_RAW where  UTC_DATETIME_ID ='%s') as xx group by UTC_DATETIME_ID,g3ManagedElement order by UTC_DATETIME_ID, g3ManagedElement" %(SQLConfig[1],SQLConfig[1])
        else:
            sourceSQL="select g3ManagedElement,UTC_DATETIME_ID,100*sum(A)*sum(B) KPI_VALUE from(select UTC_DATETIME_ID,g3ManagedElement, OSS_ID,((ISNULL(MtasSccInitOrigSessCsOk,0)+ISNULL(MtasSccInitOrigUnregSessCsOk,0))/(ISNULL(MtasSccInitOrigSessCsOk,0)+ISNULL(MtasSccInitOrigUnregSessCsOk,0)+ISNULL(MtasSccInitOrigSessCsNOkE,0)+ISNULL(MtasSccInitOrigSessCsNOkI,0)+ISNULL(MtasSccInitOrigUnregSessCsNOkI,0)+ISNULL(MtasSccInitOrigUnregSessCsNOkE,0))) as A,0.0 as B from DC_E_MTAS_MTASSCC_RAW where  UTC_DATETIME_ID ='%s' and g3ManagedElement='%s' union all select UTC_DATETIME_ID,g3ManagedElement, OSS_ID,0.0 as A ,((MtasSdsCapInitDPOk)/(MtasSdsCapInitDPOk+MtasSdsCapInitDPNOkE+MtasSdsCapInitDPNOkI)) as B from DC_E_MTAS_MTASSDS_RAW where  UTC_DATETIME_ID ='%s' and g3ManagedElement='%s') as xx group by UTC_DATETIME_ID,g3ManagedElement order by UTC_DATETIME_ID, g3ManagedElement" %(SQLConfig[1],SQLConfig[2],SQLConfig[1],SQLConfig[2])
#5b

#6a 
    elif SQLConfig[0] =='6':
        if noNode==1:
            sourceSQL="select GGSN, OSS_ID,AVG( ( (ISNULL(pgwApnAttemptedEpsBearerActivation,0))-(ISNULL(pgwApnCompletedEpsBearerActivation,0)) )/(ISNULL(pgwApnAttemptedEpsBearerActivation,0)) ) as KPI_VALUE from DC_E_GGSN_APN_RAW where UTC_DATETIME_ID ='%s' group by ggsn,OSS_ID" %(SQLConfig[1])
        else:
            sourceSQL="select GGSN, OSS_ID,AVG( ( (ISNULL(pgwApnAttemptedEpsBearerActivation,0))-(ISNULL(pgwApnCompletedEpsBearerActivation,0)) )/(ISNULL(pgwApnAttemptedEpsBearerActivation,0)) ) as KPI_VALUE from DC_E_GGSN_APN_RAW where UTC_DATETIME_ID ='%s' and GGSN='%s' group by ggsn,OSS_ID" %(SQLConfig[1],SQLConfig[2])
#6b

#7a    
    elif SQLConfig[0] =='7':
        if noNode==1:
            sourceSQL="SELECT NE_NAME,OSS_ID,UTC_DATETIME_ID, 100 * ( (counter3.total)/((counter3.total) + (counter2.total) - counter1.total) ) AS 'KPI_Value' FROM dc.DC_E_CSCF_REG_RAW, (select sum(ISNULL(scscfThirdPartyRegistrationSuccess,0)) total from dc.DC_E_CSCF_REG_RAW where NE_NAME='cscf_05' and UTC_DATETIME_ID='%s') as counter3, (select sum(ISNULL(scscfThirdPartyRegistrationFailure,0)) total from dc.DC_E_CSCF_REG_RAW where NE_NAME='cscf_05' and MOID='401' and UTC_DATETIME_ID='%s') as counter1,(select sum(ISNULL(scscfThirdPartyRegistrationFailure,0)) total from dc.DC_E_CSCF_REG_RAW where NE_NAME='cscf_05' and MOID='sum' and UTC_DATETIME_ID='%s') as counter2 WHERE UTC_DATETIME_ID='%s' and NE_NAME='cscf_05'" %(SQLConfig[1],SQLConfig[1],SQLConfig[1],SQLConfig[1])	#edit- there was duplication in this line, line X2.
        else:
            sourceSQL="SELECT NE_NAME,OSS_ID,UTC_DATETIME_ID,100 * ( (counter3.total)/((counter3.total) + (counter2.total) - counter1.total) ) AS 'KPI_Value' FROM dc.DC_E_CSCF_REG_RAW, (select sum(ISNULL(scscfThirdPartyRegistrationSuccess,0)) total from dc.DC_E_CSCF_REG_RAW where NE_NAME='%s' and UTC_DATETIME_ID='%s') as counter3, (select sum(ISNULL(scscfThirdPartyRegistrationFailure,0)) total from dc.DC_E_CSCF_REG_RAW where NE_NAME='%s' and MOID='401' and UTC_DATETIME_ID='%s') as counter1,(select sum(ISNULL(scscfThirdPartyRegistrationFailure,0)) total from dc.DC_E_CSCF_REG_RAW where NE_NAME='%s' and MOID='sum' and UTC_DATETIME_ID='%s') as counter2 WHERE UTC_DATETIME_ID='%s' and NE_NAME='%s' SELECT NE_NAME,OSS_ID,UTC_DATETIME_ID,100 * ( (counter3.total)/((counter3.total) + (counter2.total) - counter1.total) ) AS 'KPI_Value' FROM dc.DC_E_CSCF_REG_RAW, (select sum(ISNULL(scscfThirdPartyRegistrationSuccess,0)) total from dc.DC_E_CSCF_REG_RAW where NE_NAME='%s' and UTC_DATETIME_ID='%s') as counter3, (select sum(ISNULL(scscfThirdPartyRegistrationFailure,0)) total from dc.DC_E_CSCF_REG_RAW where NE_NAME='%s' and MOID='401' and UTC_DATETIME_ID='%s') as counter1,(select sum(ISNULL(scscfThirdPartyRegistrationFailure,0)) total from dc.DC_E_CSCF_REG_RAW where NE_NAME='%s' and MOID='sum' and UTC_DATETIME_ID='%s') as counter2 WHERE UTC_DATETIME_ID='%s' and NE_NAME='%s'" %(SQLConfig[2],SQLConfig[1],SQLConfig[2],SQLConfig[1],SQLConfig[2],SQLConfig[1],SQLConfig[1],SQLConfig[2],SQLConfig[2],SQLConfig[1],SQLConfig[2],SQLConfig[1],SQLConfig[2],SQLConfig[1],SQLConfig[1],SQLConfig[2])
#7b

#8a
    elif SQLConfig[0] =='8':
        if noNode==1:
            sourceSQL="select NE_ID, OSS_ID,100*avg((ISNULL(sbgSipRegStatInitialAccCnt,0)+ISNULL(sbgSipRegStatRejInitialRegCnt400,0)+ISNULL(sbgSipRegStatRejInitialRegCnt403,0))/ISNULL(sbgSipRegStatInitialAttCnt,0)) as KPI_VALUE from DC_E_IMSSBG_PROXYREGISTRAR_RAW where UTC_DATETIME_ID ='%s' group by NE_ID, UTC_DATETIME_ID,OSS_ID order by ne_id" %(SQLConfig[1])
        else:
            sourceSQL="select NE_ID, OSS_ID,100*avg((ISNULL(sbgSipRegStatInitialAccCnt,0)+ISNULL(sbgSipRegStatRejInitialRegCnt400,0)+ISNULL(sbgSipRegStatRejInitialRegCnt403,0))/ISNULL(sbgSipRegStatInitialAttCnt,0)) as KPI_VALUE from DC_E_IMSSBG_PROXYREGISTRAR_RAW where UTC_DATETIME_ID ='%s' and NE_ID='%s' group by NE_ID, UTC_DATETIME_ID,OSS_ID order by ne_id" %(SQLConfig[1],SQLConfig[2])
#8b
    
#9a    
    elif SQLConfig[0] =='9':
        if noNode==1:
            sourceSQL="select OSS_ID, g3ManagedElement,100*(avg((ISNULL(MtasFuncTermOrigSessOk,0)+ISNULL(MtasFuncTermOrigSessNOkE,0))/(ISNULL(MtasFuncTermOrigSessOk,0)+ISNULL(MtasFuncTermOrigSessNOkI,0)+ISNULL(MtasFuncTermOrigSessNOkE,0)))) as KPI_VALUE from DC_E_MTAS_MTASQOS_RAW where  UTC_DATETIME_ID ='%s' group by OSS_ID, g3ManagedElement ORDER BY g3ManagedElement"%(SQLConfig[1])
        else:
            sourceSQL="select OSS_ID, g3ManagedElement,100*(avg((ISNULL(MtasFuncTermOrigSessOk,0)+ISNULL(MtasFuncTermOrigSessNOkE,0))/(ISNULL(MtasFuncTermOrigSessOk,0)+ISNULL(MtasFuncTermOrigSessNOkI,0)+ISNULL(MtasFuncTermOrigSessNOkE,0)))) as KPI_VALUE from DC_E_MTAS_MTASQOS_RAW where  UTC_DATETIME_ID ='%s' and g3ManagedElement='%s' group by OSS_ID, g3ManagedElement ORDER BY g3ManagedElement"%(SQLConfig[1],SQLConfig[2])
#9b
    
#10a
    elif SQLConfig[0] =='10':
        if noNode==1:
            sourceSQL="select OSS_ID, g3ManagedElement,100*(avg(( ISNULL(MtasFuncTermTermSessOk,0) + ISNULL(MtasFuncTermTermSessNOkE,0))/(ISNULL(MtasFuncTermTermSessOk,0)+ISNULL(MtasFuncTermTermSessNOkI,0)+ISNULL(MtasFuncTermTermSessNOkE,0)))) as KPI_VALUE from DC_E_MTAS_MTASQOS_RAW where UTC_DATETIME_ID ='%s' group by OSS_ID, g3ManagedElement ORDER BY g3ManagedElement"%(SQLConfig[1])
        else:
            sourceSQL="select OSS_ID, g3ManagedElement,100*(avg(( ISNULL(MtasFuncTermTermSessOk,0) + ISNULL(MtasFuncTermTermSessNOkE,0))/(ISNULL(MtasFuncTermTermSessOk,0)+ISNULL(MtasFuncTermTermSessNOkI,0)+ISNULL(MtasFuncTermTermSessNOkE,0)))) as KPI_VALUE from DC_E_MTAS_MTASQOS_RAW where UTC_DATETIME_ID ='%s' and g3ManagedElement='%s' group by OSS_ID, g3ManagedElement ORDER BY g3ManagedElement"%(SQLConfig[1],SQLConfig[2])
#10b

#11a
    elif SQLConfig[0] =='11':
        if noNode==1:
            sourceSQL="select UTC_DATETIME_ID, NE_ID, OSS_ID, 100*avg((ISNULL(sbgSipSuccessIncSessions,0)-ISNULL(sbgSipRejectedIncAlertingSessions488,0)-ISNULL(sbgSipRejectedIncPreAlertingSessions488,0))/ISNULL(sbgSipTotalIncSessSetups,0)) as KPI_VALUE from DC_E_IMSSBG_SIP_RAW where UTC_DATETIME_ID ='%s' GROUP BY UTC_DATETIME_ID, NE_ID, OSS_ID order by ne_id" %(SQLConfig[1])
        else:
            sourceSQL="select UTC_DATETIME_ID, NE_ID, OSS_ID, 100*avg((ISNULL(sbgSipSuccessIncSessions,0)-ISNULL(sbgSipRejectedIncAlertingSessions488,0)-ISNULL(sbgSipRejectedIncPreAlertingSessions488,0))/ISNULL(sbgSipTotalIncSessSetups,0)) as KPI_VALUE from DC_E_IMSSBG_SIP_RAW where UTC_DATETIME_ID ='%s' and NE_ID='%s' GROUP BY UTC_DATETIME_ID, NE_ID, OSS_ID order by ne_id" %(SQLConfig[1],SQLConfig[2])
#11b

#12a
    elif SQLConfig[0] =='12':
        if noNode==1:
            sourceSQL="select SGSN, OSS_ID, isnull((VS_MM_SrvccCsOnlyToWAtt_E - VS_MM_SrvccCsOnlyToWSucc_E + VS_MM_SrvccCsAndPsToWAtt_E - VS_MM_SrvccCsAndPsToWSucc_E - VS_MM_SrvccCsAndPsToWCsSuccPsFailed_E)/(VS_MM_SrvccCsOnlyToWAtt_E + VS_MM_SrvccCsAndPsToWAtt_E),(VS_MM_SrvccCsOnlyToWAtt_E - VS_MM_SrvccCsOnlyToWSucc_E)/(VS_MM_SrvccCsOnlyToWAtt_E),(VS_MM_SrvccCsAndPsToWAtt_E - VS_MM_SrvccCsAndPsToWSucc_E - VS_MM_SrvccCsAndPsToWCsSuccPsFailed_E)/(VS_MM_SrvccCsAndPsToWAtt_E)) as KPI_Value from DC_E_SGSNMME_MOBILITY_MM_E_RAW where UTC_DATETIME_ID='%s'" %(SQLConfig[1])
        else:
            sourceSQL="select SGSN, OSS_ID, isnull((VS_MM_SrvccCsOnlyToWAtt_E - VS_MM_SrvccCsOnlyToWSucc_E + VS_MM_SrvccCsAndPsToWAtt_E - VS_MM_SrvccCsAndPsToWSucc_E - VS_MM_SrvccCsAndPsToWCsSuccPsFailed_E)/(VS_MM_SrvccCsOnlyToWAtt_E + VS_MM_SrvccCsAndPsToWAtt_E),(VS_MM_SrvccCsOnlyToWAtt_E - VS_MM_SrvccCsOnlyToWSucc_E)/(VS_MM_SrvccCsOnlyToWAtt_E),(VS_MM_SrvccCsAndPsToWAtt_E - VS_MM_SrvccCsAndPsToWSucc_E - VS_MM_SrvccCsAndPsToWCsSuccPsFailed_E)/(VS_MM_SrvccCsAndPsToWAtt_E)) as KPI_Value from DC_E_SGSNMME_MOBILITY_MM_E_RAW where UTC_DATETIME_ID='%s' and SGSN='%s'" %(SQLConfig[1],SQLConfig[2])
#12b

#13a
    elif SQLConfig[0] =='13':
        if noNode==1:
            sourceSQL="select SGSN, OSS_ID, ((ISNULL(VS_MM_SrvccCsOnlyToGAtt_E,0)-ISNULL(VS_MM_SrvccCsOnlyToGSucc_E,0))/ISNULL(VS_MM_SrvccCsOnlyToGAtt_E,0)) as KPI_VALUE from DC_E_SGSNMME_MOBILITY_MM_E_RAW where UTC_DATETIME_ID='%s' GROUP BY SGSN,OSS_ID,VS_MM_SrvccCsOnlyToGAtt_E,VS_MM_SrvccCsOnlyToGSucc_E" %(SQLConfig[1])
        else:
            sourceSQL="select SGSN, OSS_ID, ((ISNULL(VS_MM_SrvccCsOnlyToGAtt_E,0)-ISNULL(VS_MM_SrvccCsOnlyToGSucc_E,0))/ISNULL(VS_MM_SrvccCsOnlyToGAtt_E,0)) as KPI_VALUE from DC_E_SGSNMME_MOBILITY_MM_E_RAW where UTC_DATETIME_ID='%s' and SGSN='%s' GROUP BY SGSN,OSS_ID,VS_MM_SrvccCsOnlyToGAtt_E,VS_MM_SrvccCsOnlyToGSucc_E ORDER BY SGSN" %(SQLConfig[1],SQLConfig[2])
#13b

#14a 
    elif SQLConfig[0] =='14':
        if noNode==1:
            sourceSQL="select oss_id, sn, UTC_DATETIME_ID, regexp_substr(elem, '([^,]+)') as ELEM, 100*avg(ISNULL(P2CCOMPLACK,0)/ISNULL(P2CREQUTOT,0)) as KPI_VALUE  from DC_E_CNAXE_MMESTAT_RAW where UTC_DATETIME_ID= '%s' and statistics_type <> 'CLUSTER' group by oss_id, sn, elem, UTC_DATETIME_ID" %(SQLConfig[1])
        else:
            sourceSQL="select oss_id, sn, UTC_DATETIME_ID, regexp_substr(elem, '([^,]+)') as ELEM, 100*avg(ISNULL(P2CCOMPLACK,0)/ISNULL(P2CREQUTOT,0)) as KPI_VALUE  from DC_E_CNAXE_MMESTAT_RAW where UTC_DATETIME_ID= '%s' and sn='%s' and statistics_type <> 'CLUSTER' group by oss_id, sn, elem, UTC_DATETIME_ID" %(SQLConfig[1],SQLConfig[2])
#14b

#15a
    elif SQLConfig[0] =='15':
        if noNode==1:
            sourceSQL="select UTC_DATETIME_ID, oss_id, regexp_substr(elem, '([^,]+)') as ELEM, 100 * sum(ISNULL(P2CCOMPLACK,0)) / sum (ISNULL(P2CREQUTOT,0)) as KPI_VALUE from DC_E_CNAXE_MMESTAT_RAW where UTC_DATETIME_ID='%s' group by UTC_DATETIME_ID, oss_id, elem order by elem" %(SQLConfig[1])
        else:
            sourceSQL="select UTC_DATETIME_ID, oss_id, regexp_substr(elem, '([^,]+)') as ELEM, 100 * sum(ISNULL(P2CCOMPLACK,0)) / sum (ISNULL(P2CREQUTOT,0)) as KPI_VALUE from DC_E_CNAXE_MMESTAT_RAW where UTC_DATETIME_ID='%s' and elem='%s' group by UTC_DATETIME_ID, oss_id, elem order by elem" %(SQLConfig[1],SQLConfig[2])
#15b

#16a
    elif SQLConfig[0] =='16':
        if noNode==1:
            sourceSQL="select UTC_DATETIME_ID, oss_id, sn, left(elem, (case when charindex(',', ELEM)=0 then length(elem) when charindex(',', ELEM)>0 then charindex(',', ELEM)-1 end)) as ELEM, 100*avg(ISNULL(SRVCC2U_NRELREQSUCC,0)/ISNULL(SRVCC2U_NRELREQTOT,0)) as KPI_VALUE from DC_E_CNAXE_MSC_RAW where UTC_DATETIME_ID='%s' and statistics_type <> 'CLUSTER' group by oss_id, sn, elem, UTC_DATETIME_ID" %(SQLConfig[1])
        else:
            sourceSQL="select UTC_DATETIME_ID, oss_id, sn, left(elem, (case when charindex(',', ELEM)=0 then length(elem) when charindex(',', ELEM)>0 then charindex(',', ELEM)-1 end)) as ELEM, 100*avg(ISNULL(SRVCC2U_NRELREQSUCC,0)/ISNULL(SRVCC2U_NRELREQTOT,0)) as KPI_VALUE from DC_E_CNAXE_MSC_RAW where UTC_DATETIME_ID='%s' and statistics_type <> 'CLUSTER' and ELEM='%s' group by oss_id, sn, elem, UTC_DATETIME_ID" %(SQLConfig[1],SQLConfig[2])
#16b

#17a
    elif SQLConfig[0] =='17':
        if noNode==1:
            sourceSQL="select oss_id, sn, UTC_DATETIME_ID, regexp_substr(elem, '([^,]+)') as ELEM, 100*sum(ISNULL(NBRMSCS2U_NS2UASUCC,0))/sum(ISNULL(NBRMSCS2U_NS2UATOT,0)) as KPI_VALUE  from DC_E_CNAXE_MSCOBJ_RAW where UTC_DATETIME_ID='%s' and statistics_type <> 'CLUSTER' group by oss_id, sn, elem, UTC_DATETIME_ID"%(SQLConfig[1])
        else:
            sourceSQL="select oss_id, sn, UTC_DATETIME_ID, regexp_substr(elem, '([^,]+)') as ELEM, 100*sum(ISNULL(NBRMSCS2U_NS2UASUCC,0))/sum(ISNULL(NBRMSCS2U_NS2UATOT,0)) as KPI_VALUE  from DC_E_CNAXE_MSCOBJ_RAW where UTC_DATETIME_ID='%s' and elem='%s' and statistics_type <> 'CLUSTER' group by oss_id, sn, elem, UTC_DATETIME_ID"%(SQLConfig[1],SQLConfig[2])
#17b
    
#18a
    elif SQLConfig[0] =='18':
        if noNode==1:
            sourceSQL="select NE_ID, OSS_ID,AVG(ISNULL(sbgSipNetIncSessionSetupTime,0)/ISNULL(sbgSipNetIncSessionSetupUserSuccess,0))as KPI_VALUE from DC_E_IMSSBG_SIP_RAW where UTC_DATETIME_ID ='%s' GROUP BY UTC_DATETIME_ID, NE_ID, OSS_ID order by ne_id"%(SQLConfig[1])
        else:
            sourceSQL="select NE_ID, OSS_ID,AVG(ISNULL(sbgSipNetIncSessionSetupTime,0)/ISNULL(sbgSipNetIncSessionSetupUserSuccess,0))as KPI_VALUE from DC_E_IMSSBG_SIP_RAW where UTC_DATETIME_ID ='%s' and NE_ID= '%s' GROUP BY UTC_DATETIME_ID, NE_ID, OSS_ID order by ne_id"%(SQLConfig[1],SQLConfig[2])
#18b

#19a
    elif SQLConfig[0] =='19':
        if noNode==1:
            sourceSQL="select NE_ID, OSS_ID,AVG(ISNULL(sbgSipNetOutSessionSetupTime,0)/ISNULL(sbgSipNetOutSessionSetupUserSuccess,0))as KPI_VALUE from DC_E_IMSSBG_SIP_RAW where UTC_DATETIME_ID ='%s' GROUP BY UTC_DATETIME_ID, NE_ID, OSS_ID order by ne_id"%(SQLConfig[1])
        else:
            sourceSQL="select NE_ID, OSS_ID,AVG(ISNULL(sbgSipNetOutSessionSetupTime,0)/ISNULL(sbgSipNetOutSessionSetupUserSuccess,0))as KPI_VALUE from DC_E_IMSSBG_SIP_RAW where UTC_DATETIME_ID ='%s' and NE_ID ='%s' GROUP BY UTC_DATETIME_ID, NE_ID, OSS_ID order by ne_id"%(SQLConfig[1],SQLConfig[2])
#19b
    
#20a
    elif SQLConfig[0] =='20':
        if noNode==1:
            sourceSQL="select NE_ID, OSS_ID,AVG(ISNULL(sbgInitRegTime,0)/ISNULL(sbgSipRegStatInitialAccCnt,0))as KPI_VALUE from DC_E_IMSSBG_PROXYREGISTRAR_RAW where UTC_DATETIME_ID ='%s' GROUP BY UTC_DATETIME_ID, NE_ID, OSS_ID order by ne_id"%(SQLConfig[1])
        else:
            sourceSQL="select NE_ID, OSS_ID,AVG(ISNULL(sbgInitRegTime,0)/ISNULL(sbgSipRegStatInitialAccCnt,0))as KPI_VALUE from DC_E_IMSSBG_PROXYREGISTRAR_RAW where UTC_DATETIME_ID ='%s' and NE_ID='%s' GROUP BY UTC_DATETIME_ID, NE_ID, OSS_ID order by ne_id"%(SQLConfig[1],SQLConfig[2])
#20b

#21a
    elif SQLConfig[0] =='21':
        if noNode==1:
            sourceSQL="select UTC_DATETIME_ID , SGSN ,( ISNULL(VS_MM_SrvccCsOnlyToWAtt_E,0)+ISNULL(VS_MM_SrvccCsAndPsToWAtt_E,0)) AS KPI_VALUE from DC_E_SGSNMME_MOBILITY_MM_E_RAW where UTC_DATETIME_ID='%s' order by SGSN"%(SQLConfig[1])
        else:
            sourceSQL="select UTC_DATETIME_ID , SGSN ,( ISNULL(VS_MM_SrvccCsOnlyToWAtt_E,0)+ISNULL(VS_MM_SrvccCsAndPsToWAtt_E,0)) AS KPI_VALUE from DC_E_SGSNMME_MOBILITY_MM_E_RAW where UTC_DATETIME_ID='%s' and SGSN='%s' order by SGSN"%(SQLConfig[1],SQLConfig[2])
#21b
    
#22a
    elif SQLConfig[0] =='22':
        if noNode==1:
            sourceSQL="select NE_ID, OSS_ID,sum(ISNULL(sbgSipRespondedIncSessions,0))as KPI_VALUE from  DC_E_IMSSBG_SIP_RAW where UTC_DATETIME_ID ='%s' GROUP BY UTC_DATETIME_ID, NE_ID, OSS_ID order by ne_id"%(SQLConfig[1])
        else:
            sourceSQL="select NE_ID, OSS_ID,sum(ISNULL(sbgSipRespondedIncSessions,0))as KPI_VALUE from  DC_E_IMSSBG_SIP_RAW where UTC_DATETIME_ID ='%s' and NE_ID='%s' GROUP BY UTC_DATETIME_ID, NE_ID, OSS_ID order by ne_id"%(SQLConfig[1],SQLConfig[2])
#22b

#23a
    elif SQLConfig[0] =='23':
        if noNode==1:
            sourceSQL="select NE_ID, OSS_ID,avg(ISNULL(sbgSgcPktsLostRatioGauge,0))/100 as KPI_VALUE from  DC_E_IMSSBG_NETWORKQOS_RAW where UTC_DATETIME_ID ='%s' GROUP BY UTC_DATETIME_ID, NE_ID, OSS_ID order by ne_id"%(SQLConfig[1])
        else:
            sourceSQL="select NE_ID, OSS_ID,avg(ISNULL(sbgSgcPktsLostRatioGauge,0))/100 as KPI_VALUE from  DC_E_IMSSBG_NETWORKQOS_RAW where UTC_DATETIME_ID ='%s' and NE_ID='%s' GROUP BY UTC_DATETIME_ID, NE_ID, OSS_ID order by ne_id"%(SQLConfig[1],SQLConfig[2])
#23b

#24a
    elif SQLConfig[0] =='24':
        if noNode==1:
            sourceSQL=" select oss_id, ERBS, utc_datetime_id, 100 * avg(KPI_VALUE) as KPI_VALUE FROM (select oss_id, ERBS, utc_datetime_id, avg(ISNULL(pmVoipQualityRbUlOk,0) / (ISNULL(pmVoipQualityRbUlOk,0) + ISNULL(pmVoipQualityRbUlNOk,0)) ) as KPI_VALUE from DC_E_ERBS_EUTRANCELLFDD_RAW group by ERBS, utc_datetime_id, oss_id union select oss_id, ERBS, utc_datetime_id, avg( pmVoipQualityRbUlOk / (pmVoipQualityRbUlOk + pmVoipQualityRbUlNOk) ) as KPI_VALUE from DC_E_ERBS_EUTRANCELLTDD_RAW group by ERBS, utc_datetime_id, oss_id) as KPI where utc_datetime_id = '%s' group by ERBS, oss_id, utc_datetime_id order by erbs" %(SQLConfig[1])
        else:
            sourceSQL=" select oss_id, ERBS, utc_datetime_id, 100 * avg(KPI_VALUE) as KPI_VALUE FROM (select oss_id, ERBS, utc_datetime_id, avg(ISNULL(pmVoipQualityRbUlOk,0) / (ISNULL(pmVoipQualityRbUlOk,0) + ISNULL(pmVoipQualityRbUlNOk,0)) ) as KPI_VALUE from DC_E_ERBS_EUTRANCELLFDD_RAW group by ERBS, utc_datetime_id, oss_id union select oss_id, ERBS, utc_datetime_id, avg( pmVoipQualityRbUlOk / (pmVoipQualityRbUlOk + pmVoipQualityRbUlNOk) ) as KPI_VALUE from DC_E_ERBS_EUTRANCELLTDD_RAW group by ERBS, utc_datetime_id, oss_id) as KPI where utc_datetime_id = '%s'  and erbs='%s' group by ERBS, oss_id, utc_datetime_id order by erbs" %(SQLConfig[1],SQLConfig[2])
#24b

#25a
    elif SQLConfig[0] =='25':
        if noNode==1:
            sourceSQL="select OSS_ID, g3ManagedElement,100*(ISNULL(MtasPriorityCallWpsEstablished,0)/ISNULL(MtasPriorityCallWpsRequested,0)) as KPI_VALUE from DC_E_MTAS_MTASPRIORITYCALL_RAW where UTC_DATETIME_ID ='%s' ORDER BY g3ManagedElement"%(SQLConfig[1])
        else:
            sourceSQL="select OSS_ID, g3ManagedElement,100*(ISNULL(MtasPriorityCallWpsEstablished,0)/ISNULL(MtasPriorityCallWpsRequested,0)) as KPI_VALUE from DC_E_MTAS_MTASPRIORITYCALL_RAW where UTC_DATETIME_ID ='%s' and g3ManagedElement='%s' ORDER BY g3ManagedElement"%(SQLConfig[1],SQLConfig[2])
#25b

#26a
    elif SQLConfig[0] =='26':
        if noNode==1:
            sourceSQL="select NE_ID, OSS_ID,100*avg(ISNULL(sbgSgcIncPriorityCallSuccessSetups,0)/ISNULL(sbgSgcIncPriorityCallAttempts,0)) as KPI_VALUE from  DC_E_IMSSBG_SIGNWCN_RAW where UTC_DATETIME_ID ='%s' GROUP BY UTC_DATETIME_ID, NE_ID, OSS_ID order by ne_id"%(SQLConfig[1])
        else:
            sourceSQL="select NE_ID, OSS_ID,100*avg(ISNULL(sbgSgcIncPriorityCallSuccessSetups,0)/ISNULL(sbgSgcIncPriorityCallAttempts,0)) as KPI_VALUE from  DC_E_IMSSBG_SIGNWCN_RAW where UTC_DATETIME_ID ='%s' and NE_ID ='%s' GROUP BY UTC_DATETIME_ID, NE_ID, OSS_ID order by ne_id"%(SQLConfig[1],SQLConfig[2])
#26b

#27a
    elif SQLConfig[0] =='27':
        if noNode==1:
            sourceSQL="select NE_ID, OSS_ID,100*avg(ISNULL(sbgSgcTotalEmergencyCallsSuccess,0)/ISNULL(sbgSgcTotalEmergencyCallsSetups,0)) as KPI_VALUE from  DC_E_IMSSBG_SIGNWCN_RAW where UTC_DATETIME_ID ='%s' GROUP BY UTC_DATETIME_ID, NE_ID, OSS_ID order by ne_id"%(SQLConfig[1])
        else:
            sourceSQL="select NE_ID, OSS_ID,100*avg(ISNULL(sbgSgcTotalEmergencyCallsSuccess,0)/ISNULL(sbgSgcTotalEmergencyCallsSetups,0)) as KPI_VALUE from  DC_E_IMSSBG_SIGNWCN_RAW where UTC_DATETIME_ID ='%s' and NE_ID='%s' GROUP BY UTC_DATETIME_ID, NE_ID, OSS_ID order by ne_id"%(SQLConfig[1],SQLConfig[2])
#27b

#28a
    elif SQLConfig[0] =='28':
        if noNode==1:
            sourceSQL="select NE_ID, OSS_ID,sum(ISNULL(sbgSipEmerRegStatInitialAccCnt,0)) as KPI_VALUE from  DC_E_IMSSBG_PROXYREGISTRAR_RAW where UTC_DATETIME_ID ='%s' GROUP BY UTC_DATETIME_ID, NE_ID, OSS_ID order by ne_id" %(SQLConfig[1])
        else:
            sourceSQL="select NE_ID, OSS_ID,sum(ISNULL(sbgSipEmerRegStatInitialAccCnt,0)) as KPI_VALUE from  DC_E_IMSSBG_PROXYREGISTRAR_RAW where UTC_DATETIME_ID ='%s' and NE_ID='%s' GROUP BY UTC_DATETIME_ID, NE_ID, OSS_ID order by ne_id" %(SQLConfig[1],SQLConfig[2])
#28b

#29a
    elif SQLConfig[0] =='29':
        if noNode==1:
            sourceSQL="select UTC_DATETIME_ID, ERBS, 100 * avg(KPI_VALUE) as KPI_VALUE from (select FACTOR_1.UTC_DATETIME_ID as UTC_DATETIME_ID, FACTOR_1.ERBS as ERBS, FACTOR_1.cell as cell, factor_1 * factor_2 * factor_3 as KPI_VALUE from (select UTC_DATETIME_ID, ERBS, cell, factor_1 from (select UTC_DATETIME_ID, ERBS, EUtranCellFDD as cell, (ISNULL(pmRrcConnEstabSuccMod,0) + ISNULL(pmRrcConnEstabSuccMta,0))/(ISNULL(pmRrcConnEstabAttMod,0) + ISNULL(pmRrcConnEstabAttMta,0) - ISNULL(pmRrcConnEstabAttReattMod,0) - ISNULL(pmRrcConnEstabAttReattMta,0) - ISNULL(pmRrcConnEstabFailMmeOvlMod,0)) as factor_1 from DC_E_ERBS_EUTRANCELLFDD_RAW union all select UTC_DATETIME_ID, ERBS, EUtranCellTDD as cell, (ISNULL(pmRrcConnEstabSuccMod,0) + ISNULL(pmRrcConnEstabSuccMta,0))/(ISNULL(pmRrcConnEstabAttMod,0) + ISNULL(pmRrcConnEstabAttMta,0) - ISNULL(pmRrcConnEstabAttReattMod,0) - ISNULL(pmRrcConnEstabAttReattMta,0) - ISNULL(pmRrcConnEstabFailMmeOvlMod,0)) as factor_1 from DC_E_ERBS_EUTRANCELLTDD_RAW) as KPI where UTC_DATETIME_ID = '%s') as FACTOR_1,(select UTC_DATETIME_ID, ERBS, cell, factor_2 from (select UTC_DATETIME_ID, ERBS, EUtranCellFDD as cell, (ISNULL(pmS1SigConnEstabSuccMod,0) + ISNULL(pmS1SigConnEstabSuccMta,0))/(ISNULL(pmS1SigConnEstabAttMod,0) + ISNULL(pmS1SigConnEstabAttMta,0)) as factor_2 from DC_E_ERBS_EUTRANCELLFDD_RAW union all select UTC_DATETIME_ID, ERBS, EUtranCellTDD as cell, (ISNULL(pmS1SigConnEstabSuccMod,0) + ISNULL(pmS1SigConnEstabSuccMta,0))/(ISNULL(pmS1SigConnEstabAttMod,0) + ISNULL(pmS1SigConnEstabAttMta,0)) as factor_2 from DC_E_ERBS_EUTRANCELLTDD_RAW) as KPI where UTC_DATETIME_ID = '%s') as FACTOR_2,(select UTC_DATETIME_ID, ERBS, cell, factor_3 from (select UTC_DATETIME_ID, ERBS, EUtranCellFDD as cell, ISNULL(pmErabEstabSuccInitQci,0)/ISNULL(pmErabEstabAttInitQci,0) as factor_3 from DC_E_ERBS_EUTRANCELLFDD_V_RAW where DCVECTOR_INDEX=1 union all select UTC_DATETIME_ID, ERBS, EUtranCellTDD as cell, ISNULL(pmErabEstabSuccInitQci,0)/ISNULL(pmErabEstabAttInitQci,0) as factor_3 from DC_E_ERBS_EUTRANCELLTDD_V_RAW where DCVECTOR_INDEX=1) as KPI where UTC_DATETIME_ID = '%s') as FACTOR_3 where FACTOR_1.ERBS=FACTOR_2.ERBS and FACTOR_2.ERBS=FACTOR_3.ERBS and  FACTOR_1.cell=FACTOR_2.cell and FACTOR_2.cell=FACTOR_3.cell) as KPI group by UTC_DATETIME_ID, ERBS order by ERBS"%(SQLConfig[1],SQLConfig[1],SQLConfig[1])
        else:
            sourceSQL="select UTC_DATETIME_ID, ERBS, 100 * avg(KPI_VALUE) as KPI_VALUE from (select FACTOR_1.UTC_DATETIME_ID as UTC_DATETIME_ID, FACTOR_1.ERBS as ERBS, FACTOR_1.cell as cell, factor_1 * factor_2 * factor_3 as KPI_VALUE from (select UTC_DATETIME_ID, ERBS, cell, factor_1 from (select UTC_DATETIME_ID, ERBS, EUtranCellFDD as cell, (ISNULL(pmRrcConnEstabSuccMod,0) + ISNULL(pmRrcConnEstabSuccMta,0))/(ISNULL(pmRrcConnEstabAttMod,0) + ISNULL(pmRrcConnEstabAttMta,0) - ISNULL(pmRrcConnEstabAttReattMod,0) - ISNULL(pmRrcConnEstabAttReattMta,0) - ISNULL(pmRrcConnEstabFailMmeOvlMod,0)) as factor_1 from DC_E_ERBS_EUTRANCELLFDD_RAW union all select UTC_DATETIME_ID, ERBS, EUtranCellTDD as cell, (ISNULL(pmRrcConnEstabSuccMod,0) + ISNULL(pmRrcConnEstabSuccMta,0))/(ISNULL(pmRrcConnEstabAttMod,0) + ISNULL(pmRrcConnEstabAttMta,0) - ISNULL(pmRrcConnEstabAttReattMod,0) - ISNULL(pmRrcConnEstabAttReattMta,0) - ISNULL(pmRrcConnEstabFailMmeOvlMod,0)) as factor_1 from DC_E_ERBS_EUTRANCELLTDD_RAW) as KPI where UTC_DATETIME_ID = '%s'and ERBS='%s') as FACTOR_1,(select UTC_DATETIME_ID, ERBS, cell, factor_2 from (select UTC_DATETIME_ID, ERBS, EUtranCellFDD as cell, (ISNULL(pmS1SigConnEstabSuccMod,0) + ISNULL(pmS1SigConnEstabSuccMta,0))/(ISNULL(pmS1SigConnEstabAttMod,0) + ISNULL(pmS1SigConnEstabAttMta,0)) as factor_2 from DC_E_ERBS_EUTRANCELLFDD_RAW union all select UTC_DATETIME_ID, ERBS, EUtranCellTDD as cell, (ISNULL(pmS1SigConnEstabSuccMod,0) + ISNULL(pmS1SigConnEstabSuccMta,0))/(ISNULL(pmS1SigConnEstabAttMod,0) + ISNULL(pmS1SigConnEstabAttMta,0)) as factor_2 from DC_E_ERBS_EUTRANCELLTDD_RAW) as KPI where UTC_DATETIME_ID = '%s' and ERBS='%s') as FACTOR_2,(select UTC_DATETIME_ID, ERBS, cell, factor_3 from (select UTC_DATETIME_ID, ERBS, EUtranCellFDD as cell, ISNULL(pmErabEstabSuccInitQci,0)/ISNULL(pmErabEstabAttInitQci,0) as factor_3 from DC_E_ERBS_EUTRANCELLFDD_V_RAW where DCVECTOR_INDEX=1 union all select UTC_DATETIME_ID, ERBS, EUtranCellTDD as cell, ISNULL(pmErabEstabSuccInitQci,0)/ISNULL(pmErabEstabAttInitQci,0) as factor_3 from DC_E_ERBS_EUTRANCELLTDD_V_RAW where DCVECTOR_INDEX=1) as KPI where UTC_DATETIME_ID = '%s'and ERBS='%s') as FACTOR_3 where FACTOR_1.ERBS=FACTOR_2.ERBS and FACTOR_2.ERBS=FACTOR_3.ERBS and  FACTOR_1.cell=FACTOR_2.cell and FACTOR_2.cell=FACTOR_3.cell) as KPI group by UTC_DATETIME_ID, ERBS order by ERBS"%(SQLConfig[1],SQLConfig[2],SQLConfig[1],SQLConfig[2],SQLConfig[1],SQLConfig[2])
#29b

#30a
    elif SQLConfig[0] =='30':
        if noNode==1:
            sourceSQL="select UTC_DATETIME_ID, ERBS, 100 * avg(KPI_VALUE) as KPI_VALUE from(select UTC_DATETIME_ID, ERBS, EUtranCellFDD, ISNULL(pmErabEstabSuccAddedQci,0)/(ISNULL(pmErabEstabAttAddedQci,0)-ISNULL(pmErabEstabAttAddedHoOngoingQci,0)) as KPI_VALUE from DC_E_ERBS_EUTRANCELLFDD_V_RAW where DCVECTOR_INDEX=1 union all select UTC_DATETIME_ID, ERBS, EUtranCellTDD, ISNULL(pmErabEstabSuccAddedQci,0)/(ISNULL(pmErabEstabAttAddedQci,0)-ISNULL(pmErabEstabAttAddedHoOngoingQci,0)) as KPI_VALUE from DC_E_ERBS_EUTRANCELLTDD_V_RAW where DCVECTOR_INDEX=1) as KPI where UTC_DATETIME_ID = '%s' group by UTC_DATETIME_ID, ERBS order by UTC_DATETIME_ID, ERBS"%(SQLConfig[1])
        else:
            sourceSQL="select UTC_DATETIME_ID, ERBS, 100 * avg(KPI_VALUE) as KPI_VALUE from(select UTC_DATETIME_ID, ERBS, EUtranCellFDD, ISNULL(pmErabEstabSuccAddedQci,0)/(ISNULL(pmErabEstabAttAddedQci,0)-ISNULL(pmErabEstabAttAddedHoOngoingQci,0)) as KPI_VALUE from DC_E_ERBS_EUTRANCELLFDD_V_RAW where DCVECTOR_INDEX=1 union all select UTC_DATETIME_ID, ERBS, EUtranCellTDD, ISNULL(pmErabEstabSuccAddedQci,0)/(ISNULL(pmErabEstabAttAddedQci,0)-ISNULL(pmErabEstabAttAddedHoOngoingQci,0)) as KPI_VALUE from DC_E_ERBS_EUTRANCELLTDD_V_RAW where DCVECTOR_INDEX=1) as KPI where UTC_DATETIME_ID = '%s' and erbs='%s' group by UTC_DATETIME_ID, ERBS order by UTC_DATETIME_ID, ERBS"%(SQLConfig[1],SQLConfig[2])
#30b

#31a
    elif SQLConfig[0] =='31':
        if noNode==1:
            sourceSQL="select ERBS, UTC_DATETIME_ID, avg(KPI_VALUE) as KPI_VALUE from (SELECT ERBS, EUtranCellTDD, UTC_DATETIME_ID, 100 * (ISNULL(pmErabRelAbnormalEnbActQci,0)+ISNULL(pmErabRelAbnormalMmeActQci,0))/(ISNULL(pmErabRelAbnormalEnbQci,0)+ISNULL(pmErabRelNormalEnbQci,0)+ISNULL(pmErabRelMmeQci,0)) as KPI_VALUE FROM DC_E_ERBS_EUTRANCELLTDD_V_RAW WHERE DCVECTOR_INDEX=1 union SELECT ERBS, EUtranCellFDD, UTC_DATETIME_ID, 100 * (pmErabRelAbnormalEnbActQci+pmErabRelAbnormalMmeActQci)/(pmErabRelAbnormalEnbQci+pmErabRelNormalEnbQci+pmErabRelMmeQci) as KPI_VALUE FROM DC_E_ERBS_EUTRANCELLFDD_V_RAW WHERE  DCVECTOR_INDEX=1)as KPI where UTC_DATETIME_ID ='%s' group by UTC_DATETIME_ID, ERBS order by UTC_DATETIME_ID, ERBS" %(SQLConfig[1])
        else:
            sourceSQL="select ERBS, UTC_DATETIME_ID, avg(KPI_VALUE) as KPI_VALUE from (SELECT ERBS, EUtranCellTDD, UTC_DATETIME_ID, 100 * (ISNULL(pmErabRelAbnormalEnbActQci,0)+ISNULL(pmErabRelAbnormalMmeActQci,0))/(ISNULL(pmErabRelAbnormalEnbQci,0)+ISNULL(pmErabRelNormalEnbQci,0)+ISNULL(pmErabRelMmeQci,0)) as KPI_VALUE FROM DC_E_ERBS_EUTRANCELLTDD_V_RAW WHERE DCVECTOR_INDEX=1 union SELECT ERBS, EUtranCellFDD, UTC_DATETIME_ID, 100 * (pmErabRelAbnormalEnbActQci+pmErabRelAbnormalMmeActQci)/(pmErabRelAbnormalEnbQci+pmErabRelNormalEnbQci+pmErabRelMmeQci) as KPI_VALUE FROM DC_E_ERBS_EUTRANCELLFDD_V_RAW WHERE  DCVECTOR_INDEX=1)as KPI where UTC_DATETIME_ID ='%s' and ERBS='%s' group by UTC_DATETIME_ID, ERBS order by UTC_DATETIME_ID, ERBS" %(SQLConfig[1],SQLConfig[2])
#31b

#32a
    elif SQLConfig[0] =='32':
        if noNode==1:
            sourceSQL="select UTC_DATETIME_ID, ERBS, 100 * avg(KPI_VALUE) as KPI_VALUE from (select NUMERATOR.UTC_DATETIME_ID as UTC_DATETIME_ID, numerator.ERBS as ERBS, numerator.EUtranCellFDD, ISNULL(numerator,0)/ISNULL(denominator,0) as KPI_VALUE from (select UTC_DATETIME_ID, ERBS, EUtranCellFDD, sum(ISNULL(pmPdcpInactSecDlVolteDistr,0)) as numerator from DC_E_ERBS_EUTRANCELLFDD_V_RAW where DCVECTOR_INDEX IN (1,2) group by ERBS, EUtranCellFDD, UTC_DATETIME_ID) as NUMERATOR, (select UTC_DATETIME_ID, ERBS, EUtranCellFDD, sum(ISNULL(pmPdcpInactSecDlVolteDistr,0)) as denominator from DC_E_ERBS_EUTRANCELLFDD_V_RAW group by ERBS, EUtranCellFDD, UTC_DATETIME_ID) as DENOMINATOR where NUMERATOR.ERBS=DENOMINATOR.ERBS and NUMERATOR.EUtranCellFDD=DENOMINATOR.EUtranCellFDD and NUMERATOR.UTC_DATETIME_ID=DENOMINATOR.UTC_DATETIME_ID union all select NUMERATOR.UTC_DATETIME_ID as UTC_DATETIME_ID, numerator.ERBS as ERBS, numerator.EUtranCellTDD, ISNULL(numerator,0)/ISNULL(denominator,0) as KPI_VALUE from (select UTC_DATETIME_ID, ERBS, EUtranCellTDD, sum(ISNULL(pmPdcpInactSecDlVolteDistr,0)) as numerator from DC_E_ERBS_EUTRANCELLTDD_V_RAW where DCVECTOR_INDEX IN (1,2) group by ERBS, EUtranCellTDD, UTC_DATETIME_ID) as NUMERATOR, (select UTC_DATETIME_ID, ERBS, EUtranCellTDD, sum(ISNULL(pmPdcpInactSecDlVolteDistr,0)) as denominator from DC_E_ERBS_EUTRANCELLTDD_V_RAW group by ERBS, EUtranCellTDD, UTC_DATETIME_ID) as DENOMINATOR where NUMERATOR.ERBS=DENOMINATOR.ERBS and NUMERATOR.EUtranCellTDD=DENOMINATOR.EUtranCellTDD and NUMERATOR.UTC_DATETIME_ID=DENOMINATOR.UTC_DATETIME_ID) as KPI where UTC_DATETIME_ID = '%s' group by UTC_DATETIME_ID, ERBS order by UTC_DATETIME_ID, ERBS" %(SQLConfig[1])
        else:
            sourceSQL="select UTC_DATETIME_ID, ERBS, 100 * avg(KPI_VALUE) as KPI_VALUE from (select NUMERATOR.UTC_DATETIME_ID as UTC_DATETIME_ID, numerator.ERBS as ERBS, numerator.EUtranCellFDD, ISNULL(numerator,0)/ISNULL(denominator,0) as KPI_VALUE from (select UTC_DATETIME_ID, ERBS, EUtranCellFDD, sum(ISNULL(pmPdcpInactSecDlVolteDistr,0)) as numerator from DC_E_ERBS_EUTRANCELLFDD_V_RAW where DCVECTOR_INDEX IN (1,2) group by ERBS, EUtranCellFDD, UTC_DATETIME_ID) as NUMERATOR, (select UTC_DATETIME_ID, ERBS, EUtranCellFDD, sum(ISNULL(pmPdcpInactSecDlVolteDistr,0)) as denominator from DC_E_ERBS_EUTRANCELLFDD_V_RAW group by ERBS, EUtranCellFDD, UTC_DATETIME_ID) as DENOMINATOR where NUMERATOR.ERBS=DENOMINATOR.ERBS and NUMERATOR.EUtranCellFDD=DENOMINATOR.EUtranCellFDD and NUMERATOR.UTC_DATETIME_ID=DENOMINATOR.UTC_DATETIME_ID union all select NUMERATOR.UTC_DATETIME_ID as UTC_DATETIME_ID, numerator.ERBS as ERBS, numerator.EUtranCellTDD, ISNULL(numerator,0)/ISNULL(denominator,0) as KPI_VALUE from (select UTC_DATETIME_ID, ERBS, EUtranCellTDD, sum(ISNULL(pmPdcpInactSecDlVolteDistr,0)) as numerator from DC_E_ERBS_EUTRANCELLTDD_V_RAW where DCVECTOR_INDEX IN (1,2) group by ERBS, EUtranCellTDD, UTC_DATETIME_ID) as NUMERATOR, (select UTC_DATETIME_ID, ERBS, EUtranCellTDD, sum(ISNULL(pmPdcpInactSecDlVolteDistr,0)) as denominator from DC_E_ERBS_EUTRANCELLTDD_V_RAW group by ERBS, EUtranCellTDD, UTC_DATETIME_ID) as DENOMINATOR where NUMERATOR.ERBS=DENOMINATOR.ERBS and NUMERATOR.EUtranCellTDD=DENOMINATOR.EUtranCellTDD and NUMERATOR.UTC_DATETIME_ID=DENOMINATOR.UTC_DATETIME_ID) as KPI where UTC_DATETIME_ID = '%s' and ERBS='%s' group by UTC_DATETIME_ID, ERBS order by UTC_DATETIME_ID, ERBS" %(SQLConfig[1],SQLConfig[2])
#32b

#33a
    elif SQLConfig[0] =='33':
        if noNode==1:
            sourceSQL="select UTC_DATETIME_ID, ERBS, 100 * avg(KPI_VALUE) as KPI_VALUE from(select NUMERATOR.UTC_DATETIME_ID as UTC_DATETIME_ID, numerator.ERBS as ERBS, numerator.EUtranCellFDD, ISNULL(numerator,0)/ISNULL(denominator,0) as KPI_VALUE from(select UTC_DATETIME_ID, ERBS, EUtranCellFDD, sum(ISNULL(pmPdcpInactSecDlVolteDistr,0)) as numerator from DC_E_ERBS_EUTRANCELLFDD_V_RAW where DCVECTOR_INDEX IN (1,2) group by ERBS, EUtranCellFDD, UTC_DATETIME_ID) as NUMERATOR, (select UTC_DATETIME_ID, ERBS, EUtranCellFDD, sum(ISNULL(pmPdcpInactSecDlVolteDistr,0)) as denominator from DC_E_ERBS_EUTRANCELLFDD_V_RAW group by ERBS, EUtranCellFDD, UTC_DATETIME_ID ) as DENOMINATOR where NUMERATOR.ERBS=DENOMINATOR.ERBS and NUMERATOR.EUtranCellFDD=DENOMINATOR.EUtranCellFDD and NUMERATOR.UTC_DATETIME_ID=DENOMINATOR.UTC_DATETIME_ID union all select NUMERATOR.UTC_DATETIME_ID as UTC_DATETIME_ID, numerator.ERBS as ERBS, numerator.EUtranCellTDD, ISNULL(numerator,0)/ISNULL(denominator,0) as KPI_VALUE from(select UTC_DATETIME_ID, ERBS, EUtranCellTDD, sum(ISNULL(pmPdcpInactSecDlVolteDistr,0)) as numerator from DC_E_ERBS_EUTRANCELLTDD_V_RAW where DCVECTOR_INDEX IN (1,2) group by ERBS, EUtranCellTDD, UTC_DATETIME_ID) as NUMERATOR, (select UTC_DATETIME_ID, ERBS, EUtranCellTDD, sum(ISNULL(pmPdcpInactSecDlVolteDistr,0)) as denominator from DC_E_ERBS_EUTRANCELLTDD_V_RAW group by ERBS, EUtranCellTDD, UTC_DATETIME_ID) as DENOMINATOR where NUMERATOR.ERBS=DENOMINATOR.ERBS and NUMERATOR.EUtranCellTDD=DENOMINATOR.EUtranCellTDD and NUMERATOR.UTC_DATETIME_ID=DENOMINATOR.UTC_DATETIME_ID) as KPI where UTC_DATETIME_ID = '%s' group by UTC_DATETIME_ID, ERBS order by UTC_DATETIME_ID, ERBS" %(SQLConfig[1])
        else:
            sourceSQL="select UTC_DATETIME_ID, ERBS, 100 * avg(KPI_VALUE) as KPI_VALUE from (select NUMERATOR.UTC_DATETIME_ID as UTC_DATETIME_ID, numerator.ERBS as ERBS, numerator.EUtranCellFDD, ISNULL(numerator,0)/ISNULL(denominator,0) as KPI_VALUE from ( select UTC_DATETIME_ID,ERBS, EUtranCellFDD, sum(ISNULL(pmPdcpInactSecDlVolteDistr,0)) as numerator from DC_E_ERBS_EUTRANCELLFDD_V_RAW where DCVECTOR_INDEX IN (1,2) group by ERBS, EUtranCellFDD, UTC_DATETIME_ID) as NUMERATOR, ( select UTC_DATETIME_ID, ERBS, EUtranCellFDD, sum(ISNULL(pmPdcpInactSecUlVolteDistr,0)) as denominator from DC_E_ERBS_EUTRANCELLFDD_V_RAW group by ERBS, EUtranCellFDD, UTC_DATETIME_ID) as DENOMINATOR where NUMERATOR.ERBS=DENOMINATOR.ERBS  and NUMERATOR.EUtranCellFDD=DENOMINATOR.EUtranCellFDD and NUMERATOR.UTC_DATETIME_ID=DENOMINATOR.UTC_DATETIME_ID union all select NUMERATOR.UTC_DATETIME_ID as UTC_DATETIME_ID, numerator.ERBS as ERBS, numerator.EUtranCellTDD, ISNULL(numerator,0)/ISNULL(denominator,0) as KPI_VALUE from( select UTC_DATETIME_ID, ERBS, EUtranCellTDD, sum(ISNULL(pmPdcpInactSecUlVolteDistr,0)) as numerator from DC_E_ERBS_EUTRANCELLTDD_V_RAW where DCVECTOR_INDEX IN (1,2) group by ERBS, EUtranCellTDD, UTC_DATETIME_ID) as NUMERATOR,(select UTC_DATETIME_ID, ERBS, EUtranCellTDD, sum(ISNULL(pmPdcpInactSecUlVolteDistr,0)) as denominator from DC_E_ERBS_EUTRANCELLTDD_V_RAW group by ERBS, EUtranCellTDD, UTC_DATETIME_ID) as DENOMINATOR where NUMERATOR.ERBS=DENOMINATOR.ERBS and NUMERATOR.EUtranCellTDD=DENOMINATOR.EUtranCellTDD and NUMERATOR.UTC_DATETIME_ID=DENOMINATOR.UTC_DATETIME_ID) as KPI where UTC_DATETIME_ID ='%s' and ERBS='%s' group by UTC_DATETIME_ID, ERBS order by UTC_DATETIME_ID, ERBS" %(SQLConfig[1],SQLConfig[2])
#33b

#34a
    elif SQLConfig[0] =='34':
        if noNode==1:
            sourceSQL="select UTC_DATETIME_ID , SGSN, 100* (ISNULL(VS_SM_CreateDedicatedBearerQCISucc_E,0)/ISNULL(VS_SM_CreateDedicatedBearerQCIAtt_E,0)) as KPI_VALUE from DC_E_SGSNMME_SESSION_SM_E_QCI_RAW where UTC_DATETIME_ID='%s' and MOID like '%%QosClassIdentifier=1'"%(SQLConfig[1])
        else:
            sourceSQL="select UTC_DATETIME_ID , SGSN, 100* (ISNULL(VS_SM_CreateDedicatedBearerQCISucc_E,0)/ISNULL(VS_SM_CreateDedicatedBearerQCIAtt_E,0)) as KPI_VALUE from DC_E_SGSNMME_SESSION_SM_E_QCI_RAW where UTC_DATETIME_ID='%s' and SGSN='%s' and MOID like '%%QosClassIdentifier=1'"%(SQLConfig[1],SQLConfig[2])
#34b

#35a
    elif SQLConfig[0] =='35':
        if noNode==1:
            sourceSQL="select SGSN, OSS_ID,100*sum(ISNULL(num,0))/sum(ISNULL(denom,0)) as KPI_VALUE from (select sum ( ISNULL(VS_SM_CreateDedicatedBearerQCIAtt_E,0)) as num, 0  as denom ,SGSN,OSS_ID from DC_E_SGSNMME_SESSION_SM_E_QCI_RAW WHERE MOID  like '%%QosClassIdentifier=1' AND UTC_DATETIME_ID ='%s' GROUP BY SGSN,OSS_ID UNION ALL select 0 as num, sum ( ISNULL(VS_SM_CreateDedicatedBearerQCIAtt_E,0)) as denom ,SGSN,OSS_ID from DC_E_SGSNMME_SESSION_SM_E_QCI_RAW WHERE MOID  like '%%QosClassIdentifier=[1-9]%%' AND UTC_DATETIME_ID ='%s' GROUP BY SGSN,OSS_ID) as xx GROUP BY SGSN,OSS_ID ORDER BY SGSN"%(SQLConfig[1],SQLConfig[1])
        else:
            sourceSQL="select SGSN, OSS_ID,100*sum(ISNULL(num,0))/sum(ISNULL(denom,0)) as KPI_VALUE from (select sum ( ISNULL(VS_SM_CreateDedicatedBearerQCIAtt_E,0)) as num, 0  as denom ,SGSN,OSS_ID from DC_E_SGSNMME_SESSION_SM_E_QCI_RAW WHERE MOID  like '%%QosClassIdentifier=1' AND UTC_DATETIME_ID ='%s' and SGSN='%s' GROUP BY SGSN,OSS_ID UNION ALL select 0 as num, sum ( ISNULL(VS_SM_CreateDedicatedBearerQCIAtt_E,0)) as denom ,SGSN,OSS_ID from DC_E_SGSNMME_SESSION_SM_E_QCI_RAW WHERE MOID  like '%%QosClassIdentifier=[1-9]%%' AND UTC_DATETIME_ID ='%s' and SGSN='%s' GROUP BY SGSN,OSS_ID) as xx GROUP BY SGSN,OSS_ID ORDER BY SGSN"%(SQLConfig[1],SQLConfig[2],SQLConfig[1],SQLConfig[2])
#35b
    return sourceSQL


def SQLFunctionTarget(SQLConfig,noNode):
#1x
    if SQLConfig[0] =='1':
        #depending on the value of NoNode it sets a varible equal to a SQL command with string formatters replacing the configurable option found in the command
        if noNode ==1:
            targetSQL="SELECT DATETIME_ID,UTC_DATETIME_ID, DC_E_VOLTE_KPI_RAW.NODE_ID,DIM_E_VOLTE_NODE.NODE_NAME,DC_E_VOLTE_KPI_RAW.KPI_VALUE FROM DC_E_VOLTE_KPI_RAW INNER join DIM_E_VOLTE_NODE on DC_E_VOLTE_KPI_RAW.NODE_ID=DIM_E_VOLTE_NODE.NODE_ID WHERE KPI_ID=01 AND UTC_DATETIME_ID ='%s' order by node_name" %(SQLConfig[1])
        else:
            targetSQL="SELECT DATETIME_ID,UTC_DATETIME_ID, DC_E_VOLTE_KPI_RAW.NODE_ID,DIM_E_VOLTE_NODE.NODE_NAME,DC_E_VOLTE_KPI_RAW.KPI_VALUE FROM DC_E_VOLTE_KPI_RAW INNER join DIM_E_VOLTE_NODE on DC_E_VOLTE_KPI_RAW.NODE_ID=DIM_E_VOLTE_NODE.NODE_ID WHERE KPI_ID=01 AND UTC_DATETIME_ID ='%s' and node_name ='%s' order by node_name"%(SQLConfig[1],SQLConfig[2])
#1y

#2x   
    elif SQLConfig[0] =='2':
        if noNode ==1:
            targetSQL="SELECT DATETIME_ID,UTC_DATETIME_ID, DC_E_VOLTE_KPI_RAW.NODE_ID,DIM_E_VOLTE_NODE.NODE_NAME,DC_E_VOLTE_KPI_RAW.KPI_VALUE FROM DC_E_VOLTE_KPI_RAW INNER join DIM_E_VOLTE_NODE on DC_E_VOLTE_KPI_RAW.NODE_ID=DIM_E_VOLTE_NODE.NODE_ID WHERE KPI_ID=02 AND UTC_DATETIME_ID ='%s' order by node_name"%(SQLConfig[1])
        else:
            targetSQL="SELECT DATETIME_ID,UTC_DATETIME_ID, DC_E_VOLTE_KPI_RAW.NODE_ID,DIM_E_VOLTE_NODE.NODE_NAME,DC_E_VOLTE_KPI_RAW.KPI_VALUE FROM DC_E_VOLTE_KPI_RAW INNER join DIM_E_VOLTE_NODE on DC_E_VOLTE_KPI_RAW.NODE_ID=DIM_E_VOLTE_NODE.NODE_ID WHERE KPI_ID=02 AND UTC_DATETIME_ID ='%s' and node_name ='%s' order by node_name"%(SQLConfig[1],SQLConfig[2])
#2y

#3x
    elif SQLConfig[0] =='3':
        if noNode ==1:
            targetSQL="SELECT DATETIME_ID,UTC_DATETIME_ID, DC_E_VOLTE_KPI_RAW.NODE_ID,DIM_E_VOLTE_NODE.NODE_NAME,DC_E_VOLTE_KPI_RAW.KPI_VALUE FROM DC_E_VOLTE_KPI_RAW INNER join DIM_E_VOLTE_NODE on DC_E_VOLTE_KPI_RAW.NODE_ID=DIM_E_VOLTE_NODE.NODE_ID WHERE KPI_ID=03 AND UTC_DATETIME_ID ='%s' order by node_name"%(SQLConfig[1])
        else:
            targetSQL="SELECT DATETIME_ID,UTC_DATETIME_ID, DC_E_VOLTE_KPI_RAW.NODE_ID,DIM_E_VOLTE_NODE.NODE_NAME,DC_E_VOLTE_KPI_RAW.KPI_VALUE FROM DC_E_VOLTE_KPI_RAW INNER join DIM_E_VOLTE_NODE on DC_E_VOLTE_KPI_RAW.NODE_ID=DIM_E_VOLTE_NODE.NODE_ID WHERE KPI_ID=03 AND UTC_DATETIME_ID ='%s' and node_name ='%s' order by node_name"%(SQLConfig[1],SQLConfig[2])
#3y

#4x            
    elif SQLConfig[0] =='4':
        if noNode ==1:
            targetSQL="SELECT DATETIME_ID,UTC_DATETIME_ID, DC_E_VOLTE_KPI_RAW.NODE_ID,DIM_E_VOLTE_NODE.NODE_NAME,DC_E_VOLTE_KPI_RAW.KPI_VALUE FROM DC_E_VOLTE_KPI_RAW INNER join DIM_E_VOLTE_NODE on DC_E_VOLTE_KPI_RAW.NODE_ID=DIM_E_VOLTE_NODE.NODE_ID WHERE KPI_ID=04 AND UTC_DATETIME_ID ='%s' order by node_name"%(SQLConfig[1])
        else:
            targetSQL="SELECT DATETIME_ID,UTC_DATETIME_ID, DC_E_VOLTE_KPI_RAW.NODE_ID,DIM_E_VOLTE_NODE.NODE_NAME,DC_E_VOLTE_KPI_RAW.KPI_VALUE FROM DC_E_VOLTE_KPI_RAW INNER join DIM_E_VOLTE_NODE on DC_E_VOLTE_KPI_RAW.NODE_ID=DIM_E_VOLTE_NODE.NODE_ID WHERE KPI_ID=04 AND UTC_DATETIME_ID ='%s' and node_name ='%s' order by node_name"%(SQLConfig[1],SQLConfig[2])
#4y

#5x
    elif SQLConfig[0] =='5':
        if noNode ==1:
            targetSQL="SELECT DATETIME_ID,UTC_DATETIME_ID, DC_E_VOLTE_KPI_RAW.NODE_ID,DIM_E_VOLTE_NODE.NODE_NAME,DC_E_VOLTE_KPI_RAW.KPI_VALUE FROM DC_E_VOLTE_KPI_RAW INNER join DIM_E_VOLTE_NODE on DC_E_VOLTE_KPI_RAW.NODE_ID=DIM_E_VOLTE_NODE.NODE_ID WHERE KPI_ID=05 AND UTC_DATETIME_ID ='%s' order by node_name"%(SQLConfig[1])
        else:
            targetSQL="SELECT DATETIME_ID,UTC_DATETIME_ID, DC_E_VOLTE_KPI_RAW.NODE_ID,DIM_E_VOLTE_NODE.NODE_NAME,DC_E_VOLTE_KPI_RAW.KPI_VALUE FROM DC_E_VOLTE_KPI_RAW INNER join DIM_E_VOLTE_NODE on DC_E_VOLTE_KPI_RAW.NODE_ID=DIM_E_VOLTE_NODE.NODE_ID WHERE KPI_ID=05 AND UTC_DATETIME_ID ='%s' and node_name ='%s' order by node_name"%(SQLConfig[1],SQLConfig[2])
#5y

#6x 
    elif SQLConfig[0] =='6':
        if noNode ==1:
            targetSQL="SELECT DATETIME_ID,UTC_DATETIME_ID, DC_E_VOLTE_KPI_RAW.NODE_ID,DIM_E_VOLTE_NODE.NODE_NAME,DC_E_VOLTE_KPI_RAW.KPI_VALUE FROM DC_E_VOLTE_KPI_RAW INNER join DIM_E_VOLTE_NODE on DC_E_VOLTE_KPI_RAW.NODE_ID=DIM_E_VOLTE_NODE.NODE_ID WHERE KPI_ID=06 AND UTC_DATETIME_ID ='%s' order by node_name"%(SQLConfig[1])
        else:
            targetSQL="SELECT DATETIME_ID,UTC_DATETIME_ID, DC_E_VOLTE_KPI_RAW.NODE_ID,DIM_E_VOLTE_NODE.NODE_NAME,DC_E_VOLTE_KPI_RAW.KPI_VALUE FROM DC_E_VOLTE_KPI_RAW INNER join DIM_E_VOLTE_NODE on DC_E_VOLTE_KPI_RAW.NODE_ID=DIM_E_VOLTE_NODE.NODE_ID WHERE KPI_ID=06 AND UTC_DATETIME_ID ='%s' and node_name ='%s' order by node_name"%(SQLConfig[1],SQLConfig[2])
#6y

#7x    
    elif SQLConfig[0] =='7':
        if noNode ==1:
            targetSQL="SELECT DATETIME_ID,UTC_DATETIME_ID, DC_E_VOLTE_KPI_RAW.NODE_ID,DIM_E_VOLTE_NODE.NODE_NAME,DC_E_VOLTE_KPI_RAW.KPI_VALUE FROM DC_E_VOLTE_KPI_RAW INNER join DIM_E_VOLTE_NODE on DC_E_VOLTE_KPI_RAW.NODE_ID=DIM_E_VOLTE_NODE.NODE_ID WHERE KPI_ID=07 AND DATETIME_ID ='%s' order by node_name"%(SQLConfig[1])
        else:
            targetSQL="SELECT DATETIME_ID,UTC_DATETIME_ID, DC_E_VOLTE_KPI_RAW.NODE_ID,DIM_E_VOLTE_NODE.NODE_NAME,DC_E_VOLTE_KPI_RAW.KPI_VALUE FROM DC_E_VOLTE_KPI_RAW INNER join DIM_E_VOLTE_NODE on DC_E_VOLTE_KPI_RAW.NODE_ID=DIM_E_VOLTE_NODE.NODE_ID WHERE KPI_ID=07 AND DATETIME_ID ='%s' and node_name ='%s' order by node_name" %(SQLConfig[1],SQLConfig[2])
#7y

#8x
    elif SQLConfig[0] =='8':
        if noNode ==1:
            targetSQL="SELECT DATETIME_ID,UTC_DATETIME_ID, DC_E_VOLTE_KPI_RAW.NODE_ID,DIM_E_VOLTE_NODE.NODE_NAME,DC_E_VOLTE_KPI_RAW.KPI_VALUE FROM DC_E_VOLTE_KPI_RAW INNER join DIM_E_VOLTE_NODE on DC_E_VOLTE_KPI_RAW.NODE_ID=DIM_E_VOLTE_NODE.NODE_ID WHERE KPI_ID=08 AND UTC_DATETIME_ID ='%s'"%(SQLConfig[1])
        else:
            targetSQL="SELECT DATETIME_ID,UTC_DATETIME_ID, DC_E_VOLTE_KPI_RAW.NODE_ID,DIM_E_VOLTE_NODE.NODE_NAME,DC_E_VOLTE_KPI_RAW.KPI_VALUE FROM DC_E_VOLTE_KPI_RAW INNER join DIM_E_VOLTE_NODE on DC_E_VOLTE_KPI_RAW.NODE_ID=DIM_E_VOLTE_NODE.NODE_ID WHERE KPI_ID=08 AND UTC_DATETIME_ID ='%s' and node_name ='%s'"%(SQLConfig[1],SQLConfig[2])
#8y
    
#9x    
    elif SQLConfig[0] =='9':
        if noNode ==1:
            targetSQL="SELECT DATETIME_ID,UTC_DATETIME_ID, DC_E_VOLTE_KPI_RAW.NODE_ID,DIM_E_VOLTE_NODE.NODE_NAME,DC_E_VOLTE_KPI_RAW.KPI_VALUE FROM DC_E_VOLTE_KPI_RAW INNER join DIM_E_VOLTE_NODE on DC_E_VOLTE_KPI_RAW.NODE_ID=DIM_E_VOLTE_NODE.NODE_ID WHERE KPI_ID=09 AND UTC_DATETIME_ID ='%s' order by node_name"%(SQLConfig[1])
        else:
            targetSQL="SELECT DATETIME_ID,UTC_DATETIME_ID, DC_E_VOLTE_KPI_RAW.NODE_ID,DIM_E_VOLTE_NODE.NODE_NAME,DC_E_VOLTE_KPI_RAW.KPI_VALUE FROM DC_E_VOLTE_KPI_RAW INNER join DIM_E_VOLTE_NODE on DC_E_VOLTE_KPI_RAW.NODE_ID=DIM_E_VOLTE_NODE.NODE_ID WHERE KPI_ID=09 AND UTC_DATETIME_ID ='%s' and Node_name='%s' order by node_name"%(SQLConfig[1],SQLConfig[2])
#9y
    
#10x
    elif SQLConfig[0] =='10':
        if noNode ==1:
            targetSQL="SELECT DATETIME_ID,UTC_DATETIME_ID, DC_E_VOLTE_KPI_RAW.NODE_ID,DIM_E_VOLTE_NODE.NODE_NAME,DC_E_VOLTE_KPI_RAW.KPI_VALUE FROM DC_E_VOLTE_KPI_RAW INNER join DIM_E_VOLTE_NODE on DC_E_VOLTE_KPI_RAW.NODE_ID=DIM_E_VOLTE_NODE.NODE_ID WHERE KPI_ID=10 AND UTC_DATETIME_ID ='%s' order by node_name"%(SQLConfig[1])
        else:
            targetSQL="SELECT DATETIME_ID,UTC_DATETIME_ID, DC_E_VOLTE_KPI_RAW.NODE_ID,DIM_E_VOLTE_NODE.NODE_NAME,DC_E_VOLTE_KPI_RAW.KPI_VALUE FROM DC_E_VOLTE_KPI_RAW INNER join DIM_E_VOLTE_NODE on DC_E_VOLTE_KPI_RAW.NODE_ID=DIM_E_VOLTE_NODE.NODE_ID WHERE KPI_ID=10 AND UTC_DATETIME_ID ='%s' and node_name ='%s' order by node_name"%(SQLConfig[1],SQLConfig[2])
#10y

#11x
    elif SQLConfig[0] =='11':
        if noNode ==1:
            targetSQL="SELECT DATETIME_ID,UTC_DATETIME_ID, DC_E_VOLTE_KPI_RAW.NODE_ID,DIM_E_VOLTE_NODE.NODE_NAME,DC_E_VOLTE_KPI_RAW.KPI_VALUE FROM DC_E_VOLTE_KPI_RAW INNER join DIM_E_VOLTE_NODE on DC_E_VOLTE_KPI_RAW.NODE_ID=DIM_E_VOLTE_NODE.NODE_ID WHERE KPI_ID=11 AND UTC_DATETIME_ID ='%s' order by node_name"%(SQLConfig[1])
        else:
            targetSQL="SELECT DATETIME_ID,UTC_DATETIME_ID, DC_E_VOLTE_KPI_RAW.NODE_ID,DIM_E_VOLTE_NODE.NODE_NAME,DC_E_VOLTE_KPI_RAW.KPI_VALUE FROM DC_E_VOLTE_KPI_RAW INNER join DIM_E_VOLTE_NODE on DC_E_VOLTE_KPI_RAW.NODE_ID=DIM_E_VOLTE_NODE.NODE_ID WHERE KPI_ID=11 AND UTC_DATETIME_ID ='%s' and node_name ='%s' order by node_name"%(SQLConfig[1],SQLConfig[2])
#11y

#12x
    elif SQLConfig[0] =='12':
        if noNode ==1:
            targetSQL="SELECT DATETIME_ID,UTC_DATETIME_ID, DC_E_VOLTE_KPI_RAW.NODE_ID,DIM_E_VOLTE_NODE.NODE_NAME,DC_E_VOLTE_KPI_RAW.KPI_VALUE FROM DC_E_VOLTE_KPI_RAW INNER join DIM_E_VOLTE_NODE on DC_E_VOLTE_KPI_RAW.NODE_ID=DIM_E_VOLTE_NODE.NODE_ID WHERE KPI_ID=12 AND UTC_DATETIME_ID ='%s' order by node_name"%(SQLConfig[1])
        else:
            targetSQL="SELECT DATETIME_ID,UTC_DATETIME_ID, DC_E_VOLTE_KPI_RAW.NODE_ID,DIM_E_VOLTE_NODE.NODE_NAME,DC_E_VOLTE_KPI_RAW.KPI_VALUE FROM DC_E_VOLTE_KPI_RAW INNER join DIM_E_VOLTE_NODE on DC_E_VOLTE_KPI_RAW.NODE_ID=DIM_E_VOLTE_NODE.NODE_ID WHERE KPI_ID=12 AND UTC_DATETIME_ID ='%s' and node_name ='%s' order by node_name"%(SQLConfig[1],SQLConfig[2])
#12y

#13x
    elif SQLConfig[0] =='13':
        if noNode ==1:
            targetSQL="SELECT KPI_ID,DC_E_VOLTE_KPI_RAW.NODE_ID,DIM_E_VOLTE_NODE.NODE_NAME,DC_E_VOLTE_KPI_RAW.KPI_VALUE,UTC_DATETIME_ID,DATETIME_ID,DC_E_VOLTE_KPI_RAW.oss_id FROM DC_E_VOLTE_KPI_RAW INNER join DIM_E_VOLTE_NODE on DC_E_VOLTE_KPI_RAW.NODE_ID=DIM_E_VOLTE_NODE.NODE_ID WHERE KPI_ID=13 AND utc_DATETIME_ID ='%s' order by KPI_ID"%(SQLConfig[1])
        else:
            targetSQL="SELECT KPI_ID,DC_E_VOLTE_KPI_RAW.NODE_ID,DIM_E_VOLTE_NODE.NODE_NAME,DC_E_VOLTE_KPI_RAW.KPI_VALUE,UTC_DATETIME_ID,DATETIME_ID,DC_E_VOLTE_KPI_RAW.oss_id FROM DC_E_VOLTE_KPI_RAW INNER join DIM_E_VOLTE_NODE on DC_E_VOLTE_KPI_RAW.NODE_ID=DIM_E_VOLTE_NODE.NODE_ID WHERE KPI_ID=13 AND utc_DATETIME_ID ='%s' and node_name ='%s' order by KPI_ID"%(SQLConfig[1],SQLConfig[2])
#13y

#14x 
    elif SQLConfig[0] =='14':
        if noNode ==1:
            targetSQL="SELECT DATETIME_ID,UTC_DATETIME_ID, DC_E_VOLTE_KPI_RAW.NODE_ID,DIM_E_VOLTE_NODE.NODE_NAME,DC_E_VOLTE_KPI_RAW.KPI_VALUE FROM DC_E_VOLTE_KPI_RAW INNER join DIM_E_VOLTE_NODE on DC_E_VOLTE_KPI_RAW.NODE_ID=DIM_E_VOLTE_NODE.NODE_ID WHERE KPI_ID=14 AND UTC_DATETIME_ID ='%s' order by node_name" %(SQLConfig[1])
        else:
            targetSQL="SELECT DATETIME_ID,UTC_DATETIME_ID, DC_E_VOLTE_KPI_RAW.NODE_ID,DIM_E_VOLTE_NODE.NODE_NAME,DC_E_VOLTE_KPI_RAW.KPI_VALUE FROM DC_E_VOLTE_KPI_RAW INNER join DIM_E_VOLTE_NODE on DC_E_VOLTE_KPI_RAW.NODE_ID=DIM_E_VOLTE_NODE.NODE_ID WHERE KPI_ID=14 AND UTC_DATETIME_ID ='%s' and node_name ='%s' order by node_name"%(SQLConfig[1],SQLConfig[2])
#14y

#15x
    elif SQLConfig[0] =='15':
        if noNode ==1:
            targetSQL="SELECT DATETIME_ID,UTC_DATETIME_ID, DC_E_VOLTE_KPI_RAW.NODE_ID,DIM_E_VOLTE_NODE.NODE_NAME,DC_E_VOLTE_KPI_RAW.KPI_VALUE FROM DC_E_VOLTE_KPI_RAW INNER join DIM_E_VOLTE_NODE on DC_E_VOLTE_KPI_RAW.NODE_ID=DIM_E_VOLTE_NODE.NODE_ID WHERE KPI_ID=15 AND UTC_DATETIME_ID ='%s' order by node_name"%(SQLConfig[1])
        else:
            targetSQL="SELECT DATETIME_ID,UTC_DATETIME_ID, DC_E_VOLTE_KPI_RAW.NODE_ID,DIM_E_VOLTE_NODE.NODE_NAME,DC_E_VOLTE_KPI_RAW.KPI_VALUE FROM DC_E_VOLTE_KPI_RAW INNER join DIM_E_VOLTE_NODE on DC_E_VOLTE_KPI_RAW.NODE_ID=DIM_E_VOLTE_NODE.NODE_ID WHERE KPI_ID=15 AND UTC_DATETIME_ID ='%s' and node_name ='%s' order by node_name"%(SQLConfig[1],SQLConfig[2])
#15y

#16x
    elif SQLConfig[0] =='16':
        if noNode ==1:
            targetSQL="SELECT DC_E_VOLTE_KPI_RAW.NODE_ID,DIM_E_VOLTE_NODE.NODE_NAME,DC_E_VOLTE_KPI_RAW.KPI_VALUE,DATETIME_ID,UTC_DATETIME_ID FROM DC_E_VOLTE_KPI_RAW INNER join DIM_E_VOLTE_NODE on DC_E_VOLTE_KPI_RAW.NODE_ID=DIM_E_VOLTE_NODE.NODE_ID WHERE KPI_ID=15 AND UTC_DATETIME_ID ='%s' order by node_name"%(SQLConfig[1])
        else:
            targetSQL="SELECT DC_E_VOLTE_KPI_RAW.NODE_ID,DIM_E_VOLTE_NODE.NODE_NAME,DC_E_VOLTE_KPI_RAW.KPI_VALUE,DATETIME_ID,UTC_DATETIME_ID FROM DC_E_VOLTE_KPI_RAW INNER join DIM_E_VOLTE_NODE on DC_E_VOLTE_KPI_RAW.NODE_ID=DIM_E_VOLTE_NODE.NODE_ID WHERE KPI_ID=15 AND UTC_DATETIME_ID ='%s' and node_name ='%s' order by node_name"%(SQLConfig[1],SQLConfig[2])
#16y

#17x
    elif SQLConfig[0] =='17':
        if noNode ==1:
            targetSQL="SELECT DATETIME_ID,UTC_DATETIME_ID, DC_E_VOLTE_KPI_RAW.NODE_ID,DIM_E_VOLTE_NODE.NODE_NAME,DC_E_VOLTE_KPI_RAW.KPI_VALUE FROM DC_E_VOLTE_KPI_RAW INNER join DIM_E_VOLTE_NODE on DC_E_VOLTE_KPI_RAW.NODE_ID=DIM_E_VOLTE_NODE.NODE_ID WHERE KPI_ID=17 AND UTC_DATETIME_ID ='%s' order by node_name"%(SQLConfig[1])
        else:
            targetSQL="SELECT DATETIME_ID,UTC_DATETIME_ID, DC_E_VOLTE_KPI_RAW.NODE_ID,DIM_E_VOLTE_NODE.NODE_NAME,DC_E_VOLTE_KPI_RAW.KPI_VALUE FROM DC_E_VOLTE_KPI_RAW INNER join DIM_E_VOLTE_NODE on DC_E_VOLTE_KPI_RAW.NODE_ID=DIM_E_VOLTE_NODE.NODE_ID WHERE KPI_ID=17 AND UTC_DATETIME_ID ='%s' and node_name ='%s' order by node_name"%(SQLConfig[1],SQLConfig[2])
#17y
    
#18x
    elif SQLConfig[0] =='18':
        if noNode ==1:
            targetSQL="SELECT DATETIME_ID,UTC_DATETIME_ID, DC_E_VOLTE_KPI_RAW.NODE_ID,DIM_E_VOLTE_NODE.NODE_NAME,DC_E_VOLTE_KPI_RAW.KPI_VALUE FROM DC_E_VOLTE_KPI_RAW INNER join DIM_E_VOLTE_NODE on DC_E_VOLTE_KPI_RAW.NODE_ID=DIM_E_VOLTE_NODE.NODE_ID WHERE KPI_ID=18 AND UTC_DATETIME_ID ='%s' order by node_name"%(SQLConfig[1])
        else:
            targetSQL="SELECT DATETIME_ID,UTC_DATETIME_ID, DC_E_VOLTE_KPI_RAW.NODE_ID,DIM_E_VOLTE_NODE.NODE_NAME,DC_E_VOLTE_KPI_RAW.KPI_VALUE FROM DC_E_VOLTE_KPI_RAW INNER join DIM_E_VOLTE_NODE on DC_E_VOLTE_KPI_RAW.NODE_ID=DIM_E_VOLTE_NODE.NODE_ID WHERE KPI_ID=18 AND UTC_DATETIME_ID ='%s' and node_name ='%s' order by node_name"%(SQLConfig[1],SQLConfig[2])
#18y

#19x
    elif SQLConfig[0] =='19':
        if noNode ==1:
            targetSQL="SELECT DATETIME_ID,UTC_DATETIME_ID, DC_E_VOLTE_KPI_RAW.NODE_ID,DIM_E_VOLTE_NODE.NODE_NAME,DC_E_VOLTE_KPI_RAW.KPI_VALUE FROM DC_E_VOLTE_KPI_RAW INNER join DIM_E_VOLTE_NODE on DC_E_VOLTE_KPI_RAW.NODE_ID=DIM_E_VOLTE_NODE.NODE_ID WHERE KPI_ID=19 AND UTC_DATETIME_ID ='%s' order by node_name"%(SQLConfig[1])
        else:
            targetSQL="SELECT DATETIME_ID,UTC_DATETIME_ID, DC_E_VOLTE_KPI_RAW.NODE_ID,DIM_E_VOLTE_NODE.NODE_NAME,DC_E_VOLTE_KPI_RAW.KPI_VALUE FROM DC_E_VOLTE_KPI_RAW INNER join DIM_E_VOLTE_NODE on DC_E_VOLTE_KPI_RAW.NODE_ID=DIM_E_VOLTE_NODE.NODE_ID WHERE KPI_ID=19 AND UTC_DATETIME_ID ='%s' and node_name ='%s' order by node_name"%(SQLConfig[1],SQLConfig[2])
#19y
    
#20x
    elif SQLConfig[0] =='20':
        if noNode ==1:
            targetSQL="SELECT DATETIME_ID,UTC_DATETIME_ID, DC_E_VOLTE_KPI_RAW.NODE_ID,DIM_E_VOLTE_NODE.NODE_NAME,DC_E_VOLTE_KPI_RAW.KPI_VALUE FROM DC_E_VOLTE_KPI_RAW INNER join DIM_E_VOLTE_NODE on DC_E_VOLTE_KPI_RAW.NODE_ID=DIM_E_VOLTE_NODE.NODE_ID WHERE KPI_ID=20 AND UTC_DATETIME_ID ='%s' order by node_name"%(SQLConfig[1])
        else:
            targetSQL="SELECT DATETIME_ID,UTC_DATETIME_ID, DC_E_VOLTE_KPI_RAW.NODE_ID,DIM_E_VOLTE_NODE.NODE_NAME,DC_E_VOLTE_KPI_RAW.KPI_VALUE FROM DC_E_VOLTE_KPI_RAW INNER join DIM_E_VOLTE_NODE on DC_E_VOLTE_KPI_RAW.NODE_ID=DIM_E_VOLTE_NODE.NODE_ID WHERE KPI_ID=20 AND UTC_DATETIME_ID ='%s' and node_name ='%s' order by node_name"%(SQLConfig[1],SQLConfig[2])
#20y

#21x
    elif SQLConfig[0] =='21':
        if noNode ==1:
            targetSQL="SELECT DATETIME_ID,UTC_DATETIME_ID, DC_E_VOLTE_KPI_RAW.NODE_ID,DIM_E_VOLTE_NODE.NODE_NAME,DC_E_VOLTE_KPI_RAW.KPI_VALUE FROM DC_E_VOLTE_KPI_RAW INNER join DIM_E_VOLTE_NODE on DC_E_VOLTE_KPI_RAW.NODE_ID=DIM_E_VOLTE_NODE.NODE_ID WHERE KPI_ID=21 AND UTC_DATETIME_ID ='%s' order by node_name"%(SQLConfig[1])
        else:
            targetSQL="SELECT DATETIME_ID,UTC_DATETIME_ID, DC_E_VOLTE_KPI_RAW.NODE_ID,DIM_E_VOLTE_NODE.NODE_NAME,DC_E_VOLTE_KPI_RAW.KPI_VALUE FROM DC_E_VOLTE_KPI_RAW INNER join DIM_E_VOLTE_NODE on DC_E_VOLTE_KPI_RAW.NODE_ID=DIM_E_VOLTE_NODE.NODE_ID WHERE KPI_ID=21 AND UTC_DATETIME_ID ='%s' and node_name ='%s' order by node_name"%(SQLConfig[1],SQLConfig[2])
#21y
    
#22x
    elif SQLConfig[0] =='22':
        if noNode ==1:
            targetSQL="SELECT DATETIME_ID,UTC_DATETIME_ID, DC_E_VOLTE_KPI_RAW.NODE_ID,DIM_E_VOLTE_NODE.NODE_NAME,DC_E_VOLTE_KPI_RAW.KPI_VALUE FROM DC_E_VOLTE_KPI_RAW INNER join DIM_E_VOLTE_NODE on DC_E_VOLTE_KPI_RAW.NODE_ID=DIM_E_VOLTE_NODE.NODE_ID WHERE KPI_ID=22 AND UTC_DATETIME_ID ='%s' order by node_name"%(SQLConfig[1])
        else:
            targetSQL="SELECT DATETIME_ID,UTC_DATETIME_ID, DC_E_VOLTE_KPI_RAW.NODE_ID,DIM_E_VOLTE_NODE.NODE_NAME,DC_E_VOLTE_KPI_RAW.KPI_VALUE FROM DC_E_VOLTE_KPI_RAW INNER join DIM_E_VOLTE_NODE on DC_E_VOLTE_KPI_RAW.NODE_ID=DIM_E_VOLTE_NODE.NODE_ID WHERE KPI_ID=22 AND UTC_DATETIME_ID ='%s' and node_name ='%s' order by node_name"%(SQLConfig[1],SQLConfig[2])
#22y

#23x
    elif SQLConfig[0] =='23':
        if noNode ==1:
            targetSQL="SELECT DATETIME_ID,UTC_DATETIME_ID, DC_E_VOLTE_KPI_RAW.NODE_ID,DIM_E_VOLTE_NODE.NODE_NAME,DC_E_VOLTE_KPI_RAW.KPI_VALUE FROM DC_E_VOLTE_KPI_RAW INNER join DIM_E_VOLTE_NODE on DC_E_VOLTE_KPI_RAW.NODE_ID=DIM_E_VOLTE_NODE.NODE_ID WHERE KPI_ID=23 AND UTC_DATETIME_ID ='%s' order by node_name"%(SQLConfig[1])
        else:
            targetSQL="SELECT DATETIME_ID,UTC_DATETIME_ID, DC_E_VOLTE_KPI_RAW.NODE_ID,DIM_E_VOLTE_NODE.NODE_NAME,DC_E_VOLTE_KPI_RAW.KPI_VALUE FROM DC_E_VOLTE_KPI_RAW INNER join DIM_E_VOLTE_NODE on DC_E_VOLTE_KPI_RAW.NODE_ID=DIM_E_VOLTE_NODE.NODE_ID WHERE KPI_ID=23 AND UTC_DATETIME_ID ='%s' and node_name ='%s' order by node_name"%(SQLConfig[1],SQLConfig[2])
#23y

#24x
    elif SQLConfig[0] =='24':
        if noNode ==1:
            targetSQL="SELECT DC_E_VOLTE_KPI_RAW.NODE_ID,DIM_E_VOLTE_NODE.NODE_NAME,DC_E_VOLTE_KPI_RAW.KPI_VALUE,DATETIME_ID,UTC_DATETIME_ID FROM DC_E_VOLTE_KPI_RAW INNER join DIM_E_VOLTE_NODE on DC_E_VOLTE_KPI_RAW.NODE_ID=DIM_E_VOLTE_NODE.NODE_ID WHERE KPI_ID=24 AND datetime_id ='%s' order by node_name" %(SQLConfig[1])
        else:
            targetSQL="SELECT DC_E_VOLTE_KPI_RAW.NODE_ID,DIM_E_VOLTE_NODE.NODE_NAME,DC_E_VOLTE_KPI_RAW.KPI_VALUE,DATETIME_ID,UTC_DATETIME_ID FROM DC_E_VOLTE_KPI_RAW INNER join DIM_E_VOLTE_NODE on DC_E_VOLTE_KPI_RAW.NODE_ID=DIM_E_VOLTE_NODE.NODE_ID WHERE KPI_ID=24 AND datetime_id ='%s' and node_name='%s' order by node_name"%(SQLConfig[1],SQLConfig[2])
#24y

#25x
    elif SQLConfig[0] =='25':
        if noNode ==1:
            targetSQL="SELECT DATETIME_ID,UTC_DATETIME_ID, DC_E_VOLTE_KPI_RAW.NODE_ID,DIM_E_VOLTE_NODE.NODE_NAME,DC_E_VOLTE_KPI_RAW.KPI_VALUE FROM DC_E_VOLTE_KPI_RAW INNER join DIM_E_VOLTE_NODE on DC_E_VOLTE_KPI_RAW.NODE_ID=DIM_E_VOLTE_NODE.NODE_ID WHERE KPI_ID=25 AND UTC_DATETIME_ID ='%s' order by node_name"%(SQLConfig[1])
        else:
            targetSQL="SELECT DATETIME_ID,UTC_DATETIME_ID, DC_E_VOLTE_KPI_RAW.NODE_ID,DIM_E_VOLTE_NODE.NODE_NAME,DC_E_VOLTE_KPI_RAW.KPI_VALUE FROM DC_E_VOLTE_KPI_RAW INNER join DIM_E_VOLTE_NODE on DC_E_VOLTE_KPI_RAW.NODE_ID=DIM_E_VOLTE_NODE.NODE_ID WHERE KPI_ID=25 AND UTC_DATETIME_ID ='%s' and node_name ='%s' order by node_name"%(SQLConfig[1],SQLConfig[2])
#25y

#26x
    elif SQLConfig[0] =='26':
        if noNode ==1:
            targetSQL="SELECT DATETIME_ID,UTC_DATETIME_ID, DC_E_VOLTE_KPI_RAW.NODE_ID,DIM_E_VOLTE_NODE.NODE_NAME,DC_E_VOLTE_KPI_RAW.KPI_VALUE FROM DC_E_VOLTE_KPI_RAW INNER join DIM_E_VOLTE_NODE on DC_E_VOLTE_KPI_RAW.NODE_ID=DIM_E_VOLTE_NODE.NODE_ID WHERE KPI_ID=26 AND UTC_DATETIME_ID ='%s' order by node_name"%(SQLConfig[1])
        else:
            targetSQL="SELECT DATETIME_ID,UTC_DATETIME_ID, DC_E_VOLTE_KPI_RAW.NODE_ID,DIM_E_VOLTE_NODE.NODE_NAME,DC_E_VOLTE_KPI_RAW.KPI_VALUE FROM DC_E_VOLTE_KPI_RAW INNER join DIM_E_VOLTE_NODE on DC_E_VOLTE_KPI_RAW.NODE_ID=DIM_E_VOLTE_NODE.NODE_ID WHERE KPI_ID=26 AND UTC_DATETIME_ID ='%s' and node_name ='%s' order by node_name"%(SQLConfig[1],SQLConfig[2])
#26y

#27x
    elif SQLConfig[0] =='27':
        if noNode ==1:
            targetSQL="SELECT DATETIME_ID,UTC_DATETIME_ID, DC_E_VOLTE_KPI_RAW.NODE_ID,DIM_E_VOLTE_NODE.NODE_NAME,DC_E_VOLTE_KPI_RAW.KPI_VALUE FROM DC_E_VOLTE_KPI_RAW INNER join DIM_E_VOLTE_NODE on DC_E_VOLTE_KPI_RAW.NODE_ID=DIM_E_VOLTE_NODE.NODE_ID WHERE KPI_ID=27 AND UTC_DATETIME_ID ='%s' order by node_name"%(SQLConfig[1])
        else:
            targetSQL="SELECT DATETIME_ID,UTC_DATETIME_ID, DC_E_VOLTE_KPI_RAW.NODE_ID,DIM_E_VOLTE_NODE.NODE_NAME,DC_E_VOLTE_KPI_RAW.KPI_VALUE FROM DC_E_VOLTE_KPI_RAW INNER join DIM_E_VOLTE_NODE on DC_E_VOLTE_KPI_RAW.NODE_ID=DIM_E_VOLTE_NODE.NODE_ID WHERE KPI_ID=27 AND UTC_DATETIME_ID ='%s' and node_name ='%s' order by node_name"%(SQLConfig[1],SQLConfig[2])
#27y

#28x
    elif SQLConfig[0] =='28':
        if noNode ==1:
            targetSQL="SELECT DATETIME_ID,UTC_DATETIME_ID, DC_E_VOLTE_KPI_RAW.NODE_ID,DIM_E_VOLTE_NODE.NODE_NAME,DC_E_VOLTE_KPI_RAW.KPI_VALUE FROM DC_E_VOLTE_KPI_RAW INNER join DIM_E_VOLTE_NODE on DC_E_VOLTE_KPI_RAW.NODE_ID=DIM_E_VOLTE_NODE.NODE_ID WHERE KPI_ID=28 AND UTC_DATETIME_ID ='%s' order by node_name"%(SQLConfig[1])
        else:
            targetSQL="SELECT DATETIME_ID,UTC_DATETIME_ID, DC_E_VOLTE_KPI_RAW.NODE_ID,DIM_E_VOLTE_NODE.NODE_NAME,DC_E_VOLTE_KPI_RAW.KPI_VALUE FROM DC_E_VOLTE_KPI_RAW INNER join DIM_E_VOLTE_NODE on DC_E_VOLTE_KPI_RAW.NODE_ID=DIM_E_VOLTE_NODE.NODE_ID WHERE KPI_ID=28 AND UTC_DATETIME_ID ='%s' and node_name ='%s' order by node_name"%(SQLConfig[1],SQLConfig[2])
#28y

#29x
    elif SQLConfig[0] =='29':
        if noNode ==1:
            targetSQL="SELECT DATETIME_ID,UTC_DATETIME_ID, DC_E_VOLTE_KPI_RAW.NODE_ID,DIM_E_VOLTE_NODE.NODE_NAME,DC_E_VOLTE_KPI_RAW.KPI_VALUE FROM DC_E_VOLTE_KPI_RAW INNER join DIM_E_VOLTE_NODE on DC_E_VOLTE_KPI_RAW.NODE_ID=DIM_E_VOLTE_NODE.NODE_ID WHERE KPI_ID=29 AND DATETIME_ID ='%s' order by node_name"%(SQLConfig[1])
        else:
            targetSQL="SELECT DATETIME_ID,UTC_DATETIME_ID, DC_E_VOLTE_KPI_RAW.NODE_ID,DIM_E_VOLTE_NODE.NODE_NAME,DC_E_VOLTE_KPI_RAW.KPI_VALUE FROM DC_E_VOLTE_KPI_RAW INNER join DIM_E_VOLTE_NODE on DC_E_VOLTE_KPI_RAW.NODE_ID=DIM_E_VOLTE_NODE.NODE_ID WHERE KPI_ID=29 AND DATETIME_ID ='%s' and node_name ='%s' order by node_name"%(SQLConfig[1],SQLConfig[2])
#29y

#30x
    elif SQLConfig[0] =='30':
        if noNode ==1:
            targetSQL="SELECT DATETIME_ID,UTC_DATETIME_ID, DC_E_VOLTE_KPI_RAW.NODE_ID,DIM_E_VOLTE_NODE.NODE_NAME,DC_E_VOLTE_KPI_RAW.KPI_VALUE FROM DC_E_VOLTE_KPI_RAW INNER join DIM_E_VOLTE_NODE on DC_E_VOLTE_KPI_RAW.NODE_ID=DIM_E_VOLTE_NODE.NODE_ID WHERE KPI_ID=30 AND DATETIME_ID ='%s' order by node_name"%(SQLConfig[1])
        else:
            targetSQL="SELECT DATETIME_ID,UTC_DATETIME_ID, DC_E_VOLTE_KPI_RAW.NODE_ID,DIM_E_VOLTE_NODE.NODE_NAME,DC_E_VOLTE_KPI_RAW.KPI_VALUE FROM DC_E_VOLTE_KPI_RAW INNER join DIM_E_VOLTE_NODE on DC_E_VOLTE_KPI_RAW.NODE_ID=DIM_E_VOLTE_NODE.NODE_ID WHERE KPI_ID=30 AND DATETIME_ID ='%s' and node_name ='%s' order by node_name"%(SQLConfig[1],SQLConfig[2])
#30y

#31x
    elif SQLConfig[0] =='31':
        if noNode ==1:
            targetSQL="SELECT DATETIME_ID,UTC_DATETIME_ID, DC_E_VOLTE_KPI_RAW.NODE_ID,DIM_E_VOLTE_NODE.NODE_NAME,DC_E_VOLTE_KPI_RAW.KPI_VALUE FROM DC_E_VOLTE_KPI_RAW INNER join DIM_E_VOLTE_NODE on DC_E_VOLTE_KPI_RAW.NODE_ID=DIM_E_VOLTE_NODE.NODE_ID WHERE KPI_ID=31 AND DATETIME_ID ='%s' order by node_name"%(SQLConfig[1])
        else:
            targetSQL="SELECT DATETIME_ID,UTC_DATETIME_ID, DC_E_VOLTE_KPI_RAW.NODE_ID,DIM_E_VOLTE_NODE.NODE_NAME,DC_E_VOLTE_KPI_RAW.KPI_VALUE FROM DC_E_VOLTE_KPI_RAW INNER join DIM_E_VOLTE_NODE on DC_E_VOLTE_KPI_RAW.NODE_ID=DIM_E_VOLTE_NODE.NODE_ID WHERE KPI_ID=31 AND DATETIME_ID ='%s' and node_name ='%s' order by node_name"%(SQLConfig[1],SQLConfig[2])
#31y

#32x
    elif SQLConfig[0] =='32':
        if noNode ==1:
            targetSQL="SELECT DATETIME_ID,UTC_DATETIME_ID, DC_E_VOLTE_KPI_RAW.NODE_ID,DIM_E_VOLTE_NODE.NODE_NAME,DC_E_VOLTE_KPI_RAW.KPI_VALUE FROM DC_E_VOLTE_KPI_RAW INNER join DIM_E_VOLTE_NODE on DC_E_VOLTE_KPI_RAW.NODE_ID=DIM_E_VOLTE_NODE.NODE_ID WHERE KPI_ID=32 AND DATETIME_ID ='%s' order by node_name"%(SQLConfig[1])
        else:
            targetSQL="SELECT DATETIME_ID,UTC_DATETIME_ID, DC_E_VOLTE_KPI_RAW.NODE_ID,DIM_E_VOLTE_NODE.NODE_NAME,DC_E_VOLTE_KPI_RAW.KPI_VALUE FROM DC_E_VOLTE_KPI_RAW INNER join DIM_E_VOLTE_NODE on DC_E_VOLTE_KPI_RAW.NODE_ID=DIM_E_VOLTE_NODE.NODE_ID WHERE KPI_ID=32 AND DATETIME_ID ='%s' and node_name ='%s' order by node_name"%(SQLConfig[1],SQLConfig[2])
#32y

#33x
    elif SQLConfig[0] =='33':
        if noNode ==1:
            targetSQL="SELECT DC_E_VOLTE_KPI_RAW.NODE_ID,DIM_E_VOLTE_NODE.NODE_NAME,DC_E_VOLTE_KPI_RAW.KPI_VALUE,DATETIME_ID,UTC_DATETIME_ID FROM DC_E_VOLTE_KPI_RAW INNER join DIM_E_VOLTE_NODE on DC_E_VOLTE_KPI_RAW.NODE_ID=DIM_E_VOLTE_NODE.NODE_ID WHERE KPI_ID=33 AND UTC_DATETIME_ID ='%s' order by node_name" %(SQLConfig[1])
        else:
            targetSQL="SELECT DC_E_VOLTE_KPI_RAW.NODE_ID,DIM_E_VOLTE_NODE.NODE_NAME,DC_E_VOLTE_KPI_RAW.KPI_VALUE,DATETIME_ID,UTC_DATETIME_ID FROM DC_E_VOLTE_KPI_RAW INNER join DIM_E_VOLTE_NODE on DC_E_VOLTE_KPI_RAW.NODE_ID=DIM_E_VOLTE_NODE.NODE_ID WHERE KPI_ID=33 AND UTC_DATETIME_ID ='%s' and node_name= '%s' order by node_name" %(SQLConfig[1],SQLConfig[2])
#33y

#34x
    elif SQLConfig[0] =='34':
        if noNode ==1:
            targetSQL="SELECT DATETIME_ID,UTC_DATETIME_ID, DC_E_VOLTE_KPI_RAW.NODE_ID,DIM_E_VOLTE_NODE.NODE_NAME,DC_E_VOLTE_KPI_RAW.KPI_VALUE FROM DC_E_VOLTE_KPI_RAW INNER join DIM_E_VOLTE_NODE on DC_E_VOLTE_KPI_RAW.NODE_ID=DIM_E_VOLTE_NODE.NODE_ID WHERE KPI_ID=34 AND  UTC_DATETIME_ID ='%s' order by node_name"%(SQLConfig[1])
        else:
            targetSQL="SELECT DATETIME_ID,UTC_DATETIME_ID, DC_E_VOLTE_KPI_RAW.NODE_ID,DIM_E_VOLTE_NODE.NODE_NAME,DC_E_VOLTE_KPI_RAW.KPI_VALUE FROM DC_E_VOLTE_KPI_RAW INNER join DIM_E_VOLTE_NODE on DC_E_VOLTE_KPI_RAW.NODE_ID=DIM_E_VOLTE_NODE.NODE_ID WHERE KPI_ID=34 AND  UTC_DATETIME_ID ='%s' and node_name ='%s' order by node_name"%(SQLConfig[1],SQLConfig[2])
#34y

#35x
    elif SQLConfig[0] =='35':
        if noNode ==1:
            targetSQL="SELECT DATETIME_ID,UTC_DATETIME_ID, DC_E_VOLTE_KPI_RAW.NODE_ID,DIM_E_VOLTE_NODE.NODE_NAME,DC_E_VOLTE_KPI_RAW.KPI_VALUE FROM DC_E_VOLTE_KPI_RAW INNER join DIM_E_VOLTE_NODE on DC_E_VOLTE_KPI_RAW.NODE_ID=DIM_E_VOLTE_NODE.NODE_ID WHERE KPI_ID=35 AND  UTC_DATETIME_ID ='%s' order by node_name"%(SQLConfig[1])
        else:
            targetSQL="SELECT DATETIME_ID,UTC_DATETIME_ID, DC_E_VOLTE_KPI_RAW.NODE_ID,DIM_E_VOLTE_NODE.NODE_NAME,DC_E_VOLTE_KPI_RAW.KPI_VALUE FROM DC_E_VOLTE_KPI_RAW INNER join DIM_E_VOLTE_NODE on DC_E_VOLTE_KPI_RAW.NODE_ID=DIM_E_VOLTE_NODE.NODE_ID WHERE KPI_ID=35 AND  UTC_DATETIME_ID ='%s' and node_name ='%s' order by node_name"%(SQLConfig[1],SQLConfig[2])
#35y
    
    return targetSQL
