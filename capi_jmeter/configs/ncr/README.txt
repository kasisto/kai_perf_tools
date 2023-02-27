
1. Create assist.csv

export URL=https://kasisto-testing-en-us-stage-domain-a.kitsys.net
export APPLICATION_SECRET=<secret>
python3 -m helpers.create_csv_for_assistants --targets=prod

2. review config ( ./capi_jmeter/configs/ncr/ncrstage.properties)
a.  set basepath to point to your local directory
b. review tsv for authenticated user csv 

3. run jmeter

sh ./capi_jmeter/bin/jmeter.sh  -t ./capi_jmeter/configs/ncr/kai-random-assist.jmx -p ./capi_jmeter/configs/ncr/ncrstage.properties

