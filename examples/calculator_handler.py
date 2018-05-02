from Service import Service, RPC
from shared.ttypes import SharedStruct
from tutorial import Calculator
from tutorial.ttypes import InvalidOperation, Operation


@Service(thrift_class=Calculator)
class CalculatorHandler(RPC):
	def __init__(self, use_rpc, server):
		super().__init__(use_rpc, server)
		self.log = {}
		print("Starting server!")

	def ping(self):
		print('ping()')

	def add(self, n1, n2):
		print('add(%d,%d)' % (n1, n2))
		return n1 + n2

	def calculate(self, logid, work):
		print('calculate(%d, %r)' % (logid, work))

		if work.op == Operation.ADD:
			val = work.num1 + work.num2
		elif work.op == Operation.SUBTRACT:
			val = work.num1 - work.num2
		elif work.op == Operation.MULTIPLY:
			val = work.num1 * work.num2
		elif work.op == Operation.DIVIDE:
			if work.num2 == 0:
				x = InvalidOperation()
				x.whatOp = work.op
				x.why = 'Cannot divide by 0'
				raise x
			val = work.num1 / work.num2
		else:
			x = InvalidOperation()
			x.whatOp = work.op
			x.why = 'Invalid operation'
			raise x

		log = SharedStruct()
		log.key = logid
		log.value = '%d' % (val)
		self.log[logid] = log

		return val

	def getStruct(self, key):
		print('getStruct(%d)' % (key))
		return self.log[key]

	def zip(self):
		print('zip()')