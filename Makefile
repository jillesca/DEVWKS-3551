.DEFAULT_GOAL := workshop

workshop:
	chmod +x ./build_workshop.sh
	source ./build_workshop.sh

run:
	$(MAKE) clean
	docker compose up -d

cli:
	docker exec -it nso-workshop /bin/bash

clean: 
	docker compose down

follow:
	docker logs --follow nso-workshop