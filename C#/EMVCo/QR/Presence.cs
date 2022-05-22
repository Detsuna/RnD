using System.Runtime.Serialization;

namespace EMVCo.QR {
    public enum Presence {
        [EnumMember(Value = "M")] Mandatory,
        [EnumMember(Value = "C")] Conditional,
        [EnumMember(Value = "O")] Optional
    }
}
