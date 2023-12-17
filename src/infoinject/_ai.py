import openai

import inspect
import json



ENV = None
OPENAI_CLIENT = None

def ensure_ai_is_initialized():
	global ENV, OPENAI_CLIENT

	if ENV is not None and OPENAI_CLIENT is not None:
		return

	with open(".env") as f:
		ENV = json.load(f)

	API_KEY = ENV["OPENAI_API_KEY"]

	OPENAI_CLIENT = openai.OpenAI(
		api_key=API_KEY,
	)



SYSTEM_MESSAGE = ""
SYSTEM_MESSAGE += "You add debug information based on user request.\n"

BEGINNING_OF_USER_MESSAGE = ""
BEGINNING_OF_USER_MESSAGE += "You are running inside a python module called `infoinject`.\n"
BEGINNING_OF_USER_MESSAGE += "The goal of this module is to allow people to get detailed debug information without"
BEGINNING_OF_USER_MESSAGE += " cluttering their code with print statements.\n"
BEGINNING_OF_USER_MESSAGE += "For example, take this function:\n"
BEGINNING_OF_USER_MESSAGE += "```python\n"
BEGINNING_OF_USER_MESSAGE += "def add(a, b):\n"
BEGINNING_OF_USER_MESSAGE += "    return a + b\n"
BEGINNING_OF_USER_MESSAGE += "```\n"
BEGINNING_OF_USER_MESSAGE += "If you wanted to print the result of `add(1, 2)`, you could do something like:\n"
BEGINNING_OF_USER_MESSAGE += "```python\n"
BEGINNING_OF_USER_MESSAGE += "def add(a, b):\n"
BEGINNING_OF_USER_MESSAGE += "    print(f\"adding {a} + {b} = {a+b}\")"
BEGINNING_OF_USER_MESSAGE += "    return a + b\n"
BEGINNING_OF_USER_MESSAGE += "```\n"
BEGINNING_OF_USER_MESSAGE += "This can add up to a lot of useless code, especially if you have a lot of functions.\n"
BEGINNING_OF_USER_MESSAGE += "This module allows you to do something like:\n"
BEGINNING_OF_USER_MESSAGE += "```python\n"
BEGINNING_OF_USER_MESSAGE += "@inject_debug_info_using_AI(\"print the result of a and b\")\n"
BEGINNING_OF_USER_MESSAGE += "def add(a, b):\n"
BEGINNING_OF_USER_MESSAGE += "    return a + b\n"
BEGINNING_OF_USER_MESSAGE += "```\n"
BEGINNING_OF_USER_MESSAGE += "This is where you come in, you are the AI and you get called whenever `@inject_debug_info_using_AI` is used.\n"
BEGINNING_OF_USER_MESSAGE += "You will soon be given the function in question, and the user's request.\n"
BEGINNING_OF_USER_MESSAGE += "You will then use a tool called \"inject_code\" to inject the print statement into the function.\n"
BEGINNING_OF_USER_MESSAGE += "You will need to provide the line number to inject the code at.\n"
BEGINNING_OF_USER_MESSAGE += "For safety reasons, if your code does not start with `print`, it will be rejected.\n"
BEGINNING_OF_USER_MESSAGE += "For additional safety, your code must not have any side effects. We will check this.\n"
BEGINNING_OF_USER_MESSAGE += "NOTE: YOU MUST PUT ALL YOUR CODE INSIDE THE FUNCTION WITH THE `infoinject` DECORATOR.\n"
BEGINNING_OF_USER_MESSAGE += "EXAMPLE:\n"
BEGINNING_OF_USER_MESSAGE += "FUNCTION:\n"
BEGINNING_OF_USER_MESSAGE += "```python\n"
BEGINNING_OF_USER_MESSAGE += "def add(a, b):\n"
BEGINNING_OF_USER_MESSAGE += "    return a + b\n"
BEGINNING_OF_USER_MESSAGE += "```\n"
BEGINNING_OF_USER_MESSAGE += "REQUEST: \"print the result of a and b\"\n"
BEGINNING_OF_USER_MESSAGE += "CORRECT CODE TO INJECT: \"print(f\"adding {a} + {b} = {a+b}\")\"\n"
BEGINNING_OF_USER_MESSAGE += "\n\n\n"

TOOLS_FOR_AI = [
	{
		"type": "function",
		"function": {
			"name": "inject_code",
			"description": "inject a line or lines of code starting at a given line number",
			"parameters": {
				"type": "object",
				"properties": {
					"line_num": {
						"type": "integer"
					},
					"code": {
						"type": "string"
					}
				},
				"required": ["line_num", "code"],
			},
		}
	}
]



def _find_if_str_ahead(source, i, str):
	s = source[i:i+len(str)]
	return s == str




