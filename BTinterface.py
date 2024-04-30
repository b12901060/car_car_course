import logging
from typing import Optional

from BT import Bluetooth
from score import ScoreboardServer, ScoreboardFake
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
    def read(self,actlist,scoreboard:ScoreboardServer):
        i = 0   
        length = len(actlist)
        while True:
            btstr = self.bt.serial_read_string()
            if btstr =="":
                pass
            if btstr == "node" and i<length:
                self.send_action(actlist[i])
                print(f"{actlist[i]}\n")
                i = i + 1
            if btstr == "node" and i>=length:
                self.bt.disconnect()
                
            elif btstr== "card":
                uid = self.bt.serial_read_byte()
                scoreboard.add_UID(uid[2:10])
                #remain = uid[10:]
                #if remain == "node" and i<length:
                    #self.send_action(actlist[i])
                    #i = i + 1
                    
                #else:
                    #print(f"{btstr}\n")
                    
            else:
                print(f"{btstr}\n")  
                


    def end_process(self):
        self.bt.serial_write_string("e")
        self.bt.disconnect()



