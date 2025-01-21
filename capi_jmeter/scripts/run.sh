
rm -rf configs/kcb/reports/html/
rm -r configs/kcb/reports/*
mkdir -p configs/kcb/reports/html/

sh bin/jmeter \
  -n \
  -t configs/kcb/tests/test_authenticated_questions.jmx \
  -p configs/kcb/properties/runner.properties \
  -l configs/kcb/reports/results.jtl \
  -j configs/kcb/reports/jmeter.log \
  -e \
  -o configs/kcb/reports/html/ \
  -Jloops=-1 \
  -Jlog_level.jmeter=DEBUG \
  -Japi_version=5.5 \
  -Jstart_threads_count=1 \
  -Jinitial_delay=1 \
  -Jstartup_time=3 \
  -Jhold_load_for=20 \
  -Jshutdown_time=3 \
  -Jconstant_timer=1