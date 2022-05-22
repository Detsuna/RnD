using System;

namespace EMVCo.QR {
    public class DataObject : IDisposable {
        public DataObject(Int32 id, Format format, Presence presence) {
            this.id = id;
            this.format = format;
            this.presence = presence;
        }

        public Int32 id { get; protected set; }
        public Format format { get; protected set; }
        public Presence presence { get; protected set; }
        public String data { get; set; } = String.Empty;

        public void Dispose() { }
        public virtual String ToPayload() {
            if (this.presence == Presence.Optional && this.data.Length == 0) { return String.Empty; }
            return $"{this.id:D2}{this.data.Length:D2}{this.data}";
        }
    }
}