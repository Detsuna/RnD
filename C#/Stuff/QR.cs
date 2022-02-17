/*
using QRCoder;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Xml;

namespace Stuff {
    public static class QR {
        public static String GenerateQrSvg() {
            QRCodeGenerator qrGenerator = new QRCodeGenerator();
            SvgQRCode qrCode = new SvgQRCode(
                qrGenerator.CreateQrCode("The text which should be encoded.", QRCodeGenerator.ECCLevel.Q) //https://en.wikipedia.org/wiki/QR_code#Error_correction
            );
            return qrCode.GetGraphic(new System.Drawing.Size(100, 100));
        }
        public static void Demo() {
            File.WriteAllText(@".\svg.svg", CellSpacing(GenerateQrSvg()));
        }
        public static String CellSpacing(String svg) {
            XmlDocument doc = new XmlDocument();            
            doc.LoadXml(svg);
            //Console.WriteLine(svg);
            foreach (XmlElement elem in doc.GetElementsByTagName("rect")) {
                elem.SetAttribute("stroke", "white");
                elem.SetAttribute("stroke-width", "0.1%");
            };
            return doc.OuterXml;
        }
    }
}*/
