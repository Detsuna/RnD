using EMVCo.QR;
using EMVCo.QR.Merchant;
using System;

namespace WebDemo.Payment.Components {
    public class PayNow : MerchantAccountInformation {
        public PayNow(Int32 id = 26) : base(id) { this.globallyUniqueIdentifier.data = "SG.PAYNOW"; }
        public DataObject proxyType { get; protected set; } = new DataObject(id: 1, format: Format.Numeric, presence: Presence.Mandatory);
        public DataObject proxyValue { get; protected set; } = new DataObject(id: 2, format: Format.AlphanumericSpecial, presence: Presence.Mandatory);
        public DataObject editableAmountInd { get; protected set; } = new DataObject(id: 3, format: Format.Numeric, presence: Presence.Optional) { data = "0" };
        public DataObject expiryDatetime { get; protected set; } = new DataObject(id: 4, format: Format.Numeric, presence: Presence.Optional) {
            //data = DateTime.Now.Add(TimeSpan.Parse("00:05:00")).ToString("yyyyMMddHHmmss")
            data = DateTime.Now.Add(new TimeSpan(days:2,hours:0,minutes:0,seconds:0)).ToString("yyyyMMdd")
        };
    }
}