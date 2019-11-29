
# !/bin/bash



Controller_set (){

	sudo cp -a 046d:c261 /etc/usb_modeswitch.d/
	sudo usb_modeswitch -c /etc/usb_modeswitch.d/046d:c261
}



if [ "controller_set" == "$1" ]; then
	Controller_set
fi


