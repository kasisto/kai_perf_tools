### To add Assistant Credentials

- update capi_jmeter/configs/common/Assist.csv

### To add CAPI Unauthenticated request

- update capi_jmeter/configs/common/Unauthenticated_questions.csv

### To add CAPI Authenticated request

- update capi_jmeter/configs/common/Authenticated_questions.csv

### To add CAPI Web Hook Negative

- update capi_jmeter/configs/common/web_hook_negative.csv

### To add CAPI Web Hook Positive

- update capi_jmeter/configs/common/web_hook_positive.csv

### To view results point to

- update capi_jmeter/configs/common/ResultTree.csv



### How to Run KCB Perf tests

cd /capi_jmeter/bin

sh jmeter -p ../configs/kcb/<env>.properties -t ../configs/kcb/kai.jmx
  
e.g. 
sh jmeter -p ../configs/kcb/webviewqa.properties -t ../configs/kcb/kai.jmx
sh jmeter -p ../configs/kcb/webviewstage.properties -t ../configs/kcb/kai.jmx

When JMeter loads:
1. Click Green Arrow
2. Review summary report and aggregrate report to determine if report meets perf threshold.

