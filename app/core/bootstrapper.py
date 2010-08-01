from .environment import Environment as env_
from optparse import OptionParser
import sys, os
from app.config.main import Main as Config

class Bootstrapper(object):
    '''
    classdocs
    '''
    DEFAULT_DATA_DIR = 'data'


    def __init__(self):
        '''
        Constructor
        '''
        self.detectExeBuild()
        self.detectAppDir()
        # Define path based on frozen state
        # Include paths
        sys.path.insert(0, env_.get('appDir'))
        sys.path.insert(0, os.path.join(env_.get('appDir'), 'library'))
        self.parseOptions()
        self.initAppDirs()
        self.loadConfig()


    def detectExeBuild(self):
        try:
            env_.frozen = sys.frozen
        except AttributeError:
            env_.frozen = False

    def detectAppDir(self):
        appdir = os.path.dirname(os.path.abspath(__file__))
        if env_.get('frozen'):
            #path_base = os.environ['_MEIPASS2']
            appdir = os.path.dirname(sys.executable)
        env_._appDir = appdir

    def parseOptions(self):
        data_dir = self.__class__.DEFAULT_DATA_DIR
        p = OptionParser()
        p.add_option('-d', action = "store_true",
                     dest = 'daemonize', help = "Run the server as a daemon")
        p.add_option('-q', '--quiet', action = "store_true",
                     dest = 'quiet', help = "Don't log to console")
        p.add_option('-p', '--pidfile',
                     dest = 'pidfile', default = None,
                     help = "Store the process id in the given file")
        p.add_option('-t', '--debug', action = "store_true",
                     dest = 'debug', help = "Run in debug mode")

        options, args = p.parse_args()

        if args.__len__() == 1:
            data_dir = args[0]
        elif args.__len__() > 1:
            print ('Invalid argument cound: [data directory]')
            sys.exit(1)
        #register path settings to env
        env_.setDataDir(data_dir) #creates if not exists

        env_._args = args
        env_._options = options

    def loadConfig(self):
        env_.cfg = Config()

    def initAppDirs(self):
        dirs = ('config', 'logs', 'cache')
        for dir in dirs:
            dir = os.path.join(env_.get('dataDir'), dir)
            if not os.path.isdir(dir):
                os.mkdir(dir)





