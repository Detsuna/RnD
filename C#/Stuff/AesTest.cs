using Microsoft.VisualStudio.TestTools.UnitTesting;
using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using System.Security.Cryptography;
using System.Text;
using System.Text.RegularExpressions;


namespace Stuff {
    [TestClass]
    public class AesTest {
        String password = "password";
        String data = "data";

        public Aes aes;
        public AesTest() {
            this.aes = Aes.Create();
            SHA256 sha256 = SHA256.Create();
            aes.Key = sha256.ComputeHash(Encoding.UTF8.GetBytes(password));
            MD5 md5 = MD5.Create();
            aes.IV = md5.ComputeHash(Encoding.UTF8.GetBytes(password));
        }

        [TestMethod]
        public void w() {

            List<Byte> bytes = new List<Byte>();
            bytes.AddRange(Guid.NewGuid().ToByteArray());
            bytes.AddRange(Encoding.UTF8.GetBytes(data));
            bytes.AddRange(Guid.NewGuid().ToByteArray());

            bytes = aes.EncryptCbc(bytes.ToArray(), aes.IV).ToList();
            Console.WriteLine(Convert.ToBase64String(bytes.ToArray()));
            bytes = aes.DecryptCbc(bytes.ToArray(), aes.IV).ToList();
            Console.WriteLine($"[{Encoding.UTF8.GetString(bytes.GetRange(16, bytes.Count - 32).ToArray())}]");
        }

        [TestMethod]
        public void a() { }
    }
}