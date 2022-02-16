using Microsoft.VisualStudio.TestTools.UnitTesting;
using System;
using System.Globalization;
using System.Text.RegularExpressions;

namespace Stuff {
    [TestClass]
    public class RegexTest {
        public Regex comments { get; } = new Regex("--[^(\r|\n)]*(\r|\n)*", RegexOptions.Compiled);
        const String expected = "Line1 : thingy  Line2 : thingy  ";


        [TestMethod]
        public void CarriageReturn() {
            Assert.AreEqual(expected, comments.Replace("Line1 : thingy -- REMOVE_TEST\rLine2 : thingy --\r", " "), false, CultureInfo.InvariantCulture);
        }

        [TestMethod]
        public void NewLine() {
            Assert.AreEqual(expected, comments.Replace("Line1 : thingy -- REMOVE_TEST\nLine2 : thingy --\n", " "), false, CultureInfo.InvariantCulture);
        }

        [TestMethod]
        public void Both() {
            Assert.AreEqual(expected, comments.Replace("Line1 : thingy -- REMOVE_TEST\r\nLine2 : thingy --\r\n", " "), false, CultureInfo.InvariantCulture);
            Assert.AreEqual(expected, comments.Replace("Line1 : thingy -- REMOVE_TEST\n\rLine2 : thingy --\n\r", " "), false, CultureInfo.InvariantCulture);
        }
    }
}