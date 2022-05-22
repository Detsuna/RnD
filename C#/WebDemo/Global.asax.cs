using Swashbuckle.Application;
using System;
using System.IO;
using System.Reflection;
using System.Web.Http;
using Microsoft.AspNet.FriendlyUrls;
using System.Web.Routing;

namespace WebDemo {
    public class Global : System.Web.HttpApplication {
        public static DateTimeOffset compiled { get; set; } = File.GetLastWriteTime(Assembly.GetExecutingAssembly().Location);

        protected void Application_Start(object sender, EventArgs e) {
            GlobalConfiguration.Configure(this.WebApi);
            this.WebForms(RouteTable.Routes);
        }
        protected void Session_Start(object sender, EventArgs e) { }
        protected void Application_BeginRequest(object sender, EventArgs e) { }
        protected void Application_AuthenticateRequest(object sender, EventArgs e) { }
        protected void Application_Error(object sender, EventArgs e) { }
        protected void Session_End(object sender, EventArgs e) { }
        protected void Application_End(object sender, EventArgs e) { }

        private void WebApi(HttpConfiguration httpConfig) {
            httpConfig.Formatters.Remove(httpConfig.Formatters.XmlFormatter);
            httpConfig.MapHttpAttributeRoutes();
            httpConfig.EnableSwagger(/*"{apiVersion}",*/ delegate (SwaggerDocsConfig c) {
                c.SingleApiVersion(compiled.ToString("d-MMM-yyyy"), "Demo");
                c.PrettyPrint();
            }).EnableSwaggerUi();
            httpConfig.Routes.MapHttpRoute(
                 name: "Swagger UI",
                 routeTemplate: "",
                 defaults: null,
                 constraints: null,
                 handler: new RedirectHandler(SwaggerDocsConfig.DefaultRootUrlResolver, "swagger/ui/index")
            );
        }
        private void WebForms(RouteCollection routes) {
            //routes.MapPageRoute("About", "Home/About-WDI", "~/About.aspx");
            routes.EnableFriendlyUrls(new FriendlyUrlSettings() { AutoRedirectMode = RedirectMode.Permanent });
        }
    }
}