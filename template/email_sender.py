import json
from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class emailmsg:
    def __init__(self, subject, file_name, host, port, user, password):
        self.subject = subject
        self.file_name = file_name
        self.email_host = host
        self.email_port = port
        self.smtp_user = user
        self.smtp_password = password

    def email_send(self):
        connection = SMTP(host=self.email_host, port=self.email_port)
        connection.login(self.smtp_user, self.smtp_password)
        msg = MIMEMultipart()
        msg["Subject"] = self.subject
        msg["From"] = "test@mailer.xyz"

        msg.attach(MIMEText("This is auto generated mail."))

        # Send table format HTML data
        file_data = json.load(open(self.file_name,"r"))
        data = """<!DOCTYPE html>
                    <html>
                    <head>
                        <meta charset="utf-8" />
                        <style type="text/css">
                        table {
                            background: white;
                            border-radius:3px;
                            border-collapse: collapse;
                            height: auto;
                            max-width: 900px;
                            padding:5px;
                            width: 100%;
                            animation: float 5s infinite;
                        }
                        th {
                            border-bottom: 4px solid #9ea7af;
                            border-left: 1px solid #C1C3D1;
                            font-size:14px;
                            font-weight: 300;
                            padding:10px;
                            text-align:center;
                            vertical-align:middle;
                        }
                        tr {
                            border-top: 1px solid #C1C3D1;
                            border-bottom: 1px solid #C1C3D1;
                            border-left: 1px solid #C1C3D1;
                            font-size:16px;
                            font-weight:normal;
                        }
                        tr:hover td {
                            background:#4E5066;
                            color:#FFFFFF;
                            border-top: 1px solid #22262e;
                        }
                        td {
                            background:#FFFFFF;
                            padding:10px;
                            text-align:left;
                            vertical-align:middle;
                            font-weight:300;
                            font-size:13px;
                            border-right: 1px solid #C1C3D1;
                        }
                        </style>
                    </head>
                    <body>
                    <h4> This is auto generated mail.</h4>
                        <table>
                        <thead>
                            <tr style="border: 1px solid #1b1e24;">
                            <th>Key</th>
                            <th>Field 1</th>
                            <th>Field 2</th>
                            <th>Field 3</th>
                            <th>Field 4</th>
                            </tr>
                        </thead> 
                        <tbody>
                            <tr>"""

        for key,value in file_data.items():
            # Extract key to be kept at first column
            data = data + '<tr><td>' + key + '</td>'
            for key2, value2 in value.items():
                data = data + '<td>' + str(value2) + '</td>'
            # End that sepecific row
            data = data + '</tr>'
        
        # last html tags to be added
        html_tag = """
                    </table>
                    <br>
                    </body>
                    </html>
                    """
        data = data + html_tag


        msg.attach(MIMEText(data, "html"))
        connection.sendmail(
            "from_addr",
            "to_addrs",
            msg.as_string(),
        )