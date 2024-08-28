def SQLFunctionSource(SQLConfig,noNode):
#1a
    #print("SQLConfig")	#edit- this format is unnecessary
    if SQLConfig[0] =='1':
        if noNode==1:
            sourceSQL="SELECT NE_NAME,DATETIME_ID, (100*sum(IKE_SA_Establishment_Success)/sum(IKE_SA_Establishment_Attempts) *(100*sum(Authentication_and_Auth_Success)/sum(Authentication_and_Auth_Attempts)) * (100*sum(Ipsec_Tunnel_Establishment_Success)/sum(Ipsec_Tunnel_Establishment_Attempts)))/10000 as KPI_VALUEs FROM dc_e_wmg_ipsec_summary_stats_raw WHERE datetime_id = '%s' GROUP BY NE_NAME,DATETIME_ID ORDER BY NE_NAME" %(SQLConfig[1])
        else:
            sourceSQL="SELECT NE_NAME,DATETIME_ID, (100*sum(IKE_SA_Establishment_Success)/sum(IKE_SA_Establishment_Attempts) *(100*sum(Authentication_and_Auth_Success)/sum(Authentication_and_Auth_Attempts)) * (100*sum(Ipsec_Tunnel_Establishment_Success)/sum(Ipsec_Tunnel_Establishment_Attempts)))/10000 as KPI_VALUEs FROM dc_e_wmg_ipsec_summary_stats_raw WHERE datetime_id = '%s' and NE_NAME='%s'  GROUP BY NE_NAME,DATETIME_ID ORDER BY NE_NAME" %(SQLConfig[1],SQLConfig[2])
#1b

#2a   
    elif SQLConfig[0] =='2':
        if noNode==1:
            sourceSQL="SELECT NE_NAME,DATETIME_ID, 100*sum(IKE_SA_Establishment_Success)/sum(IKE_SA_Establishment_Attempts) as KPI_VALUEs FROM dc_e_wmg_ipsec_summary_stats_raw WHERE datetime_id = '%s' GROUP BY NE_NAME,DATETIME_ID ORDER BY NE_NAME" %(SQLConfig[1])
        else:
            sourceSQL="SELECT NE_NAME,DATETIME_ID, 100*sum(IKE_SA_Establishment_Success)/sum(IKE_SA_Establishment_Attempts) as KPI_VALUEs FROM dc_e_wmg_ipsec_summary_stats_raw WHERE datetime_id = '%s' and NE_NAME='%s' GROUP BY NE_NAME,DATETIME_ID ORDER BY NE_NAME" %(SQLConfig[1],SQLConfig[2])
#2b

#3a
    elif SQLConfig[0] =='3':
        if noNode==1:
            sourceSQL="SELECT NE_NAME,DATETIME_ID, 100*sum(Authentication_and_Auth_Success)/sum(Authentication_and_Auth_Attempts) as KPI_VALUEs FROM dc_e_wmg_ipsec_summary_stats_raw WHERE datetime_id = '%s' GROUP BY NE_NAME,DATETIME_ID ORDER BY NE_NAME" %(SQLConfig[1])
        else:
            sourceSQL="SELECT NE_NAME,DATETIME_ID, 100*sum(Authentication_and_Auth_Success)/sum(Authentication_and_Auth_Attempts) as KPI_VALUEs FROM dc_e_wmg_ipsec_summary_stats_raw WHERE datetime_id = '%s' and NE_NAME='%s' GROUP BY NE_NAME,DATETIME_ID ORDER BY NE_NAME" %(SQLConfig[1],SQLConfig[2])
#3b

#4a            
    elif SQLConfig[0] =='4':
        if noNode==1:
            sourceSQL="SELECT NE_NAME,DATETIME_ID, 100*sum(Ipsec_Tunnel_Establishment_Success)/sum(Ipsec_Tunnel_Establishment_Attempts) as KPI_VALUEs FROM dc_e_wmg_ipsec_summary_stats_raw WHERE datetime_id = '%s' GROUP BY NE_NAME,DATETIME_ID ORDER BY NE_NAME" %(SQLConfig[1])
        else:
            sourceSQL="SELECT NE_NAME,DATETIME_ID, 100*sum(Ipsec_Tunnel_Establishment_Success)/sum(Ipsec_Tunnel_Establishment_Attempts) as KPI_VALUEs FROM dc_e_wmg_ipsec_summary_stats_raw WHERE datetime_id = '%s' and NE_NAME='%s' GROUP BY NE_NAME,DATETIME_ID ORDER BY NE_NAME" %(SQLConfig[1],SQLConfig[2])
#4b

#5a
    elif SQLConfig[0] =='5':
        if noNode==1:
            sourceSQL="SELECT GGSN,DATETIME_ID, 100*sum(pgwApnCompletedS2bEpsBearerActivation)/sum(pgwApnAttemptedS2bEpsBearerActivation) as KPI_VALUE FROM dc_E_ggsn_apn_raw WHERE datetime_id = '%s' GROUP BY GGSN,DATETIME_ID ORDER BY GGSN" %(SQLConfig[1])
        else:
            sourceSQL="SELECT GGSN,DATETIME_ID, 100*sum(pgwApnCompletedS2bEpsBearerActivation)/sum(pgwApnAttemptedS2bEpsBearerActivation) as KPI_VALUE FROM dc_E_ggsn_apn_raw WHERE datetime_id = '%s' and GGSN='%s' GROUP BY GGSN,DATETIME_ID ORDER BY GGSN" %(SQLConfig[1],SQLConfig[2])
#5b

