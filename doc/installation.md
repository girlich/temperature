# Installation
## Prepare the µSD card
### Use a Linux PC
You need a Linux PC with a µSD card slot, where you can write the µSD card for the Raspberry Pi.
### Get the source repo
Clone the source code repository into a new directory and change into it:
```
$ git clone git@github.com:girlich/temperature.git
$ cd temperature
```
### Configuration options
It not wise to write any credentials or similar configuration options into a Git repository. So we have a file `private.yml` outside of git. You should copy the sample file as a starting point.
```
$ cp doc/private.yml ..
```
Now you can edit these entries as you like them.
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
### Enter the virtual environment
Now that the virtual environment is prepared, you can activate it.
```
$ make activate
```
### Create the µSD card
```
$ make sd
```
This will first ask for the password of `root` on the PC because later the image will be mounted, changed, unmounted and written to the µSD card. For all these steps `root` rights are necessary.

Ansible will call `rpi-imager` to get a list of current images for the Raspberry Pi. From the list the default desktop image is selected and will be downloaded. It is then uncompressed and the checksum of the uncompressed image is verified. 

A new pair of SSH keys is generated. They will be used later to login into the sensor machine. You can upload the public SSH key as your SSH key for GitHub.

Before the µSD card is overwritten, Ansible will print some information about the device, stop and give you the chance to cancel the whole process. Just press Enter to continue. This overwrites the µSD card.

After overwriting the µSD card with the new image `sync` is used to flush all buffers. So you can remove the card immediately.

## Basic setup over the network
### Transfer SD card
Remove the SD card from the PC and put it into the Raspberry Pi. Power it up. It should start and reboot twice automatically. Then the system should be ready to be reached over the network by SSH, which is necessary for Ansible to configure the system over the network.
### Login via SSH
You should logion via SSH just to make sure it works and then log out again.
```
$ ssh -i ssh-keys/ssh_key_tempsens pi@tempsens
$ exit
```
Beside basic customiziations (WiFi, SSH, user credentials) nothing is installed yet but you need to have the SSH host key locally stored in `~/.ssh/known_hosts` allow Ansible to continue.
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
$ ssh -i ssh-keys/ssh_key_tempsens pi@tempsens
$ cd temperature/git ; make activate
$ make local
```
This is finally the step to install the sensor Python script, Prometheus, Grafana and connect of it together. It even prepares a full screen Chromium browser with the important tabs already open.
## Use the graphical console
The system is now set up properly. You should see on the console a browser with 3 tabs: Grafana with the dashboard, Prometheus to see the raw data and in the final tab the actual temperature exporter.
