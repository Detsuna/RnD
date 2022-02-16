from math import lcm, log2


class RSA() : 
    def  __init__(self, P, Q, Exponent=65537) : 
        self.P = P
        self.Q = Q
        self.Exponent = Exponent

        # DP
        # DQ
        # InverseQ

        self.Modulus = P * Q
        toitent = lcm((self.P - 1), (self.Q - 1)) # toitent = (self.P - 1) * (self.Q - 1)
        self.D = pow(self.Exponent, -1, toitent) # self.Exponent**(toitent - 1) % toitent # -1 ∵ modulus[toitent] is not prime; for inverse power mod

    def __del__(self) : del self.__dict__
    def __enter__(self) : return self
    def __exit__(self, type, value, tb) : self.__del__()

    def EnCrypt(self, p) : return self.Crypt(m=p, key=self.Exponent)
    def DeCrypt(self, c) : return self.Crypt(m=c, key=self.D)
    def Crypt(self, m, key) : return m**key % self.Modulus


if __name__ == "__main__" : 
    with RSA(13, 7, 5) as rsa : 
        message = b"HELLO WORLD"

        message = bytearray([rsa.EnCrypt(m) for m in message])
        print(message)
        message = bytearray([rsa.DeCrypt(m) for m in message])
        print(message)

    with RSA(61, 53, 17) as rsa : 
        bitz = int(log2(rsa.Modulus))
        bytez = -(bitz // -8)
        message = b"Hello World!"

        message = "{0:0b}".format(int.from_bytes(message, "big")) ; message = message.zfill(-(len(message)//-bitz)*bitz)
        message = [int(message[i:i+bitz], 2) for i in range(0, len(message), bitz)]
        message = [rsa.EnCrypt(m) for m in message]
        message = b"".join([m.to_bytes(bytez, "big") for m in message])
        print(message)
        message = [int.from_bytes(message[i:i+bytez], "big") for i in range(0, len(message), bytez)]
        message = [rsa.DeCrypt(m) for m in message]
        message = "".join(["{0:0>{1}b}".format(m, bitz) for m in message])
        message = int(message, 2).to_bytes(-(len(message)// -8), "big").strip(b"\x00")
        print(message)

    pass
