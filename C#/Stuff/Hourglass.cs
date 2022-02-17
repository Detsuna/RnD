using Microsoft.VisualStudio.TestTools.UnitTesting;
using System;

namespace Stuff {
    [TestClass]
    public class Hourglass {
        public int size { get; set; } = 9;

        public String DisplayRow(int width) {
            String row = new String(' ', this.size - width);
            if (width > 1) {
                for (int i = 1; i <= width; i++) {
                    row = row + $"{i} ";
                }
                return (row + "\n" + DisplayRow(width - 1) + "\n" + row);
            } else {
                return (row + width.ToString());
            }
        }
        public String Display() { return DisplayRow(this.size); }

        [TestMethod]
        public void Demo() {
            Console.WriteLine(this.Display());
        }
    }
}
