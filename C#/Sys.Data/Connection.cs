using Microsoft.Data.Sqlite;
using System;
using System.Collections.Generic;
using System.Data;
using System.Data.Common;
using System.Data.SqlClient;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Sys.Data {
    public class Connection{
    }
    //public class sqliteConnection : SqliteConnection { public SqlConnection sql = null; }
    /*public class NotConnection : DbConnection {
        public override string ConnectionString { get; set; } = String.Empty;

        public override string Database { get; } = String.Empty;

        public override string DataSource { get; } = String.Empty;

        public override string ServerVersion { get; } = String.Empty;

        public override ConnectionState State { get; } = ConnectionState.Closed;

        public override void ChangeDatabase(string databaseName) {
            throw new NotImplementedException();
        }

        public override void Close() {
            throw new NotImplementedException();
        }

        public override void Open() {
            throw new NotImplementedException();
        }

        protected override DbTransaction BeginDbTransaction(IsolationLevel isolationLevel) {
            throw new NotImplementedException();
        }

        protected override DbCommand CreateDbCommand() {
            throw new NotImplementedException();
        }
    }*/
}