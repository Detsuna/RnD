using System;
using System.Collections.Generic;
using System.Text;

namespace EMVCo.QR.Merchant {
    public class Presentation : Template {
        public Presentation() : base(id: -1, format: Format.String, presence: Presence.Mandatory) { }

        // QR Code Conventions
        public DataObject payloadFormatIndicator { get; } = new DataObject(id: 0, format: Format.Numeric, presence: Presence.Mandatory) { data = "01" };
        public DataObject pointOfInitiationMethod { get; } = new DataObject(id: 1, format: Format.Numeric, presence: Presence.Optional) { data = "12" };
        public DataObject cyclicRedundancyCheck { get; } = new DataObject(id: 63, format: Format.AlphanumericSpecial, presence: Presence.Mandatory) { data = "0000" };

        // Merchant Account Information
        public IList<MerchantAccountInformation> merchantAccountInformation { get; } = new List<MerchantAccountInformation>();

        //Additional Merchant Information
        public DataObject merchantCategoryCode { get; set; } = new DataObject(id: 52, format: Format.Numeric, presence: Presence.Mandatory) { data = "0000" };
        public DataObject countryCode { get; set; } = new DataObject(id: 58, format: Format.AlphanumericSpecial, presence: Presence.Mandatory);
        public DataObject merchantName { get; set; } = new DataObject(id: 59, format: Format.AlphanumericSpecial, presence: Presence.Mandatory);
        public DataObject merchantCity { get; set; } = new DataObject(id: 60, format: Format.AlphanumericSpecial, presence: Presence.Mandatory);

        // Transaction Value
        public DataObject transactionAmount { get; set; } = new DataObject(id: 54, format: Format.AlphanumericSpecial, presence: Presence.Mandatory);
        public DataObject transactionCurrency { get; set; } = new DataObject(id: 53, format: Format.Numeric, presence: Presence.Mandatory);
        public DataObject postalCode { get; set; } = new DataObject(id: 61, format: Format.AlphanumericSpecial, presence: Presence.Optional);

        public AdditionalDataField additionalDataField { get; protected set; } = new AdditionalDataField();


        public override String ToPayload() {
            StringBuilder sb = new StringBuilder(base.ToPayload());
            this.cyclicRedundancyCheck.data = CRC16.CRC16CCITT(Encoding.ASCII.GetBytes(sb.ToString())).ToString("X4");
            sb.Append(this.cyclicRedundancyCheck.ToPayload());
            return sb.ToString();
        }
    }
}
