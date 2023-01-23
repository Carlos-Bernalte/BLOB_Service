all: clean run-server

run-server:
	python -m server.server

run-client:
	python -m client.client
	
test:
	tox

clean:
	@echo "Cleaning up..."
	@rm -rf .tox
	@rm -rf *storage
	@rm -rf client/downloads
	@rm -f *.db *.xml .coverage
