class ColorConfiguration:
	def __init__(self) -> None:
		self.reset_color = "\033[0m"

	def _make_color(self, *args) -> str:
		return f"\033[{';'.join(args)}m"
	
	def set_normal_color(self, *args):
		self.normal_color = self._make_color(*args)
	
	def set_time_color(self, *args):
		self.time_color = self._make_color(*args)

	def set_class_color(self, *args):
		self.class_color = self._make_color(*args)
	
	def set_caller_color(self, *args):
		self.caller_color = self._make_color(*args)

	def set_message_color(self, *args):
		self.message_color = self._make_color(*args)

	@staticmethod
	def _default() -> "ColorConfiguration":
		configuration = ColorConfiguration()
		configuration.set_normal_color("97")
		configuration.set_time_color("36")
		configuration.set_class_color("33")
		configuration.set_caller_color("1","35")
		configuration.set_message_color("1","37")
		return configuration