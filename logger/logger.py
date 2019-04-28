import logging, sys 
from logging.handlers import RotatingFileHandler
from curses.ascii import isprint

class myLogger():


    def __init__(self, name : str = 'activity.log', size : int  = 1000000, logLevel : str = "debug"):
        """
            Init function of myLogger class
            By default the logfile is called 'activity.log'
            To change it easily you could the following lines in your main script 
                'from logger import myLogger, sys'
                'sys.stdout = myLogger(__file__.split(".")[0]+".log")'
            :param name: (str) name of the logfile
            :param size: (int) size of the logfile
            :param logLevel: (str) level of the message write in the logfile
        """
        self.name = name
        self.terminal = sys.stdout
        self.logger = logging.getLogger()
        self.formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
        self.file_handler = RotatingFileHandler(name, 'a', size, 1)
        self.setlogLevel(logLevel)
        self.file_handler.setFormatter(self.formatter)
        self.logger.addHandler(self.file_handler)

    def write(self, message, msgLevel : str = "info"):
        """
            Get a message in input then duplicate it to write in the terminal and the logfile.
            :param message: message to write
            :param msgLevel: (str) level of the message, could be debug, info, warning, error, critical sorted by importance
        """
        self.terminal.write(message)
        if message.find("Error") != -1:
            self.logger.error(message)
        if message.find("KeyboardInterrupt") != -1:
            self.logger.warning(message)

        print_msg = ''.join(char for char in message if isprint(char))
        if len(print_msg) > 0 :
            if msgLevel == "info":
                self.logger.info(print_msg)  
            elif msgLevel == "debug":
                self.logger.debug(print_msg)  
            elif msgLevel == "warning":
                self.logger.warning(print_msg)  
            elif msgLevel == "critical":
                self.logger.critical(print_msg)  
            elif msgLevel == "error":
                self.logger.error(print_msg)  

    def setlogLevel(self, logLevel):
        self.logLevel = logLevel
        if self.logLevel == "debug":
            self.logger.setLevel(logging.DEBUG)
            self.file_handler.setLevel(logging.DEBUG)
        elif self.logLevel == "info":
            self.logger.setLevel(logging.INFO)
            self.file_handler.setLevel(logging.INFO)
        elif self.logLevel == "warning":
            self.logger.setLevel(logging.WARNING) 
            self.file_handler.setLevel(logging.WARNING) 
        elif self.logLevel == "error":
            self.logger.setLevel(logging.ERROR)
            self.file_handler.setLevel(logging.ERROR)
        elif self.logLevel == "critical":
            self.logger.setLevel(logging.CRITICAL)
            self.file_handler.setLevel(logging.CRITICAL)
                
    def flush(self):
        """
        """
        pass


def printer(*args, sep:str=" ", end:str=""):
    """
        TODO need to be compliant with the original print function /!\\
    """
    res = ""
    for e in args:
        if e != args[len(args)-1]:
            res += str(e) + sep
        else:
            res += str(e)
    print(res+end)

