First, we need to export some environment variables. The values depend on which environment you are going to run the tests for.

Export URL=ENVIRONMENT_URL 
export ASSISTANT_SECRET=ASSISTANT_SECRET
export ASSISTANT_NAME=ASSISTANT_NAME
export APPLICATION_SECRET=APPLICATION_SECRET

To create assistants:
    python perf_helper.py --n=49 --assistant=True

This will generate a csv file named assistant.csv. The csv can be used on 
JMeter when testing multiple assistants.
	

To create assistant versions:
	python perf_helper.py --n=49 --assistant=False

--n = number of document to be created
