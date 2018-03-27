# optional-thrift

This is an wrapper for Thrift that will allow you to
switch between running functions as RPC calls and running
them as normal python objects.<br>
<br>

## To wrap a new class
1. The class must be a subclass of `RPC`
2. Wrap the function, passing in the generated thrift class.<br>
```
from tutorial import Calculator

@Service(thrift_class=Calculator)
class CalculatorHandler(RPC):
	def __init__(self, use_rpc, server):
		super().__init__(use_rpc, server)
		self.log = {}
		print("Starting server!")
```

## Using the wrapped class:
### In the client:
```
client = CalculatorHandler(use_rpc=True, server=False)

client.ping()
print('ping()')

sum_ = client.add(1, 1)
print('1+1=%d' % sum_)
```

### In the server:
```
CalculatorHandler(use_rpc=True, server=True)
```

### How you could use this
Your client should be your main implementation.  If you set **use_rpc=False**
(could be from a command line argument), you will get back a normal CalculatorHandler
object, like any other python object, and you can call methods as normal.<br>
<br>
This wrapper allows you to alternatively set **use_rpc=True**, which will
instead try to connect to a server (specified as `localhost:9090`) and use Thrift
to execute all the equivalent functions.
<br>
### Motivation
I wanted to be able to test code that uses RPC on my local machine without
having to manage a bunch of running python instances for the server/client RPC call.
This will allow me to test my code as one giant application bundle, but deploy using
docker or another tool, and start the server and client code separately, and retain
the same functionality.

### Questions, Comments, Concerns, Queries, Qwibbles?

If you have any questions, comments, or concerns please leave them in the GitHub
Issues tracker:

https://github.com/mattpaletta/optional-thrift/issues

### Bug reports

If you discover any bugs, feel free to create an issue on GitHub. Please add as much information as
possible to help us fixing the possible bug. We also encourage you to help even more by forking and
sending us a pull request.

https://github.com/mattpaletta/optional-thrift/issues

## Maintainers

* Matthew Paletta (https://github.com/mattpaletta)

## License

MIT License. Copyright 2018 Matthew Paletta. http://mrated.ca