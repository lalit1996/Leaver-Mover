from flask import Flask, render_template, jsonify,request
import psycopg2
from flask_mail import Mail, Message
import pandas as pd
app = Flask(__name__)


# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'chiranjivikr.1996@gmail.com'
app.config['MAIL_PASSWORD'] = 'hfiv yohc uhgr syhk'
app.config['MAIL_DEFAULT_SENDER'] = 'chiranjivikr.1996@gmail.com'

mail = Mail(app)

def get_db_connection():
    return psycopg2.connect(
        host="localhost",
        database="MoverLeaver",
        user="postgres",
        password="Ayush.685"
    )

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/documents')
def get_documents():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''select t.*,m.current_manager_email,m.case_status from systemschema.documents t inner join 
(
SELECT 
CASE 
        WHEN line_manager4 IS NOT NULL THEN line_manager4
        WHEN line_manager3 IS NOT NULL THEN line_manager3
        WHEN line_manager2 IS NOT NULL THEN line_manager2
        WHEN line_manager_email IS NOT NULL THEN line_manager_email
        ELSE NULL
    END AS current_manager_email,
    * 
FROM systemschema.hr_data) as m on t.employee_id = m.employee_id''')
    rows = cur.fetchall()
    columns = [desc[0] for desc in cur.description]
    cur.close()
    conn.close()
    data = [dict(zip(columns, row)) for row in rows]
    return jsonify(data)






@app.route('/send-email', methods=['POST'])
def send_manager_email():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''select t.*,m.current_manager_email from systemschema.documents t inner join 
(
SELECT 
CASE 
        WHEN line_manager4 IS NOT NULL THEN line_manager4
        WHEN line_manager3 IS NOT NULL THEN line_manager3
        WHEN line_manager2 IS NOT NULL THEN line_manager2
        WHEN line_manager_email IS NOT NULL THEN line_manager_email
        ELSE NULL
    END AS current_manager_email,
    * 
FROM systemschema.hr_data) as m on t.employee_id = m.employee_id''')
    rows = cur.fetchall()
    columns = [desc[0] for desc in cur.description]
    cur.close()
    conn.close()
    data = [dict(zip(columns, row)) for row in rows]
    data1 = pd.DataFrame(data)
    data2 = data1['current_manager_email']
    data2 = list(data2)
    data2 = list(set(data2))
    
    print(data2)
    for current_manager in data2:
        print(current_manager)
        data3 = data1[data1['current_manager_email']==current_manager]
        table_html = data3.to_html(index=False, border=0, classes='styled-table')
        html_body = f"""
        <html>
        <head>
        <style>
        .styled-table {{
            border-collapse: collapse;
            width: 100%;
            font-family: Arial, sans-serif;
        }}
        .styled-table th, .styled-table td {{
            border: 1px solid #007BFF;
            padding: 8px;
            text-align: left;
        }}
        .styled-table th {{
            background-color: #007BFF;
            color: white;
        }}
        </style>
        </head>
        <body>
        <p>Dear Manager,</p>
        <p>Here is your item report:</p>
        {table_html}
        <p>Regards,<br>HR System</p>
        </body>
        </html>
        """
        message = Message(
        subject="Your Assigned Items",
        recipients=[current_manager],
        body=f"Dear Manager,\n\n please find the below detail ",
        html=html_body)
        mail.send(message)
    return jsonify({"status": "success", "message": "Email sent successfully"})



@app.route('/hr-data')
def get_employee():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''select * from systemschema.hr_data''')
    rows = cur.fetchall()
    columns = [desc[0] for desc in cur.description]
    cur.close()
    conn.close()
    data = [dict(zip(columns, row)) for row in rows]
    return jsonify(data)


@app.route('/record-count')
def record_count():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("select count(*) from systemschema.hr_data where case_status = 'leaver'")
    moving_count = cur.fetchone()[0]
    cur.execute("select count(*) from systemschema.hr_data where case_status = 'mover'")
    leaving_count = cur.fetchone()[0]
    cur.execute("select count(t.*) from systemschema.documents t inner join systemschema.hr_data m on t.employee_id = m.employee_id")
    pending_doc = cur.fetchone()[0]
    cur.execute("select count(t.*) from systemschema.documents t inner join systemschema.hr_data m on t.employee_id = m.employee_id where t.type='Purchase Order'")
    Po_pending_count = cur.fetchone()[0]
    cur.execute("select count(t.*) from systemschema.documents t inner join systemschema.hr_data m on t.employee_id = m.employee_id where t.type='Invoice'")
    invoice_pending_count = cur.fetchone()[0]
    cur.execute("select count(t.*) from systemschema.documents t inner join systemschema.hr_data m on t.employee_id = m.employee_id where t.type='Requisition'")
    Requisition_pending_count = cur.fetchone()[0]
    cur.close()
    conn.close()
    return jsonify({'moving_count': moving_count, 'leaving_count':leaving_count,'pending_doc':pending_doc,'Po_pending_count':Po_pending_count,'invoice_pending_count':invoice_pending_count,'Requisition_pending_count':Requisition_pending_count})





@app.route('/update_employee/<int:employee_id>', methods=['POST'])
def update_employee(employee_id):
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE systemschema.hr_data
        SET 
            employee_name = %s,
            line_manager_email = %s,
            line_manager2 = %s,
            line_manager3 = %s,
            line_manager4 = %s,
            case_status = %s
        WHERE id = %s
    """, (
        data['employee_name'], data['line_manager_email'], data['line_manager2'],
        data['line_manager3'], data['line_manager4'], data['case_status'], employee_id
    ))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'Employee updated successfully'})









if __name__ == '__main__':
    app.run(debug=True)


