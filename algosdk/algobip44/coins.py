from bip32 import HARDENED_INDEX
from typing import Tuple

__all__ = ("COIN_PATHS",)

def coin_path_by_index(index: int = 0) -> Tuple[int, int]:
    # Full list of coins and their indices is available at https://github.com/satoshilabs/slips/blob/master/slip-0044.md#registered-coin-types
    return (44 + HARDENED_INDEX, index + HARDENED_INDEX)

COIN_PATHS = {
    "BTC": coin_path_by_index(),
    # TESTNET - all registered coins, callable on testnet
    "TESTNET": coin_path_by_index(1), 
    "ETH": coin_path_by_index(60),
    "ALGO": coin_path_by_index(283) 
    # ALGO is no. 283, all Algorand ASAs are also retrievable through the same index as ALGO, 
    # though we'll have to directly query from user which ASA Token they want
    #"ASA": coin_path_by_index(283)
}