#6a 
    elif SQLConfig[0] =='6':
        if noNode==1:
            sourceSQL="SELECT g3ManagedElement,OSS_ID, 100 * ( ((counter1.total) + (counter2.total) + (counter3.total))/(counter4.total - counter5.total) ) AS KPI_Value FROM dc.DC_E_IMS_CSCF2_RAW, (select sum(scscfSuccessfulRegistrationPerAccess) total from dc.DC_E_IMS_CSCF2_RAW where g3ManagedElement='cscf_02' and DATETIME_ID='%s') as counter1, (select sum(scscfFailedRegistrationPerAccess) total from dc.DC_E_IMS_CSCF2_RAW where g3ManagedElement='cscf_02' and MOID like '%%IEEE%%' and MOID like '%%400%%' and DATETIME_ID='%s') as counter2, (select sum(scscfFailedRegistrationPerAccess) total from dc.DC_E_IMS_CSCF2_RAW where g3ManagedElement='cscf_02' and MOID like '%%IEEE%%' and MOID like '%%403%%' and DATETIME_ID='%s') as counter3, (select sum(scscfAttemptedRegistrationPerAccess) total from dc.DC_E_IMS_CSCF2_RAW where g3ManagedElement='cscf_02' and DATETIME_ID='%s') as counter4, (select sum(scscfFailedRegistrationPerAccess) total from dc.DC_E_IMS_CSCF2_RAW where g3ManagedElement='cscf_02' and MOID like '%%IEEE%%' and MOID like '%%401%%' and DATETIME_ID='%s') as counter5 WHERE DATETIME_ID='%s' and g3ManagedElement='cscf_02' SELECT NE_NAME,OSS_ID, 100 * ( ((counter1.total) + (counter2.total) + (counter3.total))/(counter4.total - counter5.total) ) AS KPI_Value FROM dc.DC_E_CSCF_REG_RAW, (select sum(scscfSuccessfulRegistrationPerAccess) total from dc.DC_E_CSCF_REG_RAW where NE_NAME='cscf_03' and DATETIME_ID='%s') as counter1, (select sum(scscfFailedRegistrationPerAccess) total from dc.DC_E_CSCF_REG_RAW where NE_NAME='cscf_03' and MOID like '%%IEEE%%' and MOID like '%%400%%' and DATETIME_ID='%s') as counter2, (select sum(scscfFailedRegistrationPerAccess) total from dc.DC_E_CSCF_REG_RAW where NE_NAME='cscf_03' and MOID like '%%IEEE%%' and MOID like '%%403%%' and DATETIME_ID='%s') as counter3, (select sum(scscfAttemptedRegistrationPerAccess) total from dc.DC_E_CSCF_REG_RAW where NE_NAME='cscf_03' and DATETIME_ID='%s') as counter4, (select sum(scscfFailedRegistrationPerAccess) total from dc.DC_E_CSCF_REG_RAW where NE_NAME='cscf_03' and MOID like '%%IEEE%%' and MOID like '%%401%%' and DATETIME_ID='%s') as counter5 WHERE DATETIME_ID='%s' and NE_NAME='cscf_03'" %(SQLConfig[1],SQLConfig[1],SQLConfig[1],SQLConfig[1],SQLConfig[1],SQLConfig[1],SQLConfig[1],SQLConfig[1],SQLConfig[1],SQLConfig[1],SQLConfig[1],SQLConfig[1],)
        else:
            sourceSQL="SELECT g3ManagedElement,OSS_ID, 100 * ( ((counter1.total) + (counter2.total) + (counter3.total))/(counter4.total - counter5.total) ) AS KPI_Value FROM dc.DC_E_IMS_CSCF2_RAW, (select sum(scscfSuccessfulRegistrationPerAccess) total from dc.DC_E_IMS_CSCF2_RAW where g3ManagedElement='%s' and DATETIME_ID='%s') as counter1, (select sum(scscfFailedRegistrationPerAccess) total from dc.DC_E_IMS_CSCF2_RAW where g3ManagedElement='%s' and MOID like '%%IEEE%%' and MOID like '%%400%%' and DATETIME_ID='%s') as counter2, (select sum(scscfFailedRegistrationPerAccess) total from dc.DC_E_IMS_CSCF2_RAW where g3ManagedElement='%s' and MOID like '%%IEEE%%' and MOID like '%%403%%' and DATETIME_ID='%s') as counter3, (select sum(scscfAttemptedRegistrationPerAccess) total from dc.DC_E_IMS_CSCF2_RAW where g3ManagedElement='%s' and DATETIME_ID='%s') as counter4, (select sum(scscfFailedRegistrationPerAccess) total from dc.DC_E_IMS_CSCF2_RAW where g3ManagedElement='%s' and MOID like '%%IEEE%%' and MOID like '%%401%%' and DATETIME_ID='%s') as counter5 WHERE DATETIME_ID='%s' and g3ManagedElement='%s' SELECT NE_NAME,OSS_ID, 100 * ( ((counter1.total) + (counter2.total) + (counter3.total))/(counter4.total - counter5.total) ) AS KPI_Value FROM dc.DC_E_CSCF_REG_RAW, (select sum(scscfSuccessfulRegistrationPerAccess) total from dc.DC_E_CSCF_REG_RAW where NE_NAME='%s' and DATETIME_ID='%s') as counter1, (select sum(scscfFailedRegistrationPerAccess) total from dc.DC_E_CSCF_REG_RAW where NE_NAME='%s' and MOID like '%%IEEE%%' and MOID like '%%400%%' and DATETIME_ID='%s') as counter2, (select sum(scscfFailedRegistrationPerAccess) total from dc.DC_E_CSCF_REG_RAW where NE_NAME='%s' and MOID like '%%IEEE%%' and MOID like '%%403%%' and DATETIME_ID='%s') as counter3, (select sum(scscfAttemptedRegistrationPerAccess) total from dc.DC_E_CSCF_REG_RAW where NE_NAME='%s' and DATETIME_ID='%s') as counter4, (select sum(scscfFailedRegistrationPerAccess) total from dc.DC_E_CSCF_REG_RAW where NE_NAME='%s' and MOID like '%%IEEE%%' and MOID like '%%401%%' and DATETIME_ID='%s') as counter5 WHERE DATETIME_ID='%s' and NE_NAME='%s'" %(SQLConfig[2],SQLConfig[1],SQLConfig[2],SQLConfig[1],SQLConfig[2],SQLConfig[1],SQLConfig[2],SQLConfig[1],SQLConfig[2],SQLConfig[1],SQLConfig[1],SQLConfig[2],SQLConfig[2],SQLConfig[1],SQLConfig[2],SQLConfig[1],SQLConfig[2],SQLConfig[1],SQLConfig[2],SQLConfig[1],SQLConfig[2],SQLConfig[1],SQLConfig[1],SQLConfig[2])
#6b

