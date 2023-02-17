from adafruit_logging import LoggingHandler

class AIOHandler(LoggingHandler):

    def __init__(self, name, portal_device):
        """Create an instance."""
        self._log_feed_name=f"{name}-logging"
        if not issubclass(type(portal_device), PortalBase):
            raise TypeError("portal_device must be a PortalBase or subclass of PortalBase")
        self._portal_device = portal_device


    def emit(self, level, msg):
        """Generate the message and write it to the AIO Feed.

        :param level: The level at which to log
        :param msg: The core message

        """
        self._portal_device.push_to_io(self._log_feed_name, self.format(level, msg))