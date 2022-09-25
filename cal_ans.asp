<%@LANGUAGE="VBSCRIPT" CODEPAGE="65001"%>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
</head>
<body>
<center>
<%response.write("<h1 style='text-align:center'>" &"计算结果" & "</h1>")%>

value1=Request.Form("value1")
op=Request.Form("op")
value2=Request.Form("value2")
ansewr=Request.Form("answer")
<%response.write("<h1 style='text-align:center'>" & value1+" "+op+" "+value2+" = " + answer & "</h1>")%>

</center>
</body>
</html>