#7a    
    elif SQLConfig[0] =='7':
        if noNode==1:
            sourceSQL="SELECT g3ManagedElement,OSS_ID, 100 * ( ((counter1.total) + (counter2.total) + (counter3.total) + (counter4.total) + (counter5.total) + (counter6.total) + (counter7.total))/(counter8.total) ) AS KPI_Value FROM dc.DC_E_IMS_CSCF2_RAW, (select sum(scscfOrigSuccessfulEstablishedInvitePerAccess) total from dc.DC_E_IMS_CSCF2_RAW where g3ManagedElement='cscf_01' and DATETIME_ID='%s') as counter1, (select sum(scscfOrigFailedInvitePerAccess) total from dc.DC_E_IMS_CSCF2_RAW where g3ManagedElement='cscf_01' and MOID like '%%IEEE%%' and MOID like '%%403%%' and DATETIME_ID='%s') as counter2, (select sum(scscfOrigFailedInvitePerAccess) total from dc.DC_E_IMS_CSCF2_RAW where g3ManagedElement='cscf_01' and MOID like '%%IEEE%%' and MOID like '%%404%%' and DATETIME_ID='%s') as counter3, (select sum(scscfOrigFailedInvitePerAccess) total from dc.DC_E_IMS_CSCF2_RAW where g3ManagedElement='cscf_01' and MOID like '%%IEEE%%' and MOID like '%%407%%' and DATETIME_ID='%s') as counter4, (select sum(scscfOrigFailedInvitePerAccess) total from dc.DC_E_IMS_CSCF2_RAW where g3ManagedElement='cscf_01' and MOID like '%%IEEE%%' and MOID like '%%484%%' and DATETIME_ID='%s') as counter5, (select sum(scscfOrigFailedInvitePerAccess) total from dc.DC_E_IMS_CSCF2_RAW where g3ManagedElement='cscf_01' and MOID like '%%IEEE%%' and MOID like '%%486%%' and DATETIME_ID='%s') as counter6, (select sum(scscfOrigFailedInvitePerAccess) total from dc.DC_E_IMS_CSCF2_RAW where g3ManagedElement='cscf_01' and MOID like '%%IEEE%%' and MOID like '%%600%%' and DATETIME_ID='%s') as counter7, (select sum(scscfOrigAttemptedInvitePerAccess) total from dc.DC_E_IMS_CSCF2_RAW where g3ManagedElement='cscf_01' and DATETIME_ID='%s') as counter8, WHERE DATETIME_ID='%s' and g3ManagedElement='cscf_01' SELECT NE_NAME,OSS_ID, 100 * ( ((counter1.total) + (counter2.total) + (counter3.total) + (counter4.total) + (counter5.total) + (counter6.total) + (counter7.total))/(counter8.total) ) AS KPI_Value FROM dc.DC_E_CSCF_SESSION_RAW, (select sum(scscfOrigSuccessfulEstablishedInvitePerAccess) total from dc.DC_E_CSCF_SESSION_RAW where NE_NAME='cscf_05' and DATETIME_ID='%s') as counter1, (select sum(scscfOrigFailedInvitePerAccess) total from dc.DC_E_CSCF_SESSION_RAW where NE_NAME='cscf_05' and MOID like '%%IEEE%%' and MOID like '%%403%%' and DATETIME_ID='%s') as counter2, (select sum(scscfOrigFailedInvitePerAccess) total from dc.DC_E_CSCF_SESSION_RAW where NE_NAME='cscf_05' and MOID like '%%IEEE%%' and MOID like '%%404%%' and DATETIME_ID='%s') as counter3, (select sum(scscfOrigFailedInvitePerAccess) total from dc.DC_E_CSCF_SESSION_RAW where NE_NAME='cscf_05' and MOID like '%%IEEE%%' and MOID like '%%407%%' and DATETIME_ID='%s') as counter4, (select sum(scscfOrigFailedInvitePerAccess) total from dc.DC_E_CSCF_SESSION_RAW where NE_NAME='cscf_05' and MOID like '%%IEEE%%' and MOID like '%%484%%' and DATETIME_ID='%s') as counter5, (select sum(scscfOrigFailedInvitePerAccess) total from dc.DC_E_CSCF_SESSION_RAW where NE_NAME='cscf_05' and MOID like '%%IEEE%%' and MOID like '%%486%%' and DATETIME_ID='%s') as counter6, (select sum(scscfOrigFailedInvitePerAccess) total from dc.DC_E_CSCF_SESSION_RAW where NE_NAME='cscf_05' and MOID like '%%IEEE%%' and MOID like '%%600%%' and DATETIME_ID='%s') as counter7, (select sum(scscfOrigAttemptedInvitePerAccess) total from dc.DC_E_CSCF_SESSION_RAW where NE_NAME='cscf_05' and DATETIME_ID='%s') as counter8, WHERE DATETIME_ID='%s' and NE_NAME='cscf_05'" %(SQLConfig[1],SQLConfig[1],SQLConfig[1],SQLConfig[1],SQLConfig[1],SQLConfig[1],SQLConfig[1],SQLConfig[1],SQLConfig[1],SQLConfig[1],SQLConfig[1],SQLConfig[1],SQLConfig[1],SQLConfig[1],SQLConfig[1],SQLConfig[1],SQLConfig[1],SQLConfig[1])
        else:
            sourceSQL="SELECT g3ManagedElement,OSS_ID, 100 * ( ((counter1.total) + (counter2.total) + (counter3.total) + (counter4.total) + (counter5.total) + (counter6.total) + (counter7.total))/(counter8.total) ) AS KPI_Value FROM dc.DC_E_IMS_CSCF2_RAW, (select sum(scscfOrigSuccessfulEstablishedInvitePerAccess) total from dc.DC_E_IMS_CSCF2_RAW where g3ManagedElement='%s' and DATETIME_ID='%s') as counter1, (select sum(scscfOrigFailedInvitePerAccess) total from dc.DC_E_IMS_CSCF2_RAW where g3ManagedElement='%s' and MOID like '%%IEEE%%' and MOID like '%%403%%' and DATETIME_ID='%s') as counter2, (select sum(scscfOrigFailedInvitePerAccess) total from dc.DC_E_IMS_CSCF2_RAW where g3ManagedElement='%s' and MOID like '%%IEEE%%' and MOID like '%%404%%' and DATETIME_ID='%s') as counter3, (select sum(scscfOrigFailedInvitePerAccess) total from dc.DC_E_IMS_CSCF2_RAW where g3ManagedElement='%s' and MOID like '%%IEEE%%' and MOID like '%%407%%' and DATETIME_ID='%s') as counter4, (select sum(scscfOrigFailedInvitePerAccess) total from dc.DC_E_IMS_CSCF2_RAW where g3ManagedElement='%s' and MOID like '%%IEEE%%' and MOID like '%%484%%' and DATETIME_ID='%s') as counter5, (select sum(scscfOrigFailedInvitePerAccess) total from dc.DC_E_IMS_CSCF2_RAW where g3ManagedElement='%s' and MOID like '%%IEEE%%' and MOID like '%%486%%' and DATETIME_ID='%s') as counter6, (select sum(scscfOrigFailedInvitePerAccess) total from dc.DC_E_IMS_CSCF2_RAW where g3ManagedElement='%s' and MOID like '%%IEEE%%' and MOID like '%%600%%' and DATETIME_ID='%s') as counter7, (select sum(scscfOrigAttemptedInvitePerAccess) total from dc.DC_E_IMS_CSCF2_RAW where g3ManagedElement='%s' and DATETIME_ID='%s') as counter8, WHERE DATETIME_ID='%s' and g3ManagedElement='%s' SELECT NE_NAME,OSS_ID, 100 * ( ((counter1.total) + (counter2.total) + (counter3.total) + (counter4.total) + (counter5.total) + (counter6.total) + (counter7.total))/(counter8.total) ) AS KPI_Value FROM dc.DC_E_CSCF_SESSION_RAW, (select sum(scscfOrigSuccessfulEstablishedInvitePerAccess) total from dc.DC_E_CSCF_SESSION_RAW where NE_NAME='%s' and DATETIME_ID='%s') as counter1, (select sum(scscfOrigFailedInvitePerAccess) total from dc.DC_E_CSCF_SESSION_RAW where NE_NAME='%s' and MOID like '%%IEEE%%' and MOID like '%%403%%' and DATETIME_ID='%s') as counter2, (select sum(scscfOrigFailedInvitePerAccess) total from dc.DC_E_CSCF_SESSION_RAW where NE_NAME='%s' and MOID like '%%IEEE%%' and MOID like '%%404%%' and DATETIME_ID='%s') as counter3, (select sum(scscfOrigFailedInvitePerAccess) total from dc.DC_E_CSCF_SESSION_RAW where NE_NAME='%s' and MOID like '%%IEEE%%' and MOID like '%%407%%' and DATETIME_ID='%s') as counter4, (select sum(scscfOrigFailedInvitePerAccess) total from dc.DC_E_CSCF_SESSION_RAW where NE_NAME='%s' and MOID like '%%IEEE%%' and MOID like '%%484%%' and DATETIME_ID='%s') as counter5, (select sum(scscfOrigFailedInvitePerAccess) total from dc.DC_E_CSCF_SESSION_RAW where NE_NAME='%s' and MOID like '%%IEEE%%' and MOID like '%%486%%' and DATETIME_ID='%s') as counter6, (select sum(scscfOrigFailedInvitePerAccess) total from dc.DC_E_CSCF_SESSION_RAW where NE_NAME='%s' and MOID like '%%IEEE%%' and MOID like '%%600%%' and DATETIME_ID='%s') as counter7, (select sum(scscfOrigAttemptedInvitePerAccess) total from dc.DC_E_CSCF_SESSION_RAW where NE_NAME='%s' and DATETIME_ID='%s') as counter8, WHERE DATETIME_ID='%s' and NE_NAME='%s'" %(SQLConfig[2],SQLConfig[1],SQLConfig[2],SQLConfig[1],SQLConfig[2],SQLConfig[1],SQLConfig[2],SQLConfig[1],SQLConfig[2],SQLConfig[1],SQLConfig[2],SQLConfig[1],SQLConfig[2],SQLConfig[1],SQLConfig[2],SQLConfig[1],SQLConfig[1],SQLConfig[2],SQLConfig[1],SQLConfig[2],SQLConfig[1],SQLConfig[2],SQLConfig[1],SQLConfig[2],SQLConfig[1],SQLConfig[2],SQLConfig[1],SQLConfig[2],SQLConfig[1],SQLConfig[2],SQLConfig[1],SQLConfig[2],SQLConfig[1],SQLConfig[1],SQLConfig[1],SQLConfig[2])
