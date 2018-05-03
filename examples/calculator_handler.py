from optionalthrift.Service import Service
from shared.ttypes import SharedStruct
from tutorial import Calculator
from tutorial.ttypes import InvalidOperation, Operation
import logging

@Service(thrift_class=Calculator, port=1111)
class CalculatorHandler():
	def __init__(self, use_rpc=False, server=False):
		self.log = {}
		logging.info("Starting server!")

	def ping(self):
		logging.info('ping()')

	def add(self, n1, n2):
		logging.info('add(%d,%d)' % (n1, n2))
		return n1 + n2

	def calculate(self, logid, work):
		logging.info('calculate(%d, %r)' % (logid, work))

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
		logging.info('getStruct(%d)' % (key))
		return self.log[key]

	def zip(self):
		logging.info('zip()')
