from .color_config import ColorConfiguration
from .logger import _debug_print

import inspect
import datetime






class DebugContext:
	"""
	You may specify new separate logging contexts.
	A Logging Context will allow, for example, separating the logging output
	of two different threads.
	This will allow easier understanding of the logs.
	"""

	def __init__(self, name:str, do_use_time=False,
			colors:"ColorConfiguration"=ColorConfiguration._default(),
			time_format:str="%H:%M:S") -> None:
		self.name = name
		self.do_use_time = do_use_time
		self.colors = colors
		self.time_format = time_format
		self.class_name = None
		self.color_on_flag = True

	def _always(self):
		global ACTIVE_DEBUG_CONTEXT
		ACTIVE_DEBUG_CONTEXT = self

	def set_color_on(self):
		self._always()
		self.color_on_flag = True
	
	def set_color_off(self):
		self._always()
		self.color_on_flag = False
	
	def set_class_name(self, class_name):
		self._always()
		self.class_name = class_name

	def __get_caller_function(self, position):
		self._always()
		return inspect.stack()[position+2][3]

	def _get_colored_time(self) -> str:
		self._always()
		if not self.do_use_time:
			return ""
		color = ""
		if self.color_on_flag:
			color = self.colors.time_color
		if len(self.time_format) != 0:
			return f"{color}{datetime.datetime.now().strftime(self.time_format)}{self.colors.reset_color}"
		else:
			return f"{color}{datetime.datetime.now()}{self.colors.reset_color}"

	def _get_colored_class_name(self) -> str:
		self._always()
		color = ""
		if self.color_on_flag:
			color = self.colors.class_color
		return f"{color}{self.class_name}{self.colors.reset_color}"

	def _get_colored_caller_function(self) -> str:
		self._always()
		color = ""
		if self.color_on_flag:
			color = self.colors.caller_color
		return f"{color}{self.__get_caller_function(1)}{self.colors.reset_color}"

	def get_time(self):
		self._always()
		return self._get_colored_time()

	def get_class_name(self):
		self._always()
		return self._get_colored_class_name()

	def get_caller_function(self, position):
		self._always()
		return self._get_colored_caller_function(position)

	def log_line(self, *args, **kwargs):
		self._always()
		normal_color = ""
		message_color = ""
		if self.color_on_flag:
			normal_color = self.colors.normal_color
			message_color = self.colors.message_color

		msg = ""
		msg += f"{normal_color}[{self.colors.reset_color}"
		msg += self._get_colored_time()
		msg += f"{normal_color}]~[{self.colors.reset_color}"
		msg += self._get_colored_class_name()
		msg += f"{normal_color}.{self.colors.reset_color}"
		msg += self._get_colored_caller_function()
		msg += f"{normal_color}]>>>{message_color}"

		_debug_print(self, msg, *args, **kwargs)

	def get_reset_poison(self):
		self._always()
		return "\033[1m~\033[0m"

	def __sequence_occurs_after(self, sequence, string, index):
		self._always()
		try:
			for i, char in enumerate(sequence):
				if string[index+i] != char:
					return False
			return True
		except IndexError:
			return False

	def simple_log_line(self, *args, **kwargs):
		with Woody.get_lock(threading.get_ident()):
			self._always()
			msg = ""
			for arg in args:
				msg += f"{arg} "
			
			def filter(msg, start_index):
				_msg = msg
				_sequence1 = self.get_reset_poison()
				_sequence2 = "\033[0m"
				for i in range(start_index, len(_msg)):
					if self.__sequence_occurs_after(_sequence1, _msg, i):
						_msg = _msg[:i] + "\033[0m" + _msg[i+len(_sequence1):]
						return _msg, i
					if self.__sequence_occurs_after(_sequence2, _msg, i):
						_msg = _msg[:i] + self.colors.normal_color + _msg[i+len(_sequence2):]
						return _msg, i
				
				return None, None
			
			index = 0
			while True:
				_msg = None
				_msg, index = filter(msg, index)
				if _msg == None:
					break
				msg = _msg
				index = index + 1
			
			_debug_print(self, self.colors.normal_color, msg, **kwargs)


	def simple_log(self, *args, **kwargs):
		self._always()
		if not "end" in kwargs:
			kwargs["end"] = ""
		_debug_print(self, "", *args, **kwargs)
