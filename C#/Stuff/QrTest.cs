using EMVCo.QR;
using Microsoft.VisualStudio.TestTools.UnitTesting;
using System;
using System.Collections.Generic;
using System.Text;

namespace Stuff {
    public class SGQR : EMVCo.QR.Merchant.Presentation {
        public SGQR() {
            this.merchantCategoryCode.data = "0000";
            this.transactionCurrency.data = "702";
            this.countryCode.data = "SG";
            this.merchantCity.data = "Singapore";
        }
    }
    public class PayNow : EMVCo.QR.Merchant.MerchantAccountInformation {
        public PayNow(Int32 id = 26) : base(id) { this.globallyUniqueIdentifier.data = "SG.PAYNOW"; }
        public DataObject proxyType { get; protected set; } = new DataObject(id: 1, format: Format.Numeric, presence: Presence.Mandatory);
        public DataObject proxyValue { get; protected set; } = new DataObject(id: 2, format: Format.AlphanumericSpecial, presence: Presence.Mandatory);
        public DataObject editableAmountInd { get; protected set; } = new DataObject(id: 3, format: Format.Numeric, presence: Presence.Optional) { data = "0" };
        public DataObject expiryDatetime { get; protected set; } = new DataObject(id: 4, format: Format.Numeric, presence: Presence.Optional) { data = DateTime.Now.Add(TimeSpan.Parse("00:05:00")).ToString("yyyyMMddHHmmss") };
    }

    [TestClass]
    public class QrTest {
        [TestMethod]
        public void Crc() {
            const String payload1 = "00020101021126500009SG.PAYNOW010100211+659855342903010040820220531520400005303702540520.005802SG5902NA6009Singapore62080104Taxi6304A43D";
            const String payload2 = "00020101021126370009SG.PAYNOW010120210200210788N030115204000053037025802SG5916G.TECH PTE. LTD.6009Singapore63040993";
            Assert.AreEqual(CRC16.CRC16CCITT(Encoding.ASCII.GetBytes(payload1.Substring(0, payload1.Length - 4))).ToString("X4"), payload1.Substring(payload1.Length - 4));
            Assert.AreEqual(CRC16.CRC16CCITT(Encoding.ASCII.GetBytes(payload2.Substring(0, payload2.Length - 4))).ToString("X4"), payload2.Substring(payload2.Length - 4));
        }

        [TestMethod]
        public void Payload() {
            String payload;
            using (SGQR sgqr = new SGQR()) {
                sgqr.pointOfInitiationMethod.data = "12";
                sgqr.transactionAmount.data = "1.00";
                sgqr.merchantName.data = "NA";
                sgqr.additionalDataField.billNumber.data = $"POC_{DateTime.Now:yyyyMMddHHmmssfff}";

                PayNow payNow = new PayNow();
                payNow.proxyType.data = "0";
                payNow.proxyValue.data = "+65 9855 3429".Replace(" ", String.Empty);
                //payNow.expiryDatetime.data = "20220531";
                payNow.editableAmountInd.data = "0";
                sgqr.merchantAccountInformation.Add(payNow);
                payload = sgqr.ToPayload();
            }
            Console.WriteLine(payload);
        }
    }
}