#7b

#8a
    elif SQLConfig[0] =='8':
        if noNode==1:
            sourceSQL="SELECT g3ManagedElement,OSS_ID, 100 * ( ((counter1.total) + (counter2.total) + (counter3.total) + (counter4.total) + (counter5.total) + (counter6.total) + (counter7.total))/(counter8.total) ) AS KPI_Value FROM dc.DC_E_IMS_CSCF2_RAW, (select sum(scscfTermSuccessfulEstablishedInvitePerAccess) total from dc.DC_E_IMS_CSCF2_RAW where g3ManagedElement='cscf_01' and DATETIME_ID='%s') as counter1, (select sum(scscfTermFailedInvitePerAccess) total from dc.DC_E_IMS_CSCF2_RAW where g3ManagedElement='cscf_01' and MOID like '%%IEEE%%' and MOID like '%%403%%' and DATETIME_ID='%s') as counter2, (select sum(scscfTermFailedInvitePerAccess) total from dc.DC_E_IMS_CSCF2_RAW where g3ManagedElement='cscf_01' and MOID like '%%IEEE%%' and MOID like '%%404%%' and DATETIME_ID='%s') as counter3, (select sum(scscfTermFailedInvitePerAccess) total from dc.DC_E_IMS_CSCF2_RAW where g3ManagedElement='cscf_01' and MOID like '%%IEEE%%' and MOID like '%%407%%' and DATETIME_ID='%s') as counter4, (select sum(scscfTermFailedInvitePerAccess) total from dc.DC_E_IMS_CSCF2_RAW where g3ManagedElement='cscf_01' and MOID like '%%IEEE%%' and MOID like '%%484%%' and DATETIME_ID='%s') as counter5, (select sum(scscfTermFailedInvitePerAccess) total from dc.DC_E_IMS_CSCF2_RAW where g3ManagedElement='cscf_01' and MOID like '%%IEEE%%' and MOID like '%%486%%' and DATETIME_ID='%s') as counter6, (select sum(scscfTermFailedInvitePerAccess) total from dc.DC_E_IMS_CSCF2_RAW where g3ManagedElement='cscf_01' and MOID like '%%IEEE%%' and MOID like '%%600%%' and DATETIME_ID='%s') as counter7, (select sum(scscfTermAttemptedInvitePerAccess) total from dc.DC_E_IMS_CSCF2_RAW where g3ManagedElement='cscf_01' and DATETIME_ID='%s') as counter8, WHERE DATETIME_ID='%s' and g3ManagedElement='cscf_01' SELECT NE_NAME,OSS_ID, 100 * ( ((counter1.total) + (counter2.total) + (counter3.total) + (counter4.total) + (counter5.total) + (counter6.total) + (counter7.total))/(counter8.total) ) AS KPI_Value FROM dc.DC_E_CSCF_SESSION_RAW, (select sum(scscfTermSuccessfulEstablishedInvitePerAccess) total from dc.DC_E_CSCF_SESSION_RAW where NE_NAME='cscf_05' and DATETIME_ID='%s') as counter1, (select sum(scscfTermFailedInvitePerAccess) total from dc.DC_E_CSCF_SESSION_RAW where NE_NAME='cscf_05' and MOID like '%%IEEE%%' and MOID like '%%403%%' and DATETIME_ID='%s') as counter2, (select sum(scscfTermFailedInvitePerAccess) total from dc.DC_E_CSCF_SESSION_RAW where NE_NAME='cscf_05' and MOID like '%%IEEE%%' and MOID like '%%404%%' and DATETIME_ID='%s') as counter3, (select sum(scscfTermFailedInvitePerAccess) total from dc.DC_E_CSCF_SESSION_RAW where NE_NAME='cscf_05' and MOID like '%%IEEE%%' and MOID like '%%407%%' and DATETIME_ID='%s') as counter4, (select sum(scscfTermFailedInvitePerAccess) total from dc.DC_E_CSCF_SESSION_RAW where NE_NAME='cscf_05' and MOID like '%%IEEE%%' and MOID like '%%484%%' and DATETIME_ID='%s') as counter5, (select sum(scscfTermFailedInvitePerAccess) total from dc.DC_E_CSCF_SESSION_RAW where NE_NAME='cscf_05' and MOID like '%%IEEE%%' and MOID like '%%486%%' and DATETIME_ID='%s') as counter6, (select sum(scscfTermFailedInvitePerAccess) total from dc.DC_E_CSCF_SESSION_RAW where NE_NAME='cscf_05' and MOID like '%%IEEE%%' and MOID like '%%600%%' and DATETIME_ID='%s') as counter7, (select sum(scscfTermAttemptedInvitePerAccess) total from dc.DC_E_CSCF_SESSION_RAW where NE_NAME='cscf_05' and DATETIME_ID='%s') as counter8, WHERE DATETIME_ID='%s' and NE_NAME='cscf_05'" %(SQLConfig[1],SQLConfig[1],SQLConfig[1],SQLConfig[1],SQLConfig[1],SQLConfig[1],SQLConfig[1],SQLConfig[1],SQLConfig[1],SQLConfig[1],SQLConfig[1],SQLConfig[1],SQLConfig[1],SQLConfig[1],SQLConfig[1],SQLConfig[1],SQLConfig[1],SQLConfig[1],)
        else:
            sourceSQL="SELECT g3ManagedElement,OSS_ID, 100 * ( ((counter1.total) + (counter2.total) + (counter3.total) + (counter4.total) + (counter5.total) + (counter6.total) + (counter7.total))/(counter8.total) ) AS KPI_Value FROM dc.DC_E_IMS_CSCF2_RAW, (select sum(scscfTermSuccessfulEstablishedInvitePerAccess) total from dc.DC_E_IMS_CSCF2_RAW where g3ManagedElement='%s' and DATETIME_ID='%s') as counter1, (select sum(scscfTermFailedInvitePerAccess) total from dc.DC_E_IMS_CSCF2_RAW where g3ManagedElement='%s' and MOID like '%%IEEE%%' and MOID like '%%403%%' and DATETIME_ID='%s') as counter2, (select sum(scscfTermFailedInvitePerAccess) total from dc.DC_E_IMS_CSCF2_RAW where g3ManagedElement='%s' and MOID like '%%IEEE%%' and MOID like '%%404%%' and DATETIME_ID='%s') as counter3, (select sum(scscfTermFailedInvitePerAccess) total from dc.DC_E_IMS_CSCF2_RAW where g3ManagedElement='%s' and MOID like '%%IEEE%%' and MOID like '%%407%%' and DATETIME_ID='%s') as counter4, (select sum(scscfTermFailedInvitePerAccess) total from dc.DC_E_IMS_CSCF2_RAW where g3ManagedElement='%s' and MOID like '%%IEEE%%' and MOID like '%%484%%' and DATETIME_ID='%s') as counter5, (select sum(scscfTermFailedInvitePerAccess) total from dc.DC_E_IMS_CSCF2_RAW where g3ManagedElement='%s' and MOID like '%%IEEE%%' and MOID like '%%486%%' and DATETIME_ID='%s') as counter6, (select sum(scscfTermFailedInvitePerAccess) total from dc.DC_E_IMS_CSCF2_RAW where g3ManagedElement='%s' and MOID like '%%IEEE%%' and MOID like '%%600%%' and DATETIME_ID='%s') as counter7, (select sum(scscfTermAttemptedInvitePerAccess) total from dc.DC_E_IMS_CSCF2_RAW where g3ManagedElement='%s' and DATETIME_ID='%s') as counter8, WHERE DATETIME_ID='%s' and g3ManagedElement='%s' SELECT NE_NAME,OSS_ID, 100 * ( ((counter1.total) + (counter2.total) + (counter3.total) + (counter4.total) + (counter5.total) + (counter6.total) + (counter7.total))/(counter8.total) ) AS KPI_Value FROM dc.DC_E_CSCF_SESSION_RAW, (select sum(scscfTermSuccessfulEstablishedInvitePerAccess) total from dc.DC_E_CSCF_SESSION_RAW where NE_NAME='%s' and DATETIME_ID='%s') as counter1, (select sum(scscfTermFailedInvitePerAccess) total from dc.DC_E_CSCF_SESSION_RAW where NE_NAME='%s' and MOID like '%%IEEE%%' and MOID like '%%403%%' and DATETIME_ID='%s') as counter2, (select sum(scscfTermFailedInvitePerAccess) total from dc.DC_E_CSCF_SESSION_RAW where NE_NAME='%s' and MOID like '%%IEEE%%' and MOID like '%%404%%' and DATETIME_ID='%s') as counter3, (select sum(scscfTermFailedInvitePerAccess) total from dc.DC_E_CSCF_SESSION_RAW where NE_NAME='%s' and MOID like '%%IEEE%%' and MOID like '%%407%%' and DATETIME_ID='%s') as counter4, (select sum(scscfTermFailedInvitePerAccess) total from dc.DC_E_CSCF_SESSION_RAW where NE_NAME='%s' and MOID like '%%IEEE%%' and MOID like '%%484%%' and DATETIME_ID='%s') as counter5, (select sum(scscfTermFailedInvitePerAccess) total from dc.DC_E_CSCF_SESSION_RAW where NE_NAME='%s' and MOID like '%%IEEE%%' and MOID like '%%486%%' and DATETIME_ID='%s') as counter6, (select sum(scscfTermFailedInvitePerAccess) total from dc.DC_E_CSCF_SESSION_RAW where NE_NAME='%s' and MOID like '%%IEEE%%' and MOID like '%%600%%' and DATETIME_ID='%s') as counter7, (select sum(scscfTermAttemptedInvitePerAccess) total from dc.DC_E_CSCF_SESSION_RAW where NE_NAME='%s' and DATETIME_ID='%s') as counter8, WHERE DATETIME_ID='%s' and NE_NAME='%s'" %(SQLConfig[2],SQLConfig[1],SQLConfig[2],SQLConfig[1],SQLConfig[2],SQLConfig[1],SQLConfig[2],SQLConfig[1],SQLConfig[2],SQLConfig[1],SQLConfig[2],SQLConfig[1],SQLConfig[2],SQLConfig[1],SQLConfig[2],SQLConfig[1],SQLConfig[1],SQLConfig[2],SQLConfig[2],SQLConfig[1],SQLConfig[2],SQLConfig[1],SQLConfig[2],SQLConfig[1],SQLConfig[2],SQLConfig[1],SQLConfig[2],SQLConfig[1],SQLConfig[2],SQLConfig[1],SQLConfig[2],SQLConfig[1],SQLConfig[2],SQLConfig[1],SQLConfig[1],SQLConfig[2])
