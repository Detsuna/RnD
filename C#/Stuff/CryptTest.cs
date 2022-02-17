using Microsoft.VisualStudio.TestTools.UnitTesting;
using System;
using System.Globalization;
using System.Security.Cryptography;
using System.Text.RegularExpressions;

namespace Stuff {
    [TestClass]
    public class CryptTest {

        [TestMethod]
        public void RsaKey() {
            Console.WriteLine(RSA.Create().ToXmlString(true));
        }
    }
}