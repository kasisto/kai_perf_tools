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


To create assistants and create assistant version afterwards

    python -m helpers.create_assistants_and_assistant_versions --n_assistants=3 --package=ASSISTANT-kcb-4-18-2022-e59d30b2a5d8089940262ec9d351b79d.tar.gz --autopublish_to=stage,prod --n_versions=2

To generate csv for existing assistants in environment

    python -m helpers.create_csv_for_assistants --targets=stage,prod

To import package to assistant (By default, we import package to application. So if we don't want to import package to assistant, we should not define assistant_ids and autopublish_to parameters:
    
    python -m helpers.import_package --package=ASSISTANT-2022_06_23_16_57_25_304436-kcb-en_US-4e038d54ca3dcb905193ad0a83592664.tar.gz --autopublish_to=stage,prod --assistant_ids=default_assistant,default_assistant_2
