using EMVCo.QR.Merchant;

namespace WebDemo.Payment.Components {
    public class SGQR : Presentation {
        public SGQR() {
            this.merchantCategoryCode.data = "0000";
            this.transactionCurrency.data = "702";
            this.countryCode.data = "SG";
            this.merchantCity.data = "Singapore";
        }
    }
}