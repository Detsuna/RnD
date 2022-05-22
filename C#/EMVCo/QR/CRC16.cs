using System;

namespace EMVCo.QR {
    public static class CRC16 {
        public const UInt16 poly = 0x1021;
        public const UInt16 initialValue = 0xFFFF;
        public static UInt16 CRC16CCITT(byte[] bytes) {
            UInt16 crc = initialValue;
            foreach (Byte b in bytes) {
                crc ^= (UInt16)(b << 8);
                for (Byte j = 0; j < 8; j++) {
                    if ((crc & 0x8000) > 0) {
                        crc = (UInt16)((crc << 1) ^ poly);
                    } else {
                        crc <<= 1;
                    }
                }
            }
            return crc;
        }
        //public static ushort CRC16CCITT(byte[] bytes) {
        //    const ushort poly = 0x1021;
        //    ushort[] table = new ushort[256];
        //    ushort initialValue = 0xffff;
        //    ushort temp, a;
        //    ushort crc = initialValue;
        //    for (int i = 0; i < table.Length; ++i) {
        //        temp = 0;
        //        a = (ushort)(i << 8);
        //        for (int j = 0; j < 8; ++j) {
        //            if (((temp ^ a) & 0x8000) != 0)
        //                temp = (ushort)((temp << 1) ^ poly);
        //            else
        //                temp <<= 1;
        //            a <<= 1;
        //        }
        //        table[i] = temp;
        //    }
        //    foreach (Byte b in bytes) {
        //        crc = (ushort)((crc << 8) ^ table[((crc >> 8) ^ (0xff & b))]);
        //    }
        //    return crc;
        //}
    }
}
