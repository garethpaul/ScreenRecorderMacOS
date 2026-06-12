ROOT := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))

PYTHON ?= python3
XCODEBUILD ?= xcodebuild

.PHONY: build check lint test verify

lint:
	$(PYTHON) "$(ROOT)/scripts/check-capture-source.py" --mode project

test:
	$(PYTHON) "$(ROOT)/scripts/check-capture-source.py" --mode behavior

build: lint
	@if command -v "$(XCODEBUILD)" >/dev/null 2>&1; then \
		cd "$(ROOT)" && "$(XCODEBUILD)" -project ScreenRecorder.xcodeproj -scheme CaptureSample -destination 'platform=macOS' CODE_SIGNING_ALLOWED=NO build; \
	else \
		echo "xcodebuild not found; static project checks completed"; \
	fi

verify: lint test build

check: verify
