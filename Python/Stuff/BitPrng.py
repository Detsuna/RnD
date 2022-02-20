from math import log2
from time import sleep


class BitPrng() : 
    def __init__(self, bitz:int=1) : 
        self.mask = int("".join(["1" for _ in range(bitz)]), 2)
        self.offset = 1<<bitz>>1 | 1<<bitz>>int(log2(bitz))>>1 | 1<<(bitz // 2) | 1<<int(log2(bitz)) | 1
        self.overflow = int("11000011"*-(bitz // -8), 2) & self.mask<<1 | 1
        self.cycles = int(log2(bitz)) | 1
        self.cycles = (self.cycles + 4) if (self.cycles & 1) else (self.cycles - 1)
    def Next(self, seed:int) -> int : 
        for _ in range(self.cycles) : seed = (seed * self.overflow ^ self.offset + self.offset + 1) & self.mask
        return seed


if __name__ == "__main__" : 
    for bitz in range(1, 101) : 
        prng = BitPrng(bitz)
        v = prng.Next(0)
        inHex = f"{v:x}"
        inHex = f"{inHex[:5]}...{inHex[-5:]}" if len(inHex)>13 else f"{inHex: >13}"
        print(f"[BitPrng({bitz: >3})] => hex:" + f"[{inHex}]" + f", float:[{v/prng.mask:.3f}]\n")

    for bitz in [256, 512, 1023, 1024, 1025] : 
        prng = BitPrng(bitz)
        print("================")
        print(f"BitPrng({bitz}).Next(0->9)")
        print("================")
        for i in range(10) : 
            v = prng.Next(i)
            inHex = f"{v:x}"
            inHex = f"{inHex[:5]}...{inHex[-5:]}" if len(inHex)>13 else f"{inHex: >13}"
            print("hex:" + f"[{inHex}]" + f", float:[{v/prng.mask:.3f}]")
        print("================\n")

    for bitz in [256, 512, 1023, 1024, 1025] : 
        prng = BitPrng(bitz)
        print("================")
        print(f"BitPrng({bitz}).Next() x10")
        print("================")
        v = 0
        for _ in range(10) : 
            v = prng.Next(v)
            inHex = f"{v:x}"
            inHex = f"{inHex[:5]}...{inHex[-5:]}" if len(inHex)>13 else f"{inHex: >13}"
            print("hex:" + f"[{inHex}]" + f", float:[{v/prng.mask:.3f}]")
        print("================\n")

    for bitz in range(1, 21) : 
        prng = BitPrng(bitz)
        start = end = count = 0
        while True : 
            end = prng.Next(end)
            count = count + 1
            if start==end : break
        print(f"[BitPrng({bitz: >3}) range] => expected:{2**bitz: >8}, actual:{count: >8}")
    