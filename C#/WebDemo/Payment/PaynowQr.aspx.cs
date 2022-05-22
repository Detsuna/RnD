using QRCoder;
using System;
using System.IO;
using System.Reflection;
using System.Text;
using WebDemo.Payment.Components;
using static QRCoder.SvgQRCode;

namespace WebDemo.Payment {
    public partial class PaynowQr : System.Web.UI.Page {
        public static SvgLogo logo = new SvgLogo(File.ReadAllText(AppDomain.CurrentDomain.BaseDirectory + "Payment\\Components\\paynow-logo-2.svg"), iconSizePercent: 35,fillLogoBackground: false);
        static QRCodeGenerator generator = new QRCodeGenerator();
        protected void Page_Load(object sender, EventArgs e) { if (!Page.IsPostBack) { ReloadQR(sender, e); }     }
        protected void ReloadQR(Object sender, EventArgs e) {
            String payload;
            using (SGQR sgqr = new SGQR()) {
                sgqr.pointOfInitiationMethod.data = "12";
                sgqr.transactionAmount.data = "1.00";
                sgqr.merchantName.data = "NA";
                sgqr.additionalDataField.billNumber.data =  $"POC_{DateTime.Now:yyyyMMddHHmmssfff}";

                PayNow payNow = new PayNow();
                payNow.proxyType.data = "0";
                payNow.proxyValue.data = "+65 9855 3429".Replace(" ", String.Empty);
                //payNow.expiryDatetime.data = "20220531";
                payNow.editableAmountInd.data = "0";
                sgqr.merchantAccountInformation.Add(payNow);
                payload = sgqr.ToPayload();
            }
            //payload = "00020101021126500009SG.PAYNOW010100211+659855342903010040820220531520400005303702540520.005802SG5902NA6009Singapore62080104Taxi6304A43D";
            QRCodeData qrCodeData = generator.CreateQrCode(Encoding.ASCII.GetBytes(payload), QRCodeGenerator.ECCLevel.Q); // ECCLevel.H
            //PngByteQRCode qrCode = new PngByteQRCode(qrCodeData);
            //ImageQR.ImageUrl = "data:image;base64," + Convert.ToBase64String(qrCode.GetGraphic(20, new Byte[] { 124, 26, 120 }, new Byte[] { 255, 255, 255 }));
            SvgQRCode qrCode = new SvgQRCode(qrCodeData);
            ImageQR.ImageUrl = "data:image/svg+xml;base64," + Convert.ToBase64String(
                Encoding.UTF8.GetBytes(qrCode.GetGraphic(20, "#7C1A78", "#FFFFFF", logo: logo))
            );
        }
    }
}