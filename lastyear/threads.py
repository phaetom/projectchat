from threading import Thread, Lock
from time import sleep

# Teeme Thread alamklassi:
class Messenger(Thread):
    
    def __init__(self, message, lock):
        Thread.__init__(self, target = self.sendMessages)
        # Muutuja, mis määrab, et kas töö on veel
        # käimas või mitte:
        self.running = True
        self.message = message
        self.lock = lock
        
    def start(self):
        Thread.start(self)
    
    def stop(self):
        # Kui tahame töö lõpetada, määrame selle
        # muutja False'iks:
        self.running = False
    
    def sendMessages(self):
        # Tsükkel käib, kuni oleme ta muutuja kaudu välja lülitanud:
        while self.running:
            sleep(1)
            self.lock.acquire()
            if self.running:
                print(self.message)
            self.lock.release()
            
# Kasutan lukku, et saaks korraga vaid ühte asja printida ja tekstid
# ei ilmuks üksteise kukile. Saaks pmst ka ilma.    
printLock = Lock()

# Teen hunniku Threade ja seon nad mingi kindla nimega, mille kaudu
# saaks nad hiljem kinni panna:
messengers = {}
messengers["Anu Ansson"] = Messenger("A", printLock)
messengers["Bert Bortson"] = Messenger("B", printLock)
messengers["Carl Carlsson"] = Messenger("C", printLock)
# Threadid tööle:
for messenger in messengers.values():
    messenger.start()
    
# Funktsioon, mis hakkab "kasutajaid" järjest disconnectima,
# e siin näites threade kinni panema:    
def killer(messengers):
    for messenger_name in messengers:
        sleep(3)
        # Nime järgi saame nüüd õige Threade välja
        # valida, mida kinni panna:
        print("Stopping", messenger_name)
        messengers[messenger_name].stop()
# Paneme selle funktsiooni eraldi threadile käima nt:
killerThreader = Thread(target=killer, args=(messengers,))
killerThreader.start()
killerThreader.join()