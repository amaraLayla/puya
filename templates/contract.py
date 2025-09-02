from algopy import ARC4Contract, arc4
from algopy.logic import Txn, Box

class GitHubBoxContract(ARC4Contract):
    @arc4.abimethod
    def deposit(self, github_handle: arc4.String) -> arc4.UInt64:
        Box.put("github", github_handle.bytes())
        return arc4.UInt64(1)
