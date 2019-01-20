import logging
from multiprocessing import cpu_count
from time import sleep

from pynotstdlib.singleton import Singleton


class ServerTypes(object):
    THREADED = "THREADED"
    FORK = "FORK"
    SIMPLE = "SIMPLE"
    POOL = "POOL"


class Service(object):
    """
    Wrapper for Thrift Classes to allow for easy switching between using RPC calls
    (when running in a cluster) and using Singletons (when running locally).  The client
    can connect to the server at the name of the thrift_class.
    """

    def __init__(self,
                 thrift_class,
                 port,
                 server_type=ServerTypes.SIMPLE,
                 pool_size=(cpu_count() - 1),
                 num_retries=-1):
        """
        :param class thrift_class: Generated thrift class we are wrapping.
        :param int port: Server port to listen on.
        :param ServerType server_type: Which Thrift server type. Must be one of `optionalthrift.ServerTypes`. Default SIMPLE.
        :param int pool_size: Only required if using a Pool Server, specifies the pool size.
        :param int num_retries: Number of times to retry connecting to a service before exiting, -1 for unlimited.
        """

        server_types = [ServerTypes.THREADED, ServerTypes.FORK,
                        ServerTypes.SIMPLE, ServerTypes.POOL]

        str_types = ", ".join(server_types)
        assert server_type in server_types, str("server_type must be one of :" + str_types)
        assert pool_size > 0, "Pool size must be greater than 0. Default `cpu_count()-1`"

        self._thrift_class = thrift_class
        self._port = port
        self._transport = None
        self._server_type = server_type
        self._pool_size = pool_size
        self._num_retries = num_retries

    def __call__(self, original_clazz):
        logging.debug("Wrapped " + str(original_clazz.__name__))

        decorator_self = self

        if decorator_self._thrift_class is not None:
            dec_name = str(decorator_self._thrift_class.__name__).split(".")[-1]
        else:
            dec_name = original_clazz.__name__

        def wrappee(*args, **kwargs):
            logging.debug('in decorator before wrapee with flag ' + dec_name)
            if "use_rpc" not in kwargs:
                use_rpc = False
                logging.warning("Defaulting to not use RPC for: " + dec_name)
            else:
                use_rpc = kwargs["use_rpc"]

            if "server" not in kwargs:
                use_server = False
                logging.warning("Defaulting to not start as server for: " + dec_name)
            else:
                use_server = kwargs["server"]

            if use_rpc and use_server:
                from thrift.protocol import TBinaryProtocol
                from thrift.transport import TSocket
                from thrift.transport import TTransport
                from thrift.server import TServer

                handler = original_clazz(*args, **kwargs)
                processor = decorator_self._thrift_class.Processor(handler)
                transport = TSocket.TServerSocket(port=decorator_self._port)
                tfactory = TTransport.TBufferedTransportFactory()
                pfactory = TBinaryProtocol.TBinaryProtocolFactory()

                self.__inst = handler

                if decorator_self._server_type == "THREADED":
                    server = TServer.TThreadedServer(processor, transport, tfactory, pfactory)

                elif decorator_self._server_type == "SIMPLE":
                    server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)

                elif decorator_self._server_type == "FORK":
                    server = TServer.TForkingServer(processor, transport, tfactory, pfactory)

                elif decorator_self._server_type == "POOL":
                    server = TServer.TThreadPoolServer(processor, transport, tfactory, pfactory)
                    server.setNumThreads(decorator_self._pool_size)
                else:
                    server = None

                logging.debug(decorator_self._server_type + " server serving: " + dec_name)
                server.serve()
                logging.debug('Done: ' + dec_name)

            elif use_rpc and not use_server:

                from thrift.protocol import TBinaryProtocol
                from thrift.transport import TSocket
                from thrift.transport import TTransport
                from thrift.server import TServer

                # Make socket
                decorator_self._transport = TSocket.TSocket(host=dec_name, port=decorator_self._port)
                # Buffering is critical. Raw sockets are very slow
                num_retried = 0
                while not decorator_self._transport.isOpen():
                    num_retried += 1
                    try:
                        decorator_self._transport.open()
                        decorator_self._transport = TTransport.TBufferedTransport(self._transport)
                    except TTransport.TTransportException:
                        logging.debug("Failed to get connection, sleeping: " + dec_name)
                        sleep(10)
                        logging.debug("Failed to get connection, retrying:" + dec_name)
                        if num_retried > decorator_self._num_retries > 0:
                            raise ValueError("Maximum connection retries exceeded: ({0})".format(dec_name))

                # Wrap in a protocol
                protocol = TBinaryProtocol.TBinaryProtocol(self._transport)
                # Create a client to use the protocol encoder
                client = decorator_self._thrift_class.Client(protocol)
                logging.debug("Client (" + dec_name + ") connected to server: " + str(self._transport.isOpen()))

                return client

            else:
                logging.debug("Returning Singleton of class: " + dec_name)
                return Singleton(original_clazz).Instance(*args, **kwargs)

        logging.debug('in decorator after wrapee with flag ' + dec_name)
        return wrappee

    def __del__(self):
        if self._transport is not None:
            self._transport.close()