#8b
    
#9a    
    elif SQLConfig[0] =='9':
        if noNode==1:
            sourceSQL="SELECT GGSN,DATETIME_ID, 100*sum(IratHoCompFromUwlanToEutran)/sum(IratHoAttFromUwlanToEutran) as KPI_VALUE FROM dc_E_ggsn_ggsn_raw WHERE datetime_id = '%s' GROUP BY GGSN,DATETIME_ID ORDER BY GGSN" %(SQLConfig[1])
        else:
            sourceSQL="SELECT GGSN,DATETIME_ID, 100*sum(IratHoCompFromUwlanToEutran)/sum(IratHoAttFromUwlanToEutran) as KPI_VALUE FROM dc_E_ggsn_ggsn_raw WHERE datetime_id = '%s' and GGSN='%s' GROUP BY GGSN,DATETIME_ID ORDER BY GGSN" %(SQLConfig[1],SQLConfig[2])
#9b
    
#10a
    elif SQLConfig[0] =='10':
        if noNode==1:
            sourceSQL="select  OSS_ID, g3ManagedElement,100*(( MtasFuncTermTermSessOk + MtasFuncTermTermSessNOkE)/(MtasFuncTermTermSessOk+MtasFuncTermTermSessNOkI+MtasFuncTermTermSessNOkE)) as KPI_VALUE from DC_E_MTAS_MTASQOS_RAW where UTC_DATETIME_ID ='%s' ORDER BY g3ManagedElement"%(SQLConfig[1])
        else:
            sourceSQL="select  OSS_ID, g3ManagedElement,100*(( MtasFuncTermTermSessOk + MtasFuncTermTermSessNOkE)/(MtasFuncTermTermSessOk+MtasFuncTermTermSessNOkI+MtasFuncTermTermSessNOkE)) as KPI_VALUE from DC_E_MTAS_MTASQOS_RAW where UTC_DATETIME_ID ='%s' and g3ManagedElement='%s' ORDER BY g3ManagedElement"%(SQLConfig[1],SQLConfig[2])
