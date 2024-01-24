from typing import Any

from faust.serializers import codecs


class ProtobufSerializer(codecs.Codec):
    """
    see https://stackoverflow.com/questions/64686686/using-python-compiled-protobuf-pb2-as-key-and-value-serializer
    """
    def __init__(self, pb_type: Any):
        self.pb_type = pb_type
        super(self.__class__, self).__init__()

    def _dumps(self, pb: Any) -> bytes:
        return pb.SerializeToString()

    def _loads(self, s: bytes) -> Any:
        pb = self.pb_type()
        pb.ParseFromString(s)
        return pb
