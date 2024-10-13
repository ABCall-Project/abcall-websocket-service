activate:
	if [ -d "venv" ]; then \
        echo "Python 🐍 environment was activated"; \
    else \
        echo "The folder environment doesn't exist"; \
		python -m venv venv; \
        echo "The environment folder was created and the python 🐍 environment was activated"; \
    fi
	. ./venv/bin/activate

install:
	pip3 install -r requirements.txt

run:
	@if [ -z "$(strip $(PORT))" ]; then \
		flask run; \
	else \
		flask run -p $(PORT); \
	fi

run-tests:
	 FLASK_ENV=test python -m unittest discover -s tests -p '*Test.py' -v

run-tests-coverage:
	 coverage run -m unittest discover
	 coverage report -m
	 coverage html
	 coverage report --fail-under=50

run-docker:
ifeq ($(strip $(PORT)),)
	flask run -h 0.0.0.0
else
	flask run -p $(PORT) -h 0.0.0.0
endif

docker-gunicorn:
	  gunicorn -w 4 --bind 127.0.0.1:$(PORT) wsgi:app &
	  python websocket.py

docker-up:
	docker compose up --build

docker-down:
	docker compose down

docker-dev-up:
	docker compose -f=docker-compose.develop.yml up --build

docker-dev-down:
	docker compose -f=docker-compose.develop.yml down

kubernetes-up:
	kubectl apply -f kubernetes/k8s-configMap.yaml
	kubectl apply -f kubernetes/k8s-deployment.yaml
	kubectl apply -f kubernetes/k8s-ingress.yaml

kubernetes-dev-up:
	make kubernetes-dev-up
	minikube tunnel

kubernetes-dev-down:
	kubectl delete configMap/websocket-configmap
	kubectl delete deploy/abcall-websocket-service
	kubectl delete ingress/abcall-websocket-ingress

run-websocket:
	python websocket.py