#10b
    #print(sourceSQL)	#edit- I think this is only here for error checking
    return sourceSQL
def SQLFunctionTarget(SQLConfig,noNode):
#1x
    if SQLConfig[0] =='1':
        #depending on the value of NoNode it sets a varible equal to a SQL command with string formatters replacing the configurable option found in the command
        if noNode ==1:
            targetSQL="SELECT DC_E_VOWIFI_KPI_RAW.NODE_ID,DIM_E_VOWIFI_NODE.NODE_NAME,DC_E_VOWIFI_KPI_RAW.KPI_VALUE FROM DC_E_VOWIFI_KPI_RAW INNER join DIM_E_VOWIFI_NODE on DC_E_VOWIFI_KPI_RAW.NODE_ID=DIM_E_VOWIFI_NODE.NODE_ID WHERE KPI_ID=1 AND DATETIME_ID ='%s' ORDER BY NODE_NAME" %(SQLConfig[1])
        else:
            targetSQL="SELECT DC_E_VOWIFI_KPI_RAW.NODE_ID,DIM_E_VOWIFI_NODE.NODE_NAME,DC_E_VOWIFI_KPI_RAW.KPI_VALUE FROM DC_E_VOWIFI_KPI_RAW INNER join DIM_E_VOWIFI_NODE on DC_E_VOWIFI_KPI_RAW.NODE_ID=DIM_E_VOWIFI_NODE.NODE_ID WHERE KPI_ID=1 AND DATETIME_ID ='%s' and node_name='%s' ORDER BY NODE_NAME" %(SQLConfig[1],SQLConfig[2])
