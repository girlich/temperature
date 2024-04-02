# Installation
## Prepare the SD card
### Use a Linux PC
You need a Linux PC with a SD card slot, where you can write the SD card for the Raspberry Pi.
### Clone this repository into a new directroy and enter
```
git clone git@github.com:girlich/temperature.git
cd temperature
```
### Create the virtual environment for Python
```
make venv
```
### Install all Ansible dependencies into the virtual environment
```
make deps-ansibe
```
### Enter the virtual environment
```
make activate
```
### Create the SD card
```
make sd
```
When the image is downloaded and patched, Ansible will stop and give you the chance to reviuew, if the device to overwrite is the right one.

## Basic setup over the network
### Transfer SD card
Remove the SD card from the PC and put it into the Raspberry Pi. Power it up. It should start and reboot twice. Then the system should be ready to be reached over the network.
### Configure the base system
make dev
make copy
### Login via SSH
```
ssh -i ssh-keys/ssh_key_temperature pi@temperature
```
### 
## Final setup on the system
### Install the actual stuff locally
```
cd temperature ; make activate
make local
```
## Use the graphical console
The system is now setup. You should see on the console a browser with 3 tabs: Grafana with the dashboard, Prometheus to see he raw data and in the final tab the actual temperature exporter.
