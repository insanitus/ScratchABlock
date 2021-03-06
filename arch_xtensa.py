from core import ADDR, REG
from archutils import *


BITNESS = 32
ENDIANNESS = "little"

ALL_REGS = {REG("a0"), REG("sp")} | reg_range("a", 2, 15)


def call_params(addr):
    return reg_range("a", 2, 7)


def param_filter(regs):
    #return regs
    #return regs & reg_range("a", 2, 7)
    # van Emmerik p.143
    # We know that for Xtensa params are passed in regs, and ignore case
    # of passing extra regs on stack so far.
    return reg_continuous_subrange(regs, reg_range("a", 2, 7))


def call_ret(addr):
    return reg_range("a", 2, 5)


def ret_filter(regs):
    # Simple filter
    #return regs & reg_range("a", 2, 5)

    # Ordered filter: if we know that returns should use a2, a3, a4, a5
    # in order, then if we have a2, a4 as potential returns, we known that
    # a4 is spurious.
    return reg_continuous_subrange(regs, reg_range("a", 2, 5))


def call_save(addr):
    return reg_range("a", 12, 15) | {REG("sp")}


def call_defs(addr):
    return call_ret(addr) | (ALL_REGS - call_save(addr))


def ret_uses(cfg):
    # a0 contains return address
    # sp should be preserved across call, but we'll check that using sp0 pseudo-reg.
    #return {REG("a0"), REG("sp")}
    return set()
