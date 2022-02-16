using Microsoft.VisualStudio.TestTools.UnitTesting;
using System;
using System.Collections.Generic;
using System.Globalization;
using System.Text.RegularExpressions;

namespace Stuff {
    public static class KeyStringExtensions {
        public static readonly Regex r = new Regex(@"(?<start>\{)+(?<property>[\w\.""'\[\]]+)(?<format>:[^}]+)?(?<end>\})+", RegexOptions.CultureInvariant | RegexOptions.IgnoreCase | RegexOptions.Compiled);

        public static Object GetProperty(this Object arg, String property) { return KeyString.Eval(arg, property); }
        public static String FormatKeys(this String format, Object? arg, IFormatProvider? formatProvider = null) {
            List<object> values = new List<object>();
            String rewrittenFormat = r.Replace(format, delegate (Match m) {
                Group startGroup = m.Groups["start"];
                Group propertyGroup = m.Groups["property"];
                Group formatGroup = m.Groups["format"];
                Group endGroup = m.Groups["end"];

                values.Add(KeyString.Eval(arg, propertyGroup.Value));

                return new String('{', startGroup.Captures.Count) + (values.Count - 1) + formatGroup.Value + new string('}', endGroup.Captures.Count);
            });
            return String.Format(rewrittenFormat, values.ToArray());
        }
    }
    public class KeyString : IFormatProvider, ICustomFormatter {
        public static readonly KeyString Provider = new KeyString();

        public Object? GetFormat(Type? formatType) { if (formatType == typeof(ICustomFormatter)) { return this; } else { return null; } }
        public static String Format(FormattableString formattable) { return formattable.ToString(Provider); }

        public String Format(String? format, Object? arg, IFormatProvider? formatProvider = null) {
            String[] formats = format.Split(':');
            format = (formats.Length > 1) ? $"{{0:{formats[1]}}}" : "{0}";
            return String.Format(format, Eval(arg, formats[0]));
        }
        public static Object Eval(Object arg, String property) {
            Object o = arg;
            IEnumerable<String> tokens = property.Split(new Char[] { '.', '"', '\'', '[', ']' }, StringSplitOptions.RemoveEmptyEntries | StringSplitOptions.TrimEntries);
            foreach (String token in tokens) {
                Object key = token; Int32 index;
                if (Int32.TryParse(token, out index)) { key = index; } else { index = -1; }

                if (o.GetType().GetProperty("Item") != null) {
                    o = o.GetType().GetProperty("Item").GetValue(o, new object[] { key });
                } else if (index > -1) { // array
                    o = (o as object[])[index];
                } else {
                    o = o.GetType().GetProperty(token).GetValue(o, null);
                }
            }
            return o;
        }
    }


    [TestClass]
    public class FormatTest {
        public class Faux {
            public static Faux Item = new Faux();
            public IDictionary<String, Object> prop { get; set; } = new Dictionary<String, Object>() {
                { "dict" , new { anonymous = new List<Object>(){
                    new object[] { DateTimeOffset.UnixEpoch}
                } } }
            };
        }

        [TestMethod]
        public void Prop() {
            DateTimeOffset actual, expected = DateTimeOffset.UnixEpoch;

            actual = (DateTimeOffset)Faux.Item.GetProperty("prop.[\"dict\"].anonymous[0][0]");
            Assert.AreEqual(expected, actual);

            actual = (DateTimeOffset)KeyString.Eval(Faux.Item, "prop.[\"dict\"].anonymous[0][0]");
            Assert.AreEqual(expected, actual);
        }

        [TestMethod]
        public void Format() {
            String actual, expected = DateTimeOffset.UnixEpoch.ToString("O");

            actual = String.Format(KeyString.Provider, "{0:prop.dict.anonymous.0.0:O}", Faux.Item);
            Assert.AreEqual(expected, actual, false, CultureInfo.InvariantCulture);

            actual = KeyString.Format($"{Faux.Item:[prop'dict']anonymous\"0\".0:O}");
            Assert.AreEqual(expected, actual, false, CultureInfo.InvariantCulture);

            actual = "{\"prop]dict'anonymous.0[0:O}".FormatKeys(Faux.Item);
            Assert.AreEqual(expected, actual, false, CultureInfo.InvariantCulture);
        }
    }
}