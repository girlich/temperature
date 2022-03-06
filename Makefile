V=./venv

all:

venv: $(V)/touchfile

$(V)/touchfile: requirements.txt
	test -d $(V) || python3 -m venv $(V) -p python3.8
	$(MAKE) update_pip
	. $(V)/bin/activate ; pip install -Ur requirements.txt
	touch $@

update_pip:
	$(V)/bin/python3 -m pip install --upgrade pip

activate: $(V)
	echo "source $(V)/bin/activate"

deps-ansible:
	ansible-galaxy collection install -r ansible/requirements.yml

local:
	cd ansible ; ansible-playbook --ask-become-pass localhost.yml --extra-vars "@../../localhost.yml"

remote:
	cd ansible ; ansible-playbook temperature.yml --extra-vars "@../../temperature.yml"

