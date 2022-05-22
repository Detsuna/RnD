namespace EMVCo.QR.Merchant {
    public class AdditionalDataField : Template {
        public AdditionalDataField() : base(id: 62, format: Format.String, presence: Presence.Optional) { }
        public DataObject billNumber { get; protected set; } = new DataObject(id: 1, format: Format.AlphanumericSpecial, presence: Presence.Optional);
    }
}