#1y

#2x   
    elif SQLConfig[0] =='2':
        if noNode ==1:
            targetSQL="SELECT DC_E_VOWIFI_KPI_RAW.NODE_ID,DIM_E_VOWIFI_NODE.NODE_NAME,DC_E_VOWIFI_KPI_RAW.KPI_VALUE FROM DC_E_VOWIFI_KPI_RAW INNER join DIM_E_VOWIFI_NODE on DC_E_VOWIFI_KPI_RAW.NODE_ID=DIM_E_VOWIFI_NODE.NODE_ID WHERE KPI_ID=2 AND DATETIME_ID ='%s' ORDER BY NODE_NAME" %(SQLConfig[1])
        else:
            targetSQL="SELECT DC_E_VOWIFI_KPI_RAW.NODE_ID,DIM_E_VOWIFI_NODE.NODE_NAME,DC_E_VOWIFI_KPI_RAW.KPI_VALUE FROM DC_E_VOWIFI_KPI_RAW INNER join DIM_E_VOWIFI_NODE on DC_E_VOWIFI_KPI_RAW.NODE_ID=DIM_E_VOWIFI_NODE.NODE_ID WHERE KPI_ID=2 AND DATETIME_ID ='%s' and node_name='%s' ORDER BY NODE_NAME" %(SQLConfig[1],SQLConfig[2])
#2y

#3x
    elif SQLConfig[0] =='3':
        if noNode ==1:
            targetSQL="SELECT DC_E_VOWIFI_KPI_RAW.NODE_ID,DIM_E_VOWIFI_NODE.NODE_NAME,DC_E_VOWIFI_KPI_RAW.KPI_VALUE FROM DC_E_VOWIFI_KPI_RAW INNER join DIM_E_VOWIFI_NODE on DC_E_VOWIFI_KPI_RAW.NODE_ID=DIM_E_VOWIFI_NODE.NODE_ID WHERE KPI_ID=3 AND DATETIME_ID ='%s' ORDER BY NODE_NAME" %(SQLConfig[1])
        else:
            targetSQL="SELECT DC_E_VOWIFI_KPI_RAW.NODE_ID,DIM_E_VOWIFI_NODE.NODE_NAME,DC_E_VOWIFI_KPI_RAW.KPI_VALUE FROM DC_E_VOWIFI_KPI_RAW INNER join DIM_E_VOWIFI_NODE on DC_E_VOWIFI_KPI_RAW.NODE_ID=DIM_E_VOWIFI_NODE.NODE_ID WHERE KPI_ID=3 AND DATETIME_ID ='%s' and node_name ='%s' ORDER BY NODE_NAME" %(SQLConfig[1],SQLConfig[2])
#3y

#4x            
    elif SQLConfig[0] =='4':
        if noNode ==1:
            targetSQL="SELECT DC_E_VOWIFI_KPI_RAW.NODE_ID,DIM_E_VOWIFI_NODE.NODE_NAME,DC_E_VOWIFI_KPI_RAW.KPI_VALUE FROM DC_E_VOWIFI_KPI_RAW INNER join DIM_E_VOWIFI_NODE on DC_E_VOWIFI_KPI_RAW.NODE_ID=DIM_E_VOWIFI_NODE.NODE_ID WHERE KPI_ID=4 AND DATETIME_ID ='%s' ORDER BY NODE_NAME" %(SQLConfig[1])
        else:
            targetSQL="SELECT DC_E_VOWIFI_KPI_RAW.NODE_ID,DIM_E_VOWIFI_NODE.NODE_NAME,DC_E_VOWIFI_KPI_RAW.KPI_VALUE FROM DC_E_VOWIFI_KPI_RAW INNER join DIM_E_VOWIFI_NODE on DC_E_VOWIFI_KPI_RAW.NODE_ID=DIM_E_VOWIFI_NODE.NODE_ID WHERE KPI_ID=4 AND DATETIME_ID ='%s' and node_name ='%s' ORDER BY NODE_NAME" %(SQLConfig[1],SQLConfig[2])
#4y

#5x
    elif SQLConfig[0] =='5':
        if noNode ==1:
            targetSQL="SELECT DC_E_VOWIFI_KPI_RAW.NODE_ID,DIM_E_VOWIFI_NODE.NODE_NAME,DC_E_VOWIFI_KPI_RAW.KPI_VALUE FROM DC_E_VOWIFI_KPI_RAW INNER join DIM_E_VOWIFI_NODE on DC_E_VOWIFI_KPI_RAW.NODE_ID=DIM_E_VOWIFI_NODE.NODE_ID WHERE KPI_ID=5 AND DATETIME_ID ='%s' ORDER BY NODE_NAME" %(SQLConfig[1])
        else:
            targetSQL="SELECT DC_E_VOWIFI_KPI_RAW.NODE_ID,DIM_E_VOWIFI_NODE.NODE_NAME,DC_E_VOWIFI_KPI_RAW.KPI_VALUE FROM DC_E_VOWIFI_KPI_RAW INNER join DIM_E_VOWIFI_NODE on DC_E_VOWIFI_KPI_RAW.NODE_ID=DIM_E_VOWIFI_NODE.NODE_ID WHERE KPI_ID=5 AND DATETIME_ID ='%s' and node_name ='%s' ORDER BY NODE_NAME" %(SQLConfig[1],SQLConfig[2])
#5y

