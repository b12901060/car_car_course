import logging
from typing import Optional

from BT import Bluetooth

log = logging.getLogger(__name__)

# hint: You may design additional functions to execute the input command,
# which will be helpful when debugging :)


class BTInterface:
    def __init__(self, port: Optional[str] = None):
        log.info("Arduino Bluetooth Connect Program.")
        self.bt = Bluetooth()
        if port is None:
            port = input("PC bluetooth port name: ")
        while not self.bt.do_connect(port):
            if port == "quit":
                self.bt.disconnect()
                quit()
            port = input("PC bluetooth port name: ")

    def start(self):
        input("Press enter to start.")
        self.bt.serial_write_string("s")

    def get_UID(self):
        return self.bt.serial_read_byte()
    def send_action(self, dirc):
        self.bt.serial_write_string(dirc)
        return
    def read(self):    
        btstr = self.bt.serial_read_string()
        if btstr != "node" :
            print(f"{btstr}\n")  
        return
    def node(self,actlist):
        self.bt.node(actlist)

    def end_process(self):
        self.bt.serial_write_string("e")
        self.bt.disconnect()



