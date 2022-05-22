using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using System.Reflection;
using System.Text;

namespace EMVCo.QR {
    public class Template : DataObject {
        public Template(Int32 id, Format format, Presence presence) : base(id: id, format: format, presence: presence) { }
        public override String ToPayload() {
            StringBuilder sb = new StringBuilder();
            IEnumerable<PropertyInfo> pis = this.GetType().GetProperties(BindingFlags.Public | BindingFlags.Instance).Where(delegate (PropertyInfo pi) {
                return ((typeof(DataObject).IsAssignableFrom(pi.PropertyType) || pi.PropertyType.IsGenericType) && !String.Equals(pi.Name, nameof(Merchant.Presentation.cyclicRedundancyCheck), StringComparison.OrdinalIgnoreCase));
            });
            IList<DataObject> dataObjects = new List<DataObject>();
            foreach (PropertyInfo pi in pis) {
                if (pi.PropertyType.IsGenericType) {
                    IList list = (IList)pi.GetValue(this);
                    foreach (DataObject obj in list) {
                        dataObjects.Add(obj);
                    }
                } else {
                    dataObjects.Add((DataObject)pi.GetValue(this));
                }
            }
            dataObjects = dataObjects.OrderBy(delegate (DataObject obj) { return obj.id; }).ToList();
            foreach (DataObject obj in dataObjects) {
                sb.Append(obj.ToPayload());
            }
            if (this.presence == Presence.Optional && sb.Length == 0) { return String.Empty; }

            if (this.id >= 0) { sb.Insert(0, $"{this.id:D2}{sb.ToString().Length:D2}"); }
            return sb.ToString();
        }
    }
}