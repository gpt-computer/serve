from google.protobuf import __version__ as __pb__version__

from gptc._docarray import docarray_v2 as is_docarray_v2

if __pb__version__.startswith("4"):
    if is_docarray_v2:
        from gptc.proto.docarray_v2.pb.gptc_pb2 import *
    else:
        from gptc.proto.docarray_v1.pb.gptc_pb2 import *

else:
    if is_docarray_v2:
        from gptc.proto.docarray_v2.pb2.gptc_pb2 import *
    else:
        from gptc.proto.docarray_v1.pb2.gptc_pb2 import *
