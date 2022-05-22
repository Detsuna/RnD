<%@ Page Language="C#" AutoEventWireup="true" CodeBehind="PaynowQr.aspx.cs" Inherits="WebDemo.Payment.PaynowQr" %>

<!DOCTYPE html>

<html xmlns="http://www.w3.org/1999/xhtml">
<head runat="server">
    <title></title>
</head>
<body>
        <form runat="server">
            <asp:ScriptManager ID="ScriptManager" runat="server"></asp:ScriptManager>
            <!-- server dt -->
            <asp:Timer ID="refresh" runat="server" OnTick="ReloadQR" Interval="60000" />
            <asp:UpdatePanel runat="server" UpdateMode="Conditional">
                <Triggers>
                    <asp:AsyncPostBackTrigger ControlID="refresh" />
                </Triggers>
                <ContentTemplate>
                    <asp:Image ID="ImageQR" runat="server" style="width:8.1cm;height:8.1cm;" />
                </ContentTemplate>
            </asp:UpdatePanel>
        </form>
</body>
</html>
