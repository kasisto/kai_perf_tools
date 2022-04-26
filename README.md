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

The kai.jmx defines a JMeter Project for executing a series of requests (based on a CSV) against a target environment.

The requests are defined in the files Authenticated_questions.csv and Unauthenticated_questions.csv
The tokens can be fixed or generated randomly
The assistant configs are fixed in the kai.jmx at this time.

The are parameters to define how many concurrent requests to make and how long to run the tests for. 

To get started:

1. cd /capi_jmeter/bin
2. sh jmeter -p ../configs/kcb/<env>.properties -t ../configs/kcb/kai.jmx
  e.g. 
  sh jmeter -p ../configs/kcb/webviewqa.properties -t ../configs/kcb/kai.jmx
  sh jmeter -p ../configs/kcb/webviewstage.properties -t ../configs/kcb/kai.jmx

When JMeter loads:
1. Click Green Arrow
2. Review summary report and aggregate report to determine if report meets perf threshold.
  
  Profiled Result - https://docs.google.com/spreadsheets/d/15VcWL_pjHQ5wmE3CALkjNH0g2i28-NGVptOgii0IDOA/edit#gid=912920869

