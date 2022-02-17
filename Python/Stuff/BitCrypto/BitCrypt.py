from io import BytesIO
from math import log2
from typing import BinaryIO

from BitPrng import BitPrng


class ByteCrypt() : 
    def __init__(self, bytez:int=1) -> None : 
        self.bytez = bytez
        self.bitz = self.bytez * 8
        self.mask = int("".join(["1" for _ in range(self.bitz)]), 2)
        self.cycles = 1<<self.bytez | 1
        self.Next = BitPrng(self.bitz).Next

    def __RotateL(self, n, d) : return ((n << d%self.bitz) | (n >> (self.bitz - d)%self.bitz)) & self.mask
    def __RotateR(self, n, d) : return ((n >> d%self.bitz) | (n << (self.bitz - d)%self.bitz)) & self.mask

    def Hash(self, data:BinaryIO) -> bytearray : 
        output = 0
        while (chunk:=data.read(self.bytez)) : output = (self.__RotateR(output, self.cycles) + self.Next(int.from_bytes(chunk, "big"))) & self.mask
        return bytearray(output.to_bytes(self.bytez, "big"))


if __name__ == "__main__" : 
    for bytez in range(1, 4) : 
        bitz = bytez * 8        
        crypt = ByteCrypt(bytez)
        start = bytearray(bytez)
        end = bytearray(bytez)
        count = 0
        while True : 
            end = crypt.Hash(BytesIO(end))
            count = count + 1
            if start==end : break
            elif count>2**bitz : 
                count = -1
                break
        print(f"expected:{2**bitz: >8}, actual:{count: >8}\n")

    crypt = ByteCrypt(4)
    hashes = {}
    with open("Tutte_le_parole_inglesi.txt", "rb") as f : 
        for l in f : 
            l = l.lower().strip()
            h = crypt.Hash(BytesIO(l)).hex()
            l = l.decode('UTF-8')
            if h in hashes : hashes[h] += [l]
            else : hashes[h] = [l]
    count = 0
    for (k, v) in hashes.items() : 
        if len(v)>1 :
            count += len(v)
            print(f"k:[{k}], v;{v}")
    print(f"clash count:{count}")

    pass

            
