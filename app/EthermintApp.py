from app.constants import *

class EthermintApp(object):


    def __init__(self,
                 id,
                 abci_addr,
                 tendermint_addr,
                 rpc_port,
                 ws_port,
                 rpcapi="eth,net,web3,personal,admin",
                 verbose=False,
                 save_logs=False
                 ):

        self.id = id
        self.abci_addr = abci_addr
        self.tendermint_addr = tendermint_addr
        self.rpc_port = rpc_port
        self.ws_port = ws_port
        self.rpcapi = rpcapi
        self.verbosity = 6 if verbose else 3
        self.datadir=ETHERMINT_FOLDER + str(id)
        self.save_logs=save_logs


    def get_init_command(self):
        return "ethermint --datadir {datadir} unsafe_reset_all && ethermint --datadir {datadir} init".format(**self.__dict__)

    def get_app_command(self):
        return "ethermint --datadir %s %s %s %s" % \
               (self.datadir, self.get_flags(), self.get_address_flags(), "2>&1 | tee %s/log-ethermint-node%s.log" % (LOGS_FOLDER, self.id) if self.save_logs else "")

    def get_flags(self):
        return "--verbosity %s" % self.verbosity

    def get_address_flags(self):
        return ETHERMINT_FLAGS + " --rpcapi {rpcapi} --abci_laddr {abci_addr} --tendermint_addr {tendermint_addr} --rpcport {rpc_port} --wsport {ws_port}".format(**self.__dict__)