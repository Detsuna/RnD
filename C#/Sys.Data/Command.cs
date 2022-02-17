using System.Text.Json;
using System.Data;
using System.Data.Common;

using System.Text;

namespace Sys.Data {
    public class Command {
        public String CommandText { get; set; } = String.Empty;
    }
    /*public class NotCommand : DbCommand {
        public override String CommandText { get ; set ; }
        public override Int32 CommandTimeout { get; set; }
        protected override DbConnection? DbConnection { get => throw new NotImplementedException(); set => throw new NotImplementedException(); }

        protected override DbParameterCollection DbParameterCollection => throw new NotImplementedException();

        protected override DbTransaction? DbTransaction { get => throw new NotImplementedException(); set => throw new NotImplementedException(); }

        public override void Cancel() {
            throw new NotImplementedException();
        }

        public override Int32 ExecuteNonQuery() {
            throw new NotImplementedException();
        }

        public override Object? ExecuteScalar() {
            throw new NotImplementedException();
        }

        public override void Prepare() {
            throw new NotImplementedException();
        }

        protected override DbParameter CreateDbParameter() {
            throw new NotImplementedException();
        }

        protected override DbDataReader ExecuteDbDataReader(CommandBehavior behavior) {
            throw new NotImplementedException();
        }
    }*/
}