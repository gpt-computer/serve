import grpc

from gptc.serve.consensus.add_voter.add_voter_pb2 import AddVoterRequest
from gptc.serve.consensus.add_voter.add_voter_pb2_grpc import RaftAdminStub


def call_add_voter(target, replica_id, voter_address):
    """Add a voter to a Raft cluster.

    :param target: The address of the Raft node to contact.
    :param replica_id: The ID of the replica to add as a voter.
    :param voter_address: The address of the new voter.
    :return: True if the voter was added successfully, False otherwise.
    """
    with grpc.insecure_channel(target) as channel:
        stub = RaftAdminStub(channel)

        req = AddVoterRequest(
            id=replica_id,
            address=voter_address,
            previous_index=0,
        )

        try:
            future = stub.AddVoter(req)
            add_voter_result = stub.Await(future)
            _ = stub.Forget(future)
            if not add_voter_result.error:
                return True
            else:
                return False
        except:
            return False


async def async_call_add_voter(target, replica_id, voter_address):
    """Asynchronously add a voter to a Raft cluster.

    :param target: The address of the Raft node to contact.
    :param replica_id: The ID of the replica to add as a voter.
    :param voter_address: The address of the new voter.
    :return: True if the voter was added successfully, False otherwise.
    """
    async with grpc.aio.insecure_channel(target) as channel:
        stub = RaftAdminStub(channel)

        req = AddVoterRequest(
            id=replica_id,
            address=voter_address,
            previous_index=0,
        )

        try:
            future = await stub.AddVoter(req)
            add_voter_result = await stub.Await(future)
            _ = await stub.Forget(future)
            if not add_voter_result.error:
                return True
            else:
                return False
        except:
            return False
