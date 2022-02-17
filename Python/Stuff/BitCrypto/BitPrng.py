from math import log2


class BitPrng() : 
    def __init__(self, bitz:int=1) -> None : 
        self.mask = int("".join(["1" for _ in range(bitz)]), 2)
        self.offset = 1<<(bitz -1) | 1<<(bitz -1)>>3 | 1<<(bitz // 2) | 1<<int(log2(bitz)) | 1
        self.overflow = int("11000011"*-(bitz // -8), 2) & self.mask<<1 | 1
        self.cycles = int(log2(bitz)) | 1
        self.cycles = (self.cycles + 4) if (self.cycles & 1) else (self.cycles - 1)
    def Next(self, seed:int) -> int : 
        for _ in range(self.cycles) : seed = (seed * self.overflow ^ self.offset + self.offset + 1) & self.mask
        return seed


if __name__ == "__main__" : 
    for bitz in range(1, 101) : # [256, 512, 1024, 2048, 4096, 8192] : 
        prng = BitPrng(bitz)
        v = prng.Next(0)
        # print(f"{v:0>{-(bitz // -4)}x}"[:10])
        print(f"[BitPrng({bitz: >3})] " + f"hex:{v:0>{-(bitz // -4)}x}"[:10]) # , int:{v}")#[:10])

    for bitz in [256, 512, 1024, 2048, 4096, 8192] : # range(20, 42) : # 
        prng = BitPrng(bitz)
        print("================")
        print(f"BitPrng({bitz})")#[:10])
        print("================")
        for i in range(10) : 
            print(f"{prng.Next(i):0>{-(bitz // -4)}x}"[:10]) # , max: {2**bitz-1}") # "[:10]):0>{-(bitz // -4)}x
        print("================\n")

    for bitz in range(1, 21) : 
        prng = BitPrng(bitz)
        start = end = count = 0
        while True : 
            end = prng.Next(end)
            count = count + 1
            if start==end : break
        print(f"expected:{2**bitz: >7}, actual:{count: >7}")
    