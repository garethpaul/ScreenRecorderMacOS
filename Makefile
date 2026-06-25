.PHONY: build check lint root-test test verify

PUBLIC_TARGETS := build check lint root-test test verify

override SHELL := /bin/sh
override .SHELLFLAGS := -c
$(PUBLIC_TARGETS): override SHELL := /bin/sh
$(PUBLIC_TARGETS): override .SHELLFLAGS := -c
override PYTHONDONTWRITEBYTECODE := 1
export PYTHONDONTWRITEBYTECODE
ifneq ($(strip $(MAKEFILES)),)
$(error MAKEFILES must be empty; repository verification requires this Makefile to be loaded alone)
endif
override MAKEFILES :=
ifneq ($(origin MAKEFILE_LIST),file)
$(error MAKEFILE_LIST must not be overridden)
endif
override ROOT := $(shell path='$(subst ','"'"',$(MAKEFILE_LIST))'; path=$$(printf '%s' "$$path" | /usr/bin/sed 's/^ //'); [ -f "$$path" ] || exit 1; directory=$$(/usr/bin/dirname -- "$$path"); CDPATH= cd -- "$$directory" && /bin/pwd -P)
export ROOT
ifeq ($(strip $(ROOT)),)
$(error repository Makefile path could not be resolved)
endif
override PYTHON := $(ROOT)/scripts/run-python.sh
override XCODEBUILD := $(ROOT)/scripts/run-xcodebuild.sh
export PYTHON XCODEBUILD
override REPOSITORY_SHELL_LITERAL = $(subst ','"'"',$1)
override REPOSITORY_ROOT_LITERAL := $(call REPOSITORY_SHELL_LITERAL,$(ROOT))
override REPOSITORY_PYTHON_LITERAL := $(call REPOSITORY_SHELL_LITERAL,$(PYTHON))
override REPOSITORY_XCODEBUILD_LITERAL := $(call REPOSITORY_SHELL_LITERAL,$(XCODEBUILD))

$(PUBLIC_TARGETS)::

lint::
	'$(REPOSITORY_PYTHON_LITERAL)' '$(REPOSITORY_ROOT_LITERAL)/scripts/check-capture-source.py' --mode project

test::
	'$(REPOSITORY_PYTHON_LITERAL)' '$(REPOSITORY_ROOT_LITERAL)/scripts/check-capture-source.py' --mode behavior
	'$(REPOSITORY_PYTHON_LITERAL)' '$(REPOSITORY_ROOT_LITERAL)/scripts/test_movie_recorder_video_start_contract.py'
	'$(REPOSITORY_PYTHON_LITERAL)' '$(REPOSITORY_ROOT_LITERAL)/scripts/test_screen_recorder_start_stop_contract.py'
	'$(REPOSITORY_PYTHON_LITERAL)' '$(REPOSITORY_ROOT_LITERAL)/scripts/test_user_stopped_autostart_contract.py'
	'$(REPOSITORY_PYTHON_LITERAL)' '$(REPOSITORY_ROOT_LITERAL)/scripts/test_menu_recorder_state_contract.py'
	'$(REPOSITORY_PYTHON_LITERAL)' '$(REPOSITORY_ROOT_LITERAL)/scripts/test_stream_delegate_failure_contract.py'
	'$(REPOSITORY_PYTHON_LITERAL)' '$(REPOSITORY_ROOT_LITERAL)/scripts/test_capture_source_reconciliation_contract.py'

build:: lint
	@if [ -x /usr/bin/xcodebuild ]; then \
		cd '$(REPOSITORY_ROOT_LITERAL)' && '$(REPOSITORY_XCODEBUILD_LITERAL)' -project ScreenRecorder.xcodeproj -scheme CaptureSample -destination 'platform=macOS' CODE_SIGNING_ALLOWED=NO build; \
	else \
		echo "xcodebuild not found; static project checks completed"; \
	fi

root-test::
	/bin/sh '$(REPOSITORY_ROOT_LITERAL)/scripts/test-makefile-root.sh'

verify:: root-test lint test build

check:: verify
