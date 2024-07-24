import ait.core.log

from ait.core.server.handler import Handler


class DebugHandler(Handler):
    def __init__(self, input_type=None, output_type=None, **kwargs):
        super(DebugHandler, self).__init__(input_type, output_type)

    def handle(self, input_data):
        ait.core.log.info(f"Debug handler received {len(input_data)} bytes")
        ait.core.log.info(input_data)
        return input_data
