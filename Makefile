V=./venv

all:
	@echo useful targets:
	@echo "venv      prepare virtual Python environment"
	@echo "activate  jump into the virtual Python environment interactively"
	@echo "sd        create an SD card locally"
	@echo "remote    configure the remote server"
	@echo "copy      copy stuff to the remopte server to continue working from there"
	@echo "update    get the most current version"

venv: $(V)/touchfile

$(V)/touchfile: requirements.txt
	test -d $(V) || python3 -m venv $(V)
	$(V)/bin/python3 -m pip install --upgrade pip
	. $(V)/bin/activate ; pip install -Ur requirements.txt
	touch $@

# The following line retains PS1 even inside "make activate".
.SHELLFLAGS=-ilc
# "source" needs a bash as shell
SHELL=/bin/bash

activate: $(V)
	source $(V)/bin/activate;bash -il

deps-ansible:
	ansible-galaxy collection install -r ansible/requirements.yml

sd:
	cd ansible ; ansible-playbook --ask-become-pass sd.yml --extra-vars "@../../private.yml"

remote:
	cd ansible ; ansible-playbook remote.yml --extra-vars "@../../private.yml"

copy:
	cd ansible ; ansible-playbook copy.yml --extra-vars "@../../private.yml"

update:
	git pull

