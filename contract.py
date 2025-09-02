from pyteal import *

def approval_program():
    handle_deposit = Seq([
        App.globalPut(Bytes("github_handle"), Txn.application_args[0]),
        Return(Int(1))
    ])

    program = Cond(
        [Txn.application_id() == Int(0), Return(Int(1))],  # On create
        [Txn.on_completion() == OnComplete.NoOp, handle_deposit]
    )

    return program

def clear_program():
    return Return(Int(1))

if __name__ == "__main__":
    with open("GitHubBoxContract.approval.teal", "w") as f:
        f.write(compileTeal(approval_program(), mode=Mode.Application))

    with open("GitHubBoxContract.clear.teal", "w") as f:
        f.write(compileTeal(clear_program(), mode=Mode.Application))
