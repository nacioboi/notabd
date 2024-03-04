import dataclasses







@dataclasses.dataclass
class DebugMode:



	name: str
	level: int
	override_instructions: "list[str]|None"



	def set_override_do_ever_write(self, do_ever_write: bool) -> None:
		if self.override_instructions is None:
			self.override_instructions = []
		self.override_instructions.append(
			f"do_ever_write={'None' if do_ever_write is None else do_ever_write}"
		)
	


	def set_override_write_to_handle(self, file_handle: "int|None") -> None:
		if self.override_instructions is None:
			self.override_instructions = []
		self.override_instructions.append(
			f"write_to_handle={'None' if file_handle is None else str(file_handle)}"
		)


	
	def set_override_write_to_file(self, file_name: "str|None") -> None:
		if self.override_instructions is None:
			self.override_instructions = []
		self.override_instructions.append(
			f"write_to_file={'None' if file_name is None else file_name}"
		)
