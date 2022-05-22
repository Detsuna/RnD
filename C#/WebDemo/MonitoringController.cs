using System;
using System.Web.Http;
using static System.Net.WebRequestMethods;

namespace WebDemo {
    public partial class MonitoringController : ApiController {
        [Route("Monitoring/ServerDatetime")]
        [AcceptVerbs(Http.Get, Http.Post)]
        public Object ServerDatetime() {
            return new { timestamp = DateTimeOffset.Now };
        }
    }
}
