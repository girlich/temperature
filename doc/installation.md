# Installation
## Overview
Installation happens in 3 steps:
1. Preparation of a µSD card on a Linux PC
2. Boot from this card and some installation over the network
3. Final installation steps on the Raspberry Pi itself.

The goal is to put as few as possible things in the earlier stages. It somethung can be installed in step 3, it is. Because we have this source code repository available in step 3, we can change many configurations on the target machine and let step 3 re-run. That's why we use [Ansible](https://www.ansible.com/) for the system administration: only the changed configuration will be applied to the system. All the rest remains stable ([idempotency](https://docs.ansible.com/ansible/latest/reference_appendices/glossary.html#term-Idempotency)).
## Prepare the µSD card
### Use a Linux PC
You need a Linux PC with a µSD card slot, where you can write the µSD card for the Raspberry Pi.
Some non-standard software needs to be installed before we can start:
* `rpi-imager`: it knows, where to get images from. We'll not use it for actually writing the µSD card.
* `sfdisk`: it can parse an image file to find the boot partition
* `xz`: it can uncompress the compressed image
### Get the source repo
Clone the Git source code repository from GitHub into a new directory and change into it:
```
$ git clone git@github.com:girlich/temperature.git
$ cd temperature
```
### Configuration options
It is not wise to write any credentials or similar configuration options into a Git repository. So we have a file `private.yml` outside of git. You should copy the sample file as a starting point.
```
$ cp doc/private.yml ..
```
Now you can edit these entries with your favorite text editor.
### Virtual Environment
To not disturb your local Python installation all the rest happens inside a virtual Python environment. You have to create it first:
```
$ make venv
```
This will create a new virtual environment and install some necessary Python dependencies like Ansible and associated tools into it.
### Ansible Dependencies
It might be, that some dependencies for Ansible are still missing. You can install them with
```
$ make deps-ansible
```
This is an extra target to allow you later to add more Ansible dependencies on the way without replacing the while virtual environment.
### Enter the virtual environment
Now that the virtual environment is prepared, you can activate it.
```
$ make activate
```
This will put you into a new shell, where some environment variables are changed. Just try
```
type python
```
to find, that `python` is no longer `/usr/bin/python` but the special `python` below the virtual environment directory `venv`.
### Create the µSD card
```
$ make sd
```
This will first ask for the password of `root` on the PC because later the image will be mounted, changed, unmounted and written to the µSD card. For all these steps `root` rights are necessary.

Ansible will call `rpi-imager` to get a list of current images for the Raspberry Pi. From the list the default desktop image is selected and will be downloaded. It is then uncompressed and the checksum of the uncompressed image is verified. 

A new pair of SSH keys is generated. They will be used later to login into the sensor machine. You can upload the public SSH key as your SSH key for GitHub.

Before the µSD card is overwritten (with `dd`), Ansible will print some information about the device, stop, and give you the chance to cancel the whole process. Just press Enter to continue. This overwrites the µSD card.

After overwriting the µSD card with the new image `sync` is used to flush all buffers. This means you can remove the card immediately, when the prompt reappears.

## Basic setup over the network
### Transfer µSD card
Remove the µSD card from the PC and put it into the Raspberry Pi. Power it up. It should start and reboot twice automatically. Then the system should be ready to be reached over the network by SSH, which is necessary for Ansible to configure the system over the network.
### Login via SSH
You should login via SSH just to make sure it works and then log out immediately. The options `ansible_host`, `ansible_user`, and `ansible_private_key_file` in `../private.yml` are used for this and must be set to useful values for your network.
```
$ make ssh
$ exit
```
Beside basic customiziations (WiFi, SSH, user credentials) nothing is installed yet but you need to have the SSH host key locally stored in `~/.ssh/known_hosts` to allow Ansible to continue.
### Configure the base system
Back on the PC you let Ansible copy over some stuff needed from the PC (like private SSH key, `private.yml`, the Git repository) to the target system. The code itself is then there.
```
$ make copy
```
Now install more tools.
```
$ make dev
```
This will install many development tools and prepare the Git repository by already creating the virtual Python environment. So now you can really continue working there on the Raspberry Pi.
## Final setup on the system
### Install the actual stuff locally
```
$ make ssh
$ cd temperature/git ; make activate
$ make local
```
This is finally the step to install the sensor Python script, Prometheus, Grafana and connect all of it together. It even prepares a full screen Chromium browser with the important tabs already open. As the last step the system will reboot again (and log you out of the SSH session in the process).

### Update of the Operating System
When the system comes up again, it is recommended to perform an update of the installed packages from the operating system.
```
$ make ssh
$ cd temperature/git
$ make update-os
```