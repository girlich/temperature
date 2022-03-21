V=./venv

all:

venv: $(V)/touchfile

$(V)/touchfile: requirements.txt
	test -d $(V) || python3 -m venv $(V)
	$(V)/bin/python3 -m pip install --upgrade pip
	. $(V)/bin/activate ; pip install -Ur requirements.txt
	touch $@

# The following line retains PS1 even inside "make activate".
.SHELLFLAGS=-ilc

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