#6x 
    elif SQLConfig[0] =='6':
        if noNode ==1:
            targetSQL="SELECT DC_E_VOWIFI_KPI_RAW.NODE_ID,DIM_E_VOWIFI_NODE.NODE_NAME,DC_E_VOWIFI_KPI_RAW.KPI_VALUE FROM DC_E_VOWIFI_KPI_RAW INNER join DIM_E_VOWIFI_NODE on DC_E_VOWIFI_KPI_RAW.NODE_ID=DIM_E_VOWIFI_NODE.NODE_ID WHERE KPI_ID=6 AND DATETIME_ID ='%s' ORDER BY NODE_NAME" %(SQLConfig[1])
        else:
            targetSQL="SELECT DC_E_VOWIFI_KPI_RAW.NODE_ID,DIM_E_VOWIFI_NODE.NODE_NAME,DC_E_VOWIFI_KPI_RAW.KPI_VALUE FROM DC_E_VOWIFI_KPI_RAW INNER join DIM_E_VOWIFI_NODE on DC_E_VOWIFI_KPI_RAW.NODE_ID=DIM_E_VOWIFI_NODE.NODE_ID WHERE KPI_ID=6 AND DATETIME_ID ='%s' and node_name ='%s' ORDER BY NODE_NAME" %(SQLConfig[1],SQLConfig[2])
#6y

#7x    
    elif SQLConfig[0] =='7':
        if noNode ==1:
            targetSQL="SELECT DC_E_VOWIFI_KPI_RAW.NODE_ID,DIM_E_VOWIFI_NODE.NODE_NAME,DC_E_VOWIFI_KPI_RAW.KPI_VALUE FROM DC_E_VOWIFI_KPI_RAW INNER join DIM_E_VOWIFI_NODE on DC_E_VOWIFI_KPI_RAW.NODE_ID=DIM_E_VOWIFI_NODE.NODE_ID WHERE KPI_ID=7 AND DATETIME_ID ='%s' ORDER BY NODE_NAME" %(SQLConfig[1])
        else:
            targetSQL="SELECT DC_E_VOWIFI_KPI_RAW.NODE_ID,DIM_E_VOWIFI_NODE.NODE_NAME,DC_E_VOWIFI_KPI_RAW.KPI_VALUE FROM DC_E_VOWIFI_KPI_RAW INNER join DIM_E_VOWIFI_NODE on DC_E_VOWIFI_KPI_RAW.NODE_ID=DIM_E_VOWIFI_NODE.NODE_ID WHERE KPI_ID=7 AND DATETIME_ID ='%s' and node_name= '%s' ORDER BY NODE_NAME" %(SQLConfig[1],SQLConfig[2])
#7y

#8x
    elif SQLConfig[0] =='8':
        if noNode ==1:
            targetSQL="SELECT DC_E_VOWIFI_KPI_RAW.NODE_ID,DIM_E_VOWIFI_NODE.NODE_NAME,DC_E_VOWIFI_KPI_RAW.KPI_VALUE FROM DC_E_VOWIFI_KPI_RAW INNER join DIM_E_VOWIFI_NODE on DC_E_VOWIFI_KPI_RAW.NODE_ID=DIM_E_VOWIFI_NODE.NODE_ID WHERE KPI_ID=8 AND DATETIME_ID ='%s' ORDER BY NODE_NAME" %(SQLConfig[1])
        else:
            targetSQL="SELECT DC_E_VOWIFI_KPI_RAW.NODE_ID,DIM_E_VOWIFI_NODE.NODE_NAME,DC_E_VOWIFI_KPI_RAW.KPI_VALUE FROM DC_E_VOWIFI_KPI_RAW INNER join DIM_E_VOWIFI_NODE on DC_E_VOWIFI_KPI_RAW.NODE_ID=DIM_E_VOWIFI_NODE.NODE_ID WHERE KPI_ID=8 AND DATETIME_ID ='%s' and node_name ='%s' ORDER BY NODE_NAME" %(SQLConfig[1],SQLConfig[2])
#8y
    
#9x    
    elif SQLConfig[0] =='9':
        if noNode ==1:
            targetSQL="SELECT DC_E_VOWIFI_KPI_RAW.NODE_ID,DIM_E_VOWIFI_NODE.NODE_NAME,DC_E_VOWIFI_KPI_RAW.KPI_VALUE FROM DC_E_VOWIFI_KPI_RAW INNER join DIM_E_VOWIFI_NODE on DC_E_VOWIFI_KPI_RAW.NODE_ID=DIM_E_VOWIFI_NODE.NODE_ID WHERE KPI_ID=9 AND DATETIME_ID ='%s' ORDER BY NODE_NAME" %(SQLConfig[1])
        else:
            targetSQL="SELECT DC_E_VOWIFI_KPI_RAW.NODE_ID,DIM_E_VOWIFI_NODE.NODE_NAME,DC_E_VOWIFI_KPI_RAW.KPI_VALUE FROM DC_E_VOWIFI_KPI_RAW INNER join DIM_E_VOWIFI_NODE on DC_E_VOWIFI_KPI_RAW.NODE_ID=DIM_E_VOWIFI_NODE.NODE_ID WHERE KPI_ID=9 AND DATETIME_ID ='%s' and node_name ='%s' ORDER BY NODE_NAME" %(SQLConfig[1],SQLConfig[2])
#9y
    
#10x
    elif SQLConfig[0] =='10':
        if noNode ==1:
            targetSQL="SELECT DC_E_VOWIFI_KPI_RAW.NODE_ID,DIM_E_VOWIFI_NODE.NODE_NAME,DC_E_VOWIFI_KPI_RAW.KPI_VALUE FROM DC_E_VOWIFI_KPI_RAW INNER join DIM_E_VOWIFI_NODE on DC_E_VOWIFI_KPI_RAW.NODE_ID=DIM_E_VOWIFI_NODE.NODE_ID WHERE KPI_ID=10 AND DATETIME_ID ='%s' ORDER BY NODE_NAME" %(SQLConfig[1])
        else:
            targetSQL="SELECT DC_E_VOWIFI_KPI_RAW.NODE_ID,DIM_E_VOWIFI_NODE.NODE_NAME,DC_E_VOWIFI_KPI_RAW.KPI_VALUE FROM DC_E_VOWIFI_KPI_RAW INNER join DIM_E_VOWIFI_NODE on DC_E_VOWIFI_KPI_RAW.NODE_ID=DIM_E_VOWIFI_NODE.NODE_ID WHERE KPI_ID=10 AND DATETIME_ID ='%s' and node_name ='%s' ORDER BY NODE_NAME" %(SQLConfig[1],SQLConfig[2])
#10y
    return targetSQL
