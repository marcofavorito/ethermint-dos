

class ABCIExampleApp(object):
    def __init__(self,
                 id,
                 abci_addr,
                 verbose = False,
                 save_logs = False,
                 ):
        self.id = id
        self.abci_addr = abci_addr
        self.verbose = verbose
        self.save_logs = save_logs

    def get_init_command(self):
        return ""

    def get_app_command(self):
        return "abci-cli dummy %s" %self.get_address_flags()

    def get_address_flags(self):
        return "--addr {abci_addr}".format(**self.__dict__)
