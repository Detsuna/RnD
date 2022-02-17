using Microsoft.VisualStudio.TestTools.UnitTesting;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Numerics;

namespace Stuff {
    public class BytePrng {
        public UInt64 bitz { get; protected set; }
        public UInt64 bytez { get; protected set; }
        public UInt64 mask { get; protected set; }
        public UInt64 offset { get; protected set; }

        public BytePrng(UInt64 bitz) {
            this.bitz = bitz;
            this.bytez = (UInt64)(-((Int64)this.bitz / -8)); // ceil ; upside down flooring
            this.mask = 1; for (BigInteger i = 0; i < this.bytez; i++) { this.mask = this.mask << 1; }; this.mask = this.mask - 1;
            IList <Byte> offsetBytes = new List<Byte>(); for (BigInteger i = 0; i < this.bytez; i++) { offsetBytes.Add(Convert.ToByte(0x99)); }
            this.offset = (UInt64)(new BigInteger(offsetBytes.ToArray()) / 2 * 2 + 1);
        }
        public BigInteger Next(BigInteger seed) {
            BigInteger result = new BigInteger(seed.ToByteArray());
            for (BigInteger i = 0; i < this.bytez * 2 + 1; i++) {
                result = (result * 271 ^ this.offset + this.offset + 1) % this.mask;
            }
            return result;
        }
    }

    [TestClass]
    public class BytePrngTest {
        [TestMethod]
        public void CarriageReturn() {
            //Assert.AreEqual(expected, comments.Replace("Line1 : thingy -- REMOVE_TEST\rLine2 : thingy --\r", " "), false, CultureInfo.InvariantCulture);
        }
    }
}