### How to use

First, we need to export some environment variables. The values depend on which environment you are going to run the tests for.

	export URL=ENVIRONMENT_URL 
	export ASSISTANT_SECRET=DEFAULT_ASSISTANT_SECRET
	export ASSISTANT_NAME=DEFAULT_ASSISTANT_NAME
	export APPLICATION_SECRET=APPLICATION_SECRET
	export PACKAGING_SECRET=PACKAGING_SECRET

To create assistants:
    
    python -m helpers.create_assistants
    
    You can pass the ff. arguments:
        --n = number of assistants to be created
        --package = package to be uploaded(package needs to be in the package folder)
        --autopublish_to = autopublish documents to target

    Example:
    python -m helpers.create_assistants --n=10 --package=ASSISTANT-kcb-10-20-2021-cfa99127a9886ba5af583826b7a4d771.tar.gz --autopublish_to=stage,prod

    This will generate a csv file named assistant.csv. The csv can be used on 
    JMeter when testing multiple assistants.
	

To create assistant versions:
    
    python -m helpers.create_assistant_versions --n=1

    --n = number of document to be created
