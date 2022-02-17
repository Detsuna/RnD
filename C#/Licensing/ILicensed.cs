using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Licensing {
    public interface ILicensed {
        public static readonly string Dunno = LicenseManager.Validate<ILicensed>();
    }
}
