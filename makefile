# Run make to build the docker container 
# Ensure that you have downloaded experiment data from OSF

build:
	docker build ./ -t adamnhornsby/fluency-model

deploy:
	docker push adamnhornsby/fluency-model