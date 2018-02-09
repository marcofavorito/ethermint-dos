from app.constants import *

class EthermintApp(object):


    def __init__(self,
                 id,
                 abci_addr="tcp://0.0.0.0:46658",
                 tendermint_addr="tcp://0.0.0.0:46657",
                 rpc_port=8545,
                 ws_port=8546,
                 rpcapi="eth,net,web3,personal,admin",
                 verbosity=False,
                 save_logs=False,
                 path=ETHERMINT_PATH,
                 datadir=ETHERMINT_FOLDER + str(id),
                 genesis_file_path=""
                 ):

        self.id = id
        self.abci_addr = abci_addr
        self.tendermint_addr = tendermint_addr
        self.rpc_port = rpc_port
        self.ws_port = ws_port
        self.rpcapi = rpcapi
        self.verbosity = 6 if verbosity==2 else 6 if verbosity==1 else 3
        self.datadir=datadir
        self.save_logs=save_logs
        self.path=path
        self.genesis_file_path=genesis_file_path


    def get_init_command(self):
        return self.path + " --datadir {datadir} unsafe_reset_all && ethermint --datadir {datadir} init {genesis_file_path}".format(**self.__dict__)

    def get_app_command(self):
        return self.path + " --datadir %s %s %s %s %s" % \
               (self.datadir, "", self.get_flags(), self.get_address_flags(), "2>&1 | tee %s/log-ethermint-node%s.log" % (LOGS_FOLDER, self.id) if self.save_logs else "")

    def get_flags(self):
        return "--verbosity %s" % self.verbosity

    def get_address_flags(self):
        return ETHERMINT_FLAGS + " --rpcapi {rpcapi} --abci_laddr {abci_addr} --tendermint_addr {tendermint_addr} --rpcport {rpc_port} --wsport {ws_port}".format(**self.__dict__)