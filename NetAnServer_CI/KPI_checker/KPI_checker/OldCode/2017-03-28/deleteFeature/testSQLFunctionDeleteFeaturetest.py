def SQLFunctionSource(SQLConfig,noNode):

#1a
    if SQLConfig[0]=="1":
        if noNode==1:
            sourceSQL="SELECT DATETIME_ID, CELLNAME, MEASURE_VALUE FROM( SELECT EUTRANCELLFDD AS CELLNAME, DATETIME_ID, 100*((pmRrcConnEstabSucc/(pmRrcConnEstabAtt-pmRrcConnEstabAttReatt-(pmRrcConnEstabFailMmeOvlMos+pmRrcConnEstabFailMmeOvlMod))) *(pmS1SigConnEstabSucc/(pmS1SigConnEstabAtt-pmS1SigConnEstabFailMmeOvlMos)) *(pmErabEstabSuccInit/pmErabEstabAttInit)) AS MEASURE_VALUE FROM DC_E_ERBS_EUTRANCELLFDD_RAW WHERE DATETIME_ID='%s'  UNION ALL SELECT EUTRANCELLTDD AS CELLNAME, DATETIME_ID, 100*((pmRrcConnEstabSucc/(pmRrcConnEstabAtt-pmRrcConnEstabAttReatt-(pmRrcConnEstabFailMmeOvlMos+pmRrcConnEstabFailMmeOvlMod))) *(pmS1SigConnEstabSucc/(pmS1SigConnEstabAtt-pmS1SigConnEstabFailMmeOvlMos)) *(pmErabEstabSuccInit/pmErabEstabAttInit)) AS MEASURE_VALUE FROM DC_E_ERBS_EUTRANCELLTDD_RAW WHERE DATETIME_ID='%s')measure ORDER BY CELLNAME" %(SQLConfig[1], SQLConfig[1])
        else:
            sourceSQL="SELECT DATETIME_ID, CELLNAME, MEASURE_VALUE FROM( SELECT EUTRANCELLFDD AS CELLNAME, DATETIME_ID, 100*((pmRrcConnEstabSucc/(pmRrcConnEstabAtt-pmRrcConnEstabAttReatt-(pmRrcConnEstabFailMmeOvlMos+pmRrcConnEstabFailMmeOvlMod))) *(pmS1SigConnEstabSucc/(pmS1SigConnEstabAtt-pmS1SigConnEstabFailMmeOvlMos)) *(pmErabEstabSuccInit/pmErabEstabAttInit)) AS MEASURE_VALUE FROM DC_E_ERBS_EUTRANCELLFDD_RAW WHERE DATETIME_ID='%s' and SN='%s' UNION ALL SELECT EUTRANCELLTDD AS CELLNAME, DATETIME_ID, 100*((pmRrcConnEstabSucc/(pmRrcConnEstabAtt-pmRrcConnEstabAttReatt-(pmRrcConnEstabFailMmeOvlMos+pmRrcConnEstabFailMmeOvlMod))) *(pmS1SigConnEstabSucc/(pmS1SigConnEstabAtt-pmS1SigConnEstabFailMmeOvlMos)) *(pmErabEstabSuccInit/pmErabEstabAttInit)) AS MEASURE_VALUE FROM DC_E_ERBS_EUTRANCELLTDD_RAW WHERE DATETIME_ID='%s' and SN='%s')measure ORDER BY CELLNAME" %(SQLConfig[1], SQLConfig[2], SQLConfig[1], SQLConfig[2])
#1b

return sourceSQL

def SQLFunctionTarget(SQLConfig,noNode):

#1x
    if SQLConfig[0]=="1":
        if noNode==1:
            targetSQL="SELECT DC_CV_ERBS_EUTRANCELL_RAW.MEASURE_ID, DC_CV_ERBS_EUTRANCELL_RAW.MeasureValue, UTC_DATETIME_ID, DATETIME_ID FROM DC_CV_ERBS_EUTRANCELL_RAW WHERE Measure_ID=1 AND UTC_DATETIME_ID ='%s' " %(SQLConfig[1])
        else:
            targetSQL="SELECT DC_CV_ERBS_EUTRANCELL_RAW.MEASURE_ID, DC_CV_ERBS_EUTRANCELL_RAW.MeasureValue, UTC_DATETIME_ID, DATETIME_ID FROM DC_CV_ERBS_EUTRANCELL_RAW WHERE Measure_ID=1 AND UTC_DATETIME_ID ='%s' and Node_FDN='%s'" %(SQLConfig[1], SQLConfig[2])
#1y

return targetSQL

