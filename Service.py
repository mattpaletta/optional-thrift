class RPC:
	def __init__(self, use_rpc=False, server=False):
		pass

class Service:

	def __init__(self, thrift_class):
		self._thrift_class = thrift_class
		self._transport = None
		
	def __call__(self, original_clazz):
		print("Wrapped " + str(original_clazz.__name__))
		
		decorator_self = self
		
		def wrappee(*args, **kwargs):
			print('in decorator before wrapee with flag ', decorator_self._thrift_class.__name__)

			if "use_rpc" in kwargs.keys() and "server" in kwargs.keys() \
					and kwargs["use_rpc"] and kwargs["server"]:
				
				from thrift.protocol import TBinaryProtocol
				from thrift.transport import TSocket
				from thrift.transport import TTransport
				from thrift.server import TServer
	
				handler = original_clazz(*args, **kwargs)
				processor = decorator_self._thrift_class.Processor(handler)
				transport = TSocket.TServerSocket(port=9090)
				tfactory = TTransport.TBufferedTransportFactory()
				pfactory = TBinaryProtocol.TBinaryProtocolFactory()
				
				self.__inst = handler
				
				server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)
				print("Serving!")
				server.serve()
				print('done.')
				
			elif "use_rpc" in kwargs.keys() and "server" in kwargs.keys() \
					and kwargs["use_rpc"] and not kwargs["server"]:
				
				from thrift.protocol import TBinaryProtocol
				from thrift.transport import TSocket
				from thrift.transport import TTransport
				from thrift.server import TServer
				
				# Make socket
				self._transport = TSocket.TSocket(host='localhost', port=9090)
				# Buffering is critical. Raw sockets are very slow
				self._transport = TTransport.TBufferedTransport(self._transport)
				# Connect!
				self._transport.open()
				# Wrap in a protocol
				protocol = TBinaryProtocol.TBinaryProtocol(self._transport)
				# Create a client to use the protocol encoder
				client = decorator_self._thrift_class.Client(protocol)
				print("Client connected to server: " + str(self._transport.isOpen()))
				
				self.__inst = client
				return self.__inst
				
			else:
				return original_clazz(*args, **kwargs)
		
		print('in decorator after wrapee with flag ', decorator_self._thrift_class.__name__)
		return wrappee
		
	def __del__(self):
		if self._transport is not None:
			self._transport.close()
