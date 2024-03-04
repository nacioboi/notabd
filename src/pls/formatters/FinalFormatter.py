from abc import ABC, abstractmethod

import base64







class IFinalFormatter(ABC):



	# NOTE: The point of having postfixes is so the final formatter can know the different pieces.
	def _get_unique_postfix(self) -> str:
		name = self.__class__.__name__
		b64_name = base64.b64encode(name.encode("utf-8")).decode("utf-8")
		return f"|`FORMATTER_POSTFIX`{b64_name}|"



	def _strip_postfixes(self, string:str) -> str:
		# example string: `abc - foo|def - bar|ghi - hi|`

		if string == "":
			return string

		if not string.endswith("|"):
			raise Exception("This should never happen.")

		ret_str = ""
		_splitted = string.split("|`FORMATTER_POSTFIX`")[:-1]  # last is always fluff.
		ret_str += _splitted[0]  # first is always juicy.
		_splitted = _splitted[1:]

		for splitted in _splitted:
			end = None
			# look for the closing pipe...
			for i, char in enumerate(splitted):
				if char == "|":
					end = i
			assert end is not None
			ret_str += splitted[end:]
		
		return ret_str
				


	@abstractmethod
	def raw_handle(self, string:str) -> str:
		pass