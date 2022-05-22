using System.Runtime.Serialization;

namespace EMVCo.QR {
    public enum Format {
        [EnumMember(Value = "AN")] Alphanumeric,
        [EnumMember(Value = "ANS")] AlphanumericSpecial,
        [EnumMember(Value = "B")] Binary,
        [EnumMember(Value = "CN")] CompressedNumeric,
        [EnumMember(Value = "N")] Numeric,
        [EnumMember(Value = "S")] String
    }
}