def _get_code_inserted(caller, source, line_no, test_code, args, kwargs):
	caller_name = caller.__name__
	lines = source.split("\n")

	min_indentation_level = 0
	indentation_level = 0
	indentation_type = " "

	# pass 1: find the min indentation level
	for li in range(len(lines)):
		if lines[li].strip().endswith(":"):
			min_indentation_level = len(lines[li]) - len(lines[li].lstrip())
			break

	# pass 2: find the indentation level of the line we want to insert at/
	for li in range(len(lines)):
		if not li == line_no:
			continue
		for j, c in enumerate(lines[li]):
			if c == " ":
				indentation_type = " "
				indentation_level += 1
			elif c == "\t":
				indentation_type = "\t"
				indentation_level += 1
			else:
				break
		if lines[li].strip().endswith(":"):
			indentation_level += 1

	print(f"min_indentation_level: {min_indentation_level}")
	print(f"indentation_level: {indentation_level}")
	print(f"indentation_type: {'space' if indentation_type == ' ' else 'tab'}")

	# pass 3: replace the original function name with a new one
	for li in range(len(lines)):
		for j, c in enumerate(lines[li]):
			if _find_if_str_ahead(lines[li], j, f"def {caller_name}"):
				new_line = lines[li][:j]
				new_line += "def __" + caller_name + "__" + lines[li][j+len(f"def {caller_name}"):]
				lines[li] = new_line

	prefix = indentation_type*indentation_level
	to_be_inserted = test_code.split("\n")

	for i, line in enumerate(to_be_inserted):
		to_be_inserted[i] = line.strip()
		to_be_inserted[i] = prefix + to_be_inserted[i]

	for line in to_be_inserted:
		lines.insert(line_no, line)

	lines = lines[2:]
	test_code = lines.copy()
	if indentation_type == "\t":
		test_code.insert(len(test_code), "\t" + f"return __{caller_name}__(*args, **kwargs)")
	else:
		test_code.insert(len(test_code), f"{' '*min_indentation_level}return __{caller_name}__(*args, **kwargs)")

	test_code.insert(0, f"def __test__(*args, **kwargs):")
	test_code.insert(len(test_code), f"locals()['__test__'] = __test__")

	out_code = "\n".join(lines)
	test_code = "\n".join(test_code)
	try:
		exec(test_code, globals(), locals())
		locals()['__test__'](*args, **kwargs) # type: ignore
	except Exception as e:
		print("\x1b[31mERROR: exception while executing test code.\x1b[0m")
		print(f"test_code: [[[\x1b[33m\n{test_code}\x1b[0m\n]]]")
		print(f"out_code: [[[\x1b[33m\n{out_code}\x1b[0m\n]]]")
		print(f"args: ", *args)
		print(f"kwargs: ", **kwargs)
		print(f"error: \x1b[1;31m{e}\x1b[0m")
		return None

	return out_code

def get_ai_response(injector_instance, caller, _prompt, test_args_and_kwargs, engine="davinci", temperature=0.9, max_tokens=150, top_p=1, frequency_penalty=0, presence_penalty=0, stop=None):
	global OPENAI_CLIENT, SYSTEM_MESSAGE, BEGINNING_OF_USER_MESSAGE, TOOLS_FOR_AI

	assert OPENAI_CLIENT is not None

	# if we had already compiled this function, just return the compiled version.
	if injector_instance._check_function_name_in_compiled_functions(caller.__name__):
		return injector_instance._get_compiled_function(caller.__name__)

	source = inspect.getsource(caller)

	prompt = BEGINNING_OF_USER_MESSAGE + "BEGIN:\n"
	prompt += "FUNCTION: ```python\n"
	prompt += source + "\n```\n"
	prompt += "REQUEST: \"" + _prompt + "\"\n"

	#print(f"\n\n\nprompt: [{prompt}]\n\n")

	response = OPENAI_CLIENT.chat.completions.create(
		model="gpt-4",
		messages=[
			{
				"role": "system",
				"content": SYSTEM_MESSAGE
			},
			{
				"role": "user",
				"content": prompt
			}
		],
		tools=TOOLS_FOR_AI, # type: ignore
		tool_choice="auto"
	)

	if response.choices[0].finish_reason != "tool_calls":
		print("ERROR: finish_reason != tool_calls")
		print(response)
		print("\n\x1b[0m", flush=True)
		return ""
	
	assert response.choices[0].message.tool_calls is not None
	tool_req = response.choices[0].message.tool_calls[0]
	#func_to_call = tool_req.function.name 	## not used right now, but may be used later.
	func_args = json.loads(tool_req.function.arguments)

	line_no_ = func_args["line_num"]
	code_ = func_args["code"]

	return _get_code_inserted(caller, source, line_no_, code_, test_args_and_kwargs[0], test_args_and_kwargs[1])

