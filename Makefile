all: clean run-server

run-server:
	python3 -m server.server

run-client:
	python3 -m client.client
	
test:
	tox

clean:
	@echo "Cleaning up..."
	@rm -rf .tox
	@rm -rf *storage
	@rm -rf client/downloads
	@rm -f *.db *.xml .coverage
