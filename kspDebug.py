import colorama as cr
import inspect
import time

INFO = "{cr.Fore.WHITE}[INFO]".format(cr=cr)
WARN = "{cr.Fore.YELLOW}[WARN]".format(cr=cr)
ERROR = "{cr.Back.RED}[ERROR]".format(cr=cr)
class kspDebug:
    def __init__(self, moduleName):
        self.moduleName = moduleName
        cr.init(autoreset=True)
    def getTime(self):
        return time.strftime("%H:%M:%S", time.gmtime())
    def getCallingFunction(self):
        return inspect.stack()[2][3]
    def out(self, content, level=INFO):
        print("[{time}] {cr.Fore.RED}({self.moduleName}) {cr.Style.DIM}{callingFunction}() {level}: {content}".format(
            self=self,
            time=self.getTime(),
            content=content,
            cr=cr,
            callingFunction=self.getCallingFunction(),
            level=level
        ))