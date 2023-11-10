from typing import Tuple, final

def init() -> None: ...
def quit() -> None: ...
def get_init() -> bool: ...
def get_count() -> int: ...
@final
class JoystickType:
    def __init__(self, id: int) -> None: ...
    def init(self) -> None: ...
    def quit(self) -> None: ...
    def get_init(self) -> bool: ...
    def get_id(self) -> int: ...
    def get_instance_id(self) -> int: ...
    def get_guid(self) -> str: ...
    def get_power_level(self) -> str: ...
    def get_name(self) -> str: ...
    def get_numaxes(self) -> int: ...
    def get_axis(self, axis_number: int) -> float: ...
    def get_numballs(self) -> int: ...
    def get_ball(self, ball_number: int) -> Tuple[float, float]: ...
    def get_numbuttons(self) -> int: ...
    def get_button(self, button: int) -> bool: ...
    def get_numhats(self) -> int: ...
    def get_hat(self, hat_number: int) -> Tuple[float, float]: ...
    def rumble(
        self, low_frequency: float, high_frequency: float, duration: int
    ) -> bool: ...
    def stop_rumble(self) -> None: ...

# according to the current implementation, Joystick is a function that returns
# a JoystickType instance. In the future, when the C implementation is fixed to
# add __init__/__new__ to Joystick and it's exported directly, the typestubs
# here must be updated too
def Joystick(id: int) -> JoystickType: ...
