using System;
using System.Collections;
using System.Collections.Generic;
using System.Net;

namespace Licensing {
    public sealed class LicenseManager {
        class prover : ILicenseProvider {
            public void Dispose() { }
        }
        private LicenseManager() { }
        private static readonly LicenseManager instance = new LicenseManager();
        private static readonly IDictionary<Type, ILicenseProvider> providers = new Dictionary<Type, ILicenseProvider>();

        public static void Register<T>(ILicenseProvider provider) where T : ILicensed {
            providers.Add(typeof(T), provider);
        }
        public static string Validate<T>() where T : ILicensed {
            return providers[typeof(T)].GetType().Name;
        }
    }
}