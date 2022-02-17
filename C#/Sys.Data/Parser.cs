using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Sys.Data {
    public class Parser {
        public String Text { get; }
        public Parser(String text) { this.Text = text; }

        public void Parse() {
            String[] queries = Text.Split(";");
        }
    }
}
