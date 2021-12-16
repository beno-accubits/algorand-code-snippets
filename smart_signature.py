#sample_smart_sig.py
from pyteal import *

"""Basic Donation Escrow"""
def donation_escrow(benefactor):
    Fee = Int(1000)

    #Only the benefactor account can withdraw from this escrow
    program = And(
        Txn.type_enum() == TxnType.Payment,
        Txn.fee() <= Fee,
        Txn.receiver() == Addr(benefactor),
        Global.group_size() == Int(1),
        Txn.rekey_to() == Global.zero_address()        
    )
    # Mode.Signature specifies that this is a smart signature
    return compileTeal(program, Mode.Signature, version=5)
