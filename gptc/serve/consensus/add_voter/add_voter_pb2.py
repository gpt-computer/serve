from google.protobuf import __version__ as __pb__version__

if __pb__version__.startswith("4"):
    from gptc.serve.consensus.add_voter.pb.add_voter_pb2 import *
else:
    from gptc.serve.consensus.add_voter.pb2.add_voter_pb2 import *
