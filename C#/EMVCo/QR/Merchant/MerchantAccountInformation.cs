using System;

namespace EMVCo.QR.Merchant {
    public class MerchantAccountInformation : Template {
        public MerchantAccountInformation(Int32 id) : base(id: id, format: Format.AlphanumericSpecial, presence: Presence.Mandatory) {
            if (id < 2 || 51 < id) { throw new ArgumentOutOfRangeException("MerchantAccountInformation id must be between 2-51"); }
        }
        public DataObject globallyUniqueIdentifier { get; protected set; } = new DataObject(id: 0, format: Format.AlphanumericSpecial, presence: Presence.Mandatory);
    }
}
