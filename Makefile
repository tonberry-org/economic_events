.DEFAULT_GOAL : help

.PHONY: help
help:
	@echo "clean - cleans source tree"
	@echo "build - builds wheel file"
	@echo "package - generates zip file"
	@echo "gen - generates response models"

ZIP_FILE = pricehistory.zip
WHEEL_FILE = realpath ./dist/*.whl

.PHONY: clean
clean:
	rm -rf ./dist/

.PHONY: build
build:
	poetry build --format wheel

.PHONY: package
package: build
	pip install $(WHEEL_FILE) -t dist && \
	rm -f $(WHEEL_FILE) && \
	cd dist && zip $(ZIP_FILE) * -r -x '*.pyc'

