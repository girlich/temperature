mkfile_path := $(abspath $(lastword $(MAKEFILE_LIST)))
mkfile_dir := $(dir $(mkfile_path))

V=$(mkfile_dir)venv

all:
	@echo running in $(mkfile_dir)
	@echo venv is $(V)
	@echo useful targets:
	@echo "venv        prepare virtual Python environment"
	@echo "activate    jump into the virtual Python environment interactively"
	@echo "sd          create an SD card locally"
	@echo "copy        copy stuff to the remote server to continue working from there"
	@echo "dev         prepare a development environment of the server"
	@echo "local       configure the local server"
	@echo "update-git  get the most current version"
	@echo "update-os   update the operating system and packages in it"

venv: $(V)/touchfile

# If you need a newer Python, change this here.
PYTHON=python3.11

$(V)/touchfile: requirements.txt
	test -d $(V) || $(PYTHON) -m venv $(V)
	$(V)/bin/python3 -m pip install --upgrade pip
	. $(V)/bin/activate ; pip install -Ur requirements.txt
	touch $@

activate: $(V)
	. $(V)/bin/activate && exec bash

deps-ansible: ansible/requirements.yml
	$(V)/bin/ansible-galaxy collection install -r ansible/requirements.yml
	touch $(V)/galaxy

# Locally on a PC: prepare and write the SD card
sd:
	cd ansible ; ansible-playbook --ask-become-pass sd.yml --extra-vars "@../../private.yml"

# After booting the SD card, copy stuff over.
copy:
	cd ansible ; ansible-playbook copy.yml --extra-vars "@../../private.yml"

# Make sure development works there.
dev:
	cd ansible ; ansible-playbook dev.yml --extra-vars "@../../private.yml"

# Locally on the Raspberry, prepare all the rest.
local:
	cd ansible ; ansible-playbook local.yml --extra-vars "@../../private.yml"

update-git:
	git pull

update-os:
	sudo apt update
	sudo apt upgrade -y
	sudo apt autoremove

