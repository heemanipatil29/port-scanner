import socket
from flask import send_file
from reportlab.pdfgen import canvas
from flask import Flask,request,Response

latest_report = ""
app = Flask(__name__)
@app.route("/", methods=["GET", "POST"])
def home():
    return """
    <html>
    <title>PORT SCANNER</title>
    <head>
    <body style="background: url('/static/portscanner.jpg') center/cover no-repeat;">
    <p style="color:#FFFFFF; font-size:70px; font-family:'times new roman';text-align:center">Port Scanner</p>
    <form action="/page2" method="POST">
    <p style="color:#FFFFFF; text-align:left; font-size:35;">Enter IP Address:
    <input type="text" name="ip" placeholder="Enter IP Address" style="width:300px; height:35px;"></p>
    <a href="/page2"><button type="submit" style="width:180px; height:60px; font-size:25px; color:black; background-color:#00C853;">NEXT</button></a></form>
     </body></head></html>
     """
@app.route("/page2", methods=["GET", "POST"])
def page2():
    ip = request.form.get("ip")
    return f"""

    <html>
    <body style="background: url('/static/portscanner.jpg') center/cover no-repeat;">
    <p style="color:#FFFFFF; font-size:50px; font-family:'times new roman';text-align:left;"> Start Port & End Port</p>
    <form action="/page3" method="POST">
    <input type="hidden" name="ip" value="{ip}">
    <p style="color:#FFFFFF; text-align:left; font-size:35;">Enter Start Port:
    <input type="number" name="start_port" style="width:250px; height:30px;"></p>
    <p style="color:#FFFFFF; text-align:left; font-size:35;">Enter End Port:
    <input type="number" name="end_port" style="width:250px; height:30px;"></p>
    <button type="submit" style="width:180px; height:60px; font-size:25px; color:black; background-color:#00C853;">SCAN</button></form>
    </body>
    </html>
    """
@app.route("/page3", methods=["GET", "POST"])
def page3():
    ip = request.form.get("ip")

    start_port = request.form.get("start_port")
    end_port = request.form.get("end_port")

    if not start_port or not end_port:
        return "Please enter Start Port and End Port"

    start_port = int(start_port)
    end_port = int(end_port)
    service = {21: "FTP", 22: "SSH", 25: "SMTP", 53: "DNS", 80: "HTTP", 110: "POP3", 143: "IMAP", 443: "HTTPS", 3306: "MYSQL", 8080: "HTTP-ALT"}
    table_rows = ""

    global latest_report
    latest_report = "Port Scan Report\n\n"

    for port in service.keys():
        
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        result = s.connect_ex((ip, port))
        if result == 0:
            status =("open")
            status_color = "#22C55E"
        else:
            status = ("close")
            status_color = "#EF4444"
        service_name = service.get(port, "unknown")
        latest_report += (
            f"Port: {port} | "
            f"Status: {status} | "
            f"Service: {service_name}\n"
        )

        s.close()
        table_rows += f"""
        <tr>
        <td style="background-color:#2563EB; color:white; text-align:center; font-weight:bold;">{port}</td>
        <td style="background-color:{status_color}; color:white; text-align:center; font-weight:bold;">{status}</td>
        <td style="background-color:#7C3AED; color:white; text-align:center; font-weight:bold;">{service_name}</td> 
        </tr>
        """
    return f"""
    <html>
    <body style="background: url('/static/portscanner.jpg') center/cover no-repeat;">
    <table border="1" style="margin:auto; border-collapse:collapse; width:20%; background-color:#000000; color:#00FF00;">
    <tr>
    <th>Port Number</th>
    <th>Status</th>
    <th>Service</th>
    </tr>
    
    {table_rows}
    </table><br><br>
    <a href="/download"><button style="width:220px; height:60px; font_size:22px; background-color:#16A34A; color:white; border-radius:10px;">Download Report</button></a>
    </body></html>
    """
@app.route("/download")
def download():
    pdf_file = "port_scan_report.pdf"

    c = canvas.Canvas(pdf_file)


    y = 760
    for line in latest_report.split("\n"):
        c.drawString(50, y, line)
        y -= 20

    c.save()

    return send_file(pdf_file, as_attachment=True)
app.run(debug=True)