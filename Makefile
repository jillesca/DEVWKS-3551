.DEFAULT_GOAL := workshop

workshop:
	chmod +x ~/src/DEVWKS-3551/build_workshop.sh
	source ~/src/DEVWKS-3551/build_workshop.sh

run:
	$(MAKE) clean
	docker compose up -d

cli:
	docker exec -it nso-workshop /bin/bash

clean: 
	docker compose down

follow:
	docker logs --follow nso-workshop