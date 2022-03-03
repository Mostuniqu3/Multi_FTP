from logger import Logger
from threading import Thread
import time
from time import process_time
from talk_to_ftp import TalkToFTP

class FileThread(Thread):
    def __init__(self, ftp_website, fileQueue, id, DEBUG = False):
        Thread.__init__(self)
        self.fileQueue = fileQueue
        self.ftp_website = ftp_website
        self.id = id
        self.DEBUG = DEBUG
        self.log = Logger.log_debug if DEBUG else Logger.log_info
        self.ftp = TalkToFTP(ftp_website)

    def run(self):
        Logger.log_debug("<{}> Running".format(self.id))
        while True :
            if self.fileQueue.qsize() > 0 :
                if(self.DEBUG) : self.start_time = process_time()
                self.ftp.connect()
                file = self.fileQueue.get()
                action = file[0]
                file = file[1:]
                fileName = ""
                if(action == "CREATE"):
                    self.transfer_file(file)
                    fileName = file[2]
                elif(action == "REPLACE"):
                    self.ftp.remove_file(file[1])
                    self.transfer_file(file)
                    fileName = file[2]
                elif(action == "REMOVE"):
                    self.ftp.remove_file(file[0])
                    fileName = file[0]
                else:
                    self.log("<{}> UNIMPLEMENTED ACTION : {}".format(self.id, action))
                    fileName = file[2]

                self.fileQueue.task_done()
                self.ftp.disconnect()
                if(self.DEBUG) : self.log("<{}> Action {} {} took {:.1f} ms".format(self.id,action, fileName, (process_time() - self.start_time) * 1000))

            else :
                time.sleep(0.1)
            
    def transfer_file(self, file):
        self.ftp.file_transfer(file[0], file[1], file[2])