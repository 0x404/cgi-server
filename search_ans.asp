<%@LANGUAGE="VBSCRIPT" CODEPAGE="65001"%>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
</head>
<body>
<%response.write("<h1 style='text-align:center'>" &"查询结果" & "</h1>")%>

<%
set conn=Server.CreateObject("ADODB.Connection")
conn.Provider="Microsoft.Jet.OLEDB.4.0"
conn.Open(Server.Mappath("./student.mdb"))
conn.Execute sql
%>

<%
ID=Request.Form("ID")

set rs = Server.CreateObject("ADODB.recordset")
sql="SELECT s_name, s_class FROM student WHERE s_id == '" & ID & "' ORDER by s_class desc"
rs.Open sql, conn
%>
<table border="1" width="100%" bgcolor="#d2e7b2" style="text-align:center">
<tr>
<th bgcolor='#bcce8a2'>姓名</th>
<th bgcolor='#bcce8a2'>班级</th>
</tr>
<%do until rs.EOF%>
<tr>
<%for each x6 in rs.Fields%>
<td><%Response.Write(x6.value)%></td>
<%next
rs.MoveNext%>
</tr>
<%loop
rs.close
%>


</table>
<%Response.Write("<p style='text-align:center'><a href='/dataquery' title='返回查询界面'>返回查询界面</a></p>")%>

</body>
</html>