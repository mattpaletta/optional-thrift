# optional-thrift

### Installation
```
pip install optionalthrift
```

This is an wrapper for Thrift that will allow you to
switch between running functions as RPC calls and running
them as normal python objects.<br>
<br>

## To wrap a new class
1. The class must be a subclass of `RPC`
2. Wrap the function, passing in the generated thrift class.<br>
```
import sys
sys.path.append("gen-py")

from tutorial import Calculator

@Service(thrift_class=Calculator, port=1111)
class CalculatorHandler(object):
	def __init__(self, use_rpc=False, server=False):
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
print('1+1=' + str(sum_))
```

### In the server:
```
CalculatorHandler(use_rpc=True, server=True)
```

### How you could use this
Your client should be your main implementation.  If you set **use_rpc=False**
(could be from a command line argument), you will get back a singleton for CalculatorHandler
object, where methods will be called within the same python process.<br>
<br>
This wrapper allows you to alternatively set **use_rpc=True** at runtime, which will
instead try to connect to a server (for example as `Calculator:1111`) and use Thrift
to execute all the equivalent functions. (these must also be specified in **.thrift** files.
<br>
### Motivation
I wanted to be able to test code that uses RPC on my local machine, and use the IDE debugger, without
having to manage a bunch of running python instances for the server/client RPC call.
This will allow me to test my code as one giant application bundle, but deploy using
docker or another tool (see example), and start the server and client code separately, while retaining
the same functionality.

I also wanted to be able to change between running as a cluster and running locally with simple runtime arguments.

### Advanced Usage
By default, optionalthrift will use a **SIMPLE** thrift server.  The other server types available include
SIMPLE, FORK, POOL, and THREADED.  For example, to create a pool server with a pool size of 10 you could use the following:
```

from optionalthrift.Service import Service, ServerTypes

@Service(thrift_class=Calculator, port=1111, server_type=ServerType.POOL, pool_size=10)
class CalculatorHandler(object):
    def __init__(self, use_rpc=False, server=False):
            ...
```

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