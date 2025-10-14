
class Singleton:
    """The Singleton pattern ensures that a class has
    only one instance and provides a global point
    of access to it."""

    __instance = None

    @staticmethod
    def getInstance():
        if Singleton.__instance == None:
            Singleton()
        return Singleton.__instance

    def __init__(self):
        if Singleton.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            Singleton.__instance = self


class Button:
    def render(self):
        pass
class WindowsButton(Button):
    def render(self):
        return "Windows Button Rendered"
class MacOSButton(Button):
    def render(self):
        return "MacOS Button Rendered"

"""Description
The Observer pattern defines a one-to-many 
dependency between objects so that when one 
object changes state, all its 
dependents are notified and 
updated automatically.

Example"""
class Subject:
    def __init__(self):
        self.__observers = []
    def register_observer(self, observer):
        self.__observers.append(observer)
    def notify_observers(self, message):
        for observer in self.__observers:
            observer.notify(message)
class Observer:
    def notify(self, message):
        pass
class EmailAlerts(Observer):
    def notify(self, message):
        print(f"Email Alert: {message}")
class SMSAlerts(Observer):
    def notify(self, message):
        print(f"SMS Alert: {message}")


#          Command Pattern example classes

class SwitchOnCommand(object):
    def __init__(self, device):
        self.device = device

    def execute(self):
        self.device.switch_on()

class SwitchOffCommand(object):
    def __init__(self, device):
        self.device = device

    def execute(self):
        self.device.switch_off()

class Device(object):
    def switch_on(self):
        print(f"Device turned on")

    def switch_off(self):
        print(f"Device turned off")

class RemoteControl(object):
    def __init__(self):
        self.commands = []

    def set_command(self, command):
        self.commands.append(command)

    def press_button(self):
        for cmd in self.commands:
            cmd.execute()


#          **************** test methods ****************

class Tests:

    @staticmethod
    def TestSingleton1():
        # Usage
        s = Singleton.getInstance()
        print(s)
        s2 = Singleton.getInstance()
        print(s2)
        # Both instances are the same

    # Factory Method Pattern
    # Description
    # This pattern provides an interface for creating
    # objects in a superclass but allows subclasses
    # to alter the type of objects that will be
    # created.

    @staticmethod
    def TestFactory():
        # Usage
        button = Tests.get_button("Windows")
        print(button.render())
        button2 = Tests.get_button("MacOS")
        print(button2.render())

    @staticmethod
    def get_button(os: str):
        if os == "Windows":
            return WindowsButton()
        elif os == "MacOS":
            return MacOSButton()

    #     Observer Pattern test
    # The Observer pattern defines a one-to-many
    # dependency between objects so that when
    # one object changes state, all its
    # dependents are notified and updated
    # automatically.
    @staticmethod
    def testObserverPattern():
        # Usage
        subject = Subject()
        email_alerts = EmailAlerts()
        sms_alerts = SMSAlerts()
        subject.register_observer(email_alerts)
        subject.register_observer(sms_alerts)
        subject.notify_observers("Server Down!")


    @staticmethod
    def test_command_pattern():
        lamp = Device()
        controller = RemoteControl()

        controller.set_command(SwitchOnCommand(lamp))
        controller.press_button()

        controller.set_command(SwitchOffCommand(lamp))
        controller.press_button()


