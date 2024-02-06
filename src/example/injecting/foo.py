from infoinject import InfoInjector

def _add(a, b):
	return (a+10) + b

@InfoInjector.inject_debug_info([
	{
		"line": 1,
		"code": [
		"print(f'a = {a}')",
		]
	}
], globals(), locals())
def add(a, b):
	return _add(a,b)

# Testing different indentation levels.
@InfoInjector.inject_debug_info([
	{
		"line": 1,
		"code": [
		"print(f'n = {n}')",
		]
	},
	{
		"line": 2,
		"code": [
		"print(f'n <= 1')",
		]
	},
	{
		"line": 4,
		"code": [
		"if n % 2 == 0:",
		"\tprint('n is even')",
		]
	}
], globals(), locals())
def fib(n):
	if n <= 1:
		return n
	else:
		return fib(n-1) + fib(n-2)




# TODO: make things easier.
@InfoInjector.add_instruction({
	"line": 1,
	"code": [
		"print(f'n = {n}')",
	]
})
@InfoInjector.add_instruction({
	"line": 2,
	"code": [
		"print(f'n <= 1')",
	]
})
@InfoInjector.add_instruction({
	"line": 4,
	"code": [
		"if n % 2 == 0:",
		"\tprint('n is even')",
	]
})
@InfoInjector.inject(globals(), locals())
def better_fib(n):
	if n <= 1:
		return n
	else:
		return fib(n-1) + fib(n-2)	


print(fib(10))
