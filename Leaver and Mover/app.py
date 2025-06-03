# from flask import Flask, render_template, request, jsonify
# from datetime import datetime, timedelta
# import psycopg2
# import os
# import smtplib
# from email.mime.text import MIMEText
# import csv
# import io

# app = Flask(__name__)


# conn = psycopg2.connect(
#     host="localhost",
#     database="MoverLeaver",
#     user="postgres",
#     password="Ayush.685"
# )

# # Database configuration
# DB_HOST = os.getenv('DB_HOST', 'localhost')
# DB_NAME = os.getenv('DB_NAME', 'hr_transition')
# DB_USER = os.getenv('DB_USER', 'postgres')
# DB_PASSWORD = os.getenv('DB_PASSWORD', 'Ayush.685')

# # Email configuration
# SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.example.com')
# SMTP_PORT = os.getenv('SMTP_PORT', 587)
# EMAIL_USER = os.getenv('EMAIL_USER', 'hr@company.com')
# EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD', 'email_password')
# EMAIL_FROM = os.getenv('EMAIL_FROM', 'HR System <hr@company.com>')

# def get_db_connection():
#     return psycopg2.connect(
#         host=DB_HOST,
#         database=DB_NAME,
#         user=DB_USER,
#         password=DB_PASSWORD
#     )

# @app.route('/')
# def index():
#     return render_template('index.html')

# # @app.route('/dashboard_data')
# # def dashboard_data():
# #     conn = get_db_connection()
# #     cur = conn.cursor()
    
# #     # Get counts
# #     cur.execute("SELECT COUNT(*) FROM employees WHERE status = 'Moving'")
# #     movers = cur.fetchone()[0]
    
# #     cur.execute("SELECT COUNT(*) FROM employees WHERE status = 'Leaving'")
# #     leavers = cur.fetchone()[0]
    
# #     cur.execute("SELECT COUNT(*) FROM documents WHERE status = 'Pending'")
# #     pending_docs = cur.fetchone()[0]
    
# #     # Pending approvals - documents that need reassignment
# #     cur.execute("""
# #         SELECT COUNT(*) 
# #         FROM documents d
# #         JOIN employees e ON d.approver_email = e.employee_email
# #         WHERE e.status IN ('Moving', 'Leaving') AND d.status = 'Pending'
# #     """)
# #     pending_approvals = cur.fetchone()[0]
    
# #     # Recent activity (simplified for demo)
# #     activities = [
# #         {
# #             "icon": "fas fa-user-check",
# #             "title": "John Smith transitioned to new role",
# #             "details": "Employee ID: E-10245 | Department: Marketing",
# #             "time": "2 hours ago"
# #         },
# #         {
# #             "icon": "fas fa-file-upload",
# #             "title": "New document uploaded",
# #             "details": "Invoice #INV-2023-087 | Amount: $12,500",
# #             "time": "5 hours ago"
# #         },
# #         {
# #             "icon": "fas fa-envelope",
# #             "title": "Reassignment request sent",
# #             "details": "To: Michael Brown | Document: PO-2023-451",
# #             "time": "Yesterday, 3:45 PM"
# #         },
# #         {
# #             "icon": "fas fa-user-minus",
# #             "title": "Employee exit processed",
# #             "details": "Lisa Anderson | Last day: June 30, 2023",
# #             "time": "June 10, 2023"
# #         }
# #     ]
    
# #     cur.close()
# #     conn.close()
    
# #     return jsonify({
# #         "movers": movers,
# #         "leavers": leavers,
# #         "pending_docs": pending_docs,
# #         "pending_approvals": pending_approvals,
# #         "activities": activities
# #     })

# # @app.route('/employees')
# # def get_employees():
# #     conn = get_db_connection()
# #     cur = conn.cursor()
# #     cur.execute("SELECT * FROM employees ORDER BY transition_date")
# #     employees = cur.fetchall()
# #     cur.close()
# #     conn.close()
    
# #     # Convert to list of dictionaries
# #     result = []
# #     for emp in employees:
# #         result.append({
# #             "id": emp[0],
# #             "employee_id": emp[1],
# #             "manager_id": emp[2],
# #             "employee_name": emp[3],
# #             "manager_name": emp[4],
# #             "employee_email": emp[5],
# #             "manager_email": emp[6],
# #             "status": emp[7],
# #             "transition_date": emp[8].strftime('%Y-%m-%d')
# #         })
    
# #     return jsonify(result)

# # @app.route('/add_employee', methods=['POST'])
# # def add_employee():
# #     data = request.json
# #     try:
# #         conn = get_db_connection()
# #         cur = conn.cursor()
# #         cur.execute(
# #             "INSERT INTO employees (employee_id, manager_id, employee_name, manager_name, "
# #             "employee_email, manager_email, status, transition_date) "
# #             "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
# #             (
# #                 data['employee_id'],
# #                 data['manager_id'],
# #                 data['employee_name'],
# #                 data['manager_name'],
# #                 data['employee_email'],
# #                 data['manager_email'],
# #                 data['status'],
# #                 data['transition_date']
# #             )
# #         )
# #         conn.commit()
# #         cur.close()
# #         conn.close()
# #         return jsonify({"success": True})
# #     except Exception as e:
# #         return jsonify({"success": False, "error": str(e)}), 400

# # @app.route('/upload_employees', methods=['POST'])
# # def upload_employees():
# #     if 'file' not in request.files:
# #         return jsonify({"success": False, "error": "No file part"}), 400
    
# #     file = request.files['file']
# #     if file.filename == '':
# #         return jsonify({"success": False, "error": "No selected file"}), 400
    
# #     if not file.filename.endswith('.csv'):
# #         return jsonify({"success": False, "error": "File must be a CSV"}), 400
    
# #     try:
# #         stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
# #         csv_reader = csv.reader(stream)
# #         next(csv_reader)  # Skip header if exists
        
# #         conn = get_db_connection()
# #         cur = conn.cursor()
        
# #         for row in csv_reader:
# #             if len(row) != 8:
# #                 continue
                
# #             cur.execute(
# #                 "INSERT INTO employees (employee_id, manager_id, employee_name, manager_name, "
# #                 "employee_email, manager_email, status, transition_date) "
# #                 "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
# #                 (row[0], row[3], row[1], row[4], row[2], row[5], row[6], row[7])
# #             )
        
# #         conn.commit()
# #         cur.close()
# #         conn.close()
        
# #         return jsonify({"success": True})
# #     except Exception as e:
# #         return jsonify({"success": False, "error": str(e)}), 500

# # @app.route('/employee/<int:id>')
# # def get_employee(id):
# #     conn = get_db_connection()
# #     cur = conn.cursor()
# #     cur.execute("SELECT * FROM employees WHERE id = %s", (id,))
# #     employee = cur.fetchone()
# #     cur.close()
# #     conn.close()
    
# #     if employee:
# #         return jsonify({
# #             "id": employee[0],
# #             "employee_id": employee[1],
# #             "manager_id": employee[2],
# #             "employee_name": employee[3],
# #             "manager_name": employee[4],
# #             "employee_email": employee[5],
# #             "manager_email": employee[6],
# #             "status": employee[7],
# #             "transition_date": employee[8].strftime('%Y-%m-%d')
# #         })
# #     else:
# #         return jsonify({"error": "Employee not found"}), 404

# # @app.route('/delete_employee/<int:id>', methods=['DELETE'])
# # def delete_employee(id):
# #     try:
# #         conn = get_db_connection()
# #         cur = conn.cursor()
# #         cur.execute("DELETE FROM employees WHERE id = %s", (id,))
# #         conn.commit()
# #         cur.close()
# #         conn.close()
# #         return jsonify({"success": True})
# #     except Exception as e:
# #         return jsonify({"success": False, "error": str(e)}), 500

# # @app.route('/documents')
# # def get_documents():
# #     conn = get_db_connection()
# #     cur = conn.cursor()
# #     cur.execute("select t.*,m.line_manager2, m.line_manager3, m.line_manager4 from systemschema.documents t inner join systemschema.hr_data m on t.employee_id = m.employee_id")
# #     documents = cur.fetchall()
# #     cur.close()
# #     conn.close()
    
# #     result = []
# #     for doc in documents:
# #         result.append({
# #             "id": doc[0],
# #             "document_number": doc[1],
# #             "document_type": doc[2],
# #             "approver_name": doc[3],
# #             "approver_email": doc[4],
# #             "status": doc[5],
# #             "manager1": doc[6],
# #             "manager2": doc[7],
# #             "manager3": doc[8],
# #             "manager4": doc[9],
# #             "created_at": doc[10].strftime('%Y-%m-%d')
# #         })
    
# #     return jsonify(result)

# # @app.route('/add_document', methods=['POST'])
# # def add_document():
# #     data = request.json
# #     try:
# #         conn = get_db_connection()
# #         cur = conn.cursor()
        
# #         # Insert document
# #         cur.execute(
# #             "INSERT INTO documents (document_number, document_type, approver_name, "
# #             "approver_email, status, manager1, manager2, manager3, manager4) "
# #             "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
# #             (
# #                 data['doc_number'],
# #                 data['doc_type'],
# #                 data['approver_name'],
# #                 data['approver_email'],
# #                 data.get('doc_status', 'Pending'),
# #                 data.get('manager1', None),
# #                 data.get('manager2', None),
# #                 data.get('manager3', None),
# #                 data.get('manager4', None)
# #             )
# #         )
        
# #         # Check if approver is moving/leaving
# #         cur.execute(
# #             "SELECT status, transition_date, manager_name, manager_email "
# #             "FROM employees "
# #             "WHERE employee_email = %s AND status IN ('Moving', 'Leaving')",
# #             (data['approver_email'],)
# #         )
# #         approver = cur.fetchone()
        
# #         conn.commit()
# #         cur.close()
# #         conn.close()
        
# #         response = {"success": True}
        
# #         if approver:
# #             # Approver is moving/leaving - send notification
# #             send_reassignment_email(
# #                 data['doc_number'],
# #                 data['approver_name'],
# #                 approver[0],  # status
# #                 approver[1].strftime('%Y-%m-%d'),  # transition_date
# #                 approver[2],  # manager_name
# #                 approver[3]   # manager_email
# #             )
# #             response["check_needed"] = True
# #             response["manager_name"] = approver[2]
# #             response["manager_email"] = approver[3]
# #             response["status"] = approver[0]
# #             response["transition_date"] = approver[1].strftime('%Y-%m-%d')
        
# #         return jsonify(response)
# #     except Exception as e:
# #         return jsonify({"success": False, "error": str(e)}), 400

# # @app.route('/document/<int:id>')
# # def get_document(id):
# #     conn = get_db_connection()
# #     cur = conn.cursor()
# #     cur.execute("SELECT * FROM documents WHERE id = %s", (id,))
# #     document = cur.fetchone()
# #     cur.close()
# #     conn.close()
    
# #     if document:
# #         return jsonify({
# #             "id": document[0],
# #             "document_number": document[1],
# #             "document_type": document[2],
# #             "approver_name": document[3],
# #             "approver_email": document[4],
# #             "status": document[5],
# #             "manager1": document[6],
# #             "manager2": document[7],
# #             "manager3": document[8],
# #             "manager4": document[9],
# #             "created_at": document[10].strftime('%Y-%m-%d')
# #         })
# #     else:
# #         return jsonify({"error": "Document not found"}), 404

# # @app.route('/delete_document/<int:id>', methods=['DELETE'])
# # def delete_document(id):
# #     try:
# #         conn = get_db_connection()
# #         cur = conn.cursor()
# #         cur.execute("DELETE FROM documents WHERE id = %s", (id,))
# #         conn.commit()
# #         cur.close()
# #         conn.close()
# #         return jsonify({"success": True})
# #     except Exception as e:
# #         return jsonify({"success": False, "error": str(e)}), 500

# # @app.route('/reassign_approver', methods=['POST'])
# # def reassign_approver():
# #     data = request.json
# #     try:
# #         conn = get_db_connection()
# #         cur = conn.cursor()
        
# #         # Find the first available manager field
# #         cur.execute(
# #             "SELECT manager1, manager2, manager3, manager4 "
# #             "FROM documents "
# #             "WHERE document_number = %s",
# #             (data['doc_number'],)
# #         )
# #         doc = cur.fetchone()
        
# #         if not doc:
# #             return jsonify({"success": False, "error": "Document not found"}), 404
        
# #         # Find the next available manager field
# #         new_manager_field = None
# #         for i in range(1, 5):
# #             if not doc[i]:
# #                 new_manager_field = f"manager{i}"
# #                 break
        
# #         if not new_manager_field:
# #             return jsonify({"success": False, "error": "No available manager fields"}), 400
        
# #         # Update the document
# #         cur.execute(
# #             f"UPDATE documents SET {new_manager_field} = %s, status = 'Reassigned' "
# #             "WHERE document_number = %s",
# #             (data['new_approver'], data['doc_number'])
# #         )
        
# #         conn.commit()
# #         cur.close()
# #         conn.close()
        
# #         return jsonify({"success": True})
# #     except Exception as e:
# #         return jsonify({"success": False, "error": str(e)}), 500

# # @app.route('/reports_data')
# # def reports_data():
# #     conn = get_db_connection()
# #     cur = conn.cursor()
    
# #     # Employee status counts
# #     cur.execute("SELECT status, COUNT(*) FROM employees GROUP BY status")
# #     status_counts = {}
# #     for row in cur.fetchall():
# #         status_counts[row[0]] = row[1]
    
# #     # Document type counts
# #     cur.execute("SELECT document_type, COUNT(*) FROM documents GROUP BY document_type")
# #     doc_types = []
# #     for row in cur.fetchall():
# #         doc_types.append({
# #             "type": row[0],
# #             "count": row[1]
# #         })
    
# #     cur.close()
# #     conn.close()
    
# #     return jsonify({
# #         "movers": status_counts.get('Moving', 0),
# #         "leavers": status_counts.get('Leaving', 0),
# #         "doc_types": doc_types
# #     })

# # @app.route('/alerts')
# # def get_alerts():
# #     # In a real system, this would query the database for alerts
# #     # For demo, return some sample data
# #     return jsonify([
# #         {
# #             "id": 1,
# #             "type": "Transition Reminder",
# #             "employee": "Lisa Anderson",
# #             "details": "Employee exit in 5 days - reassign documents",
# #             "due_date": "2023-06-30",
# #             "status": "Pending"
# #         },
# #         {
# #             "id": 2,
# #             "type": "Reassignment Needed",
# #             "employee": "John Smith",
# #             "details": "3 documents pending approval",
# #             "due_date": "2023-07-15",
# #             "status": "Pending"
# #         },
# #         {
# #             "id": 3,
# #             "type": "Transition Completed",
# #             "employee": "Robert Chen",
# #             "details": "All documents reassigned successfully",
# #             "due_date": "2023-06-01",
# #             "status": "Completed"
# #         }
# #     ])

# # @app.route('/resolve_alert/<int:id>', methods=['POST'])
# # def resolve_alert(id):
# #     # In a real system, this would update the alert status in the database
# #     return jsonify({"success": True})

# # def send_reassignment_email(doc_number, approver_name, status, transition_date, manager_name, manager_email):
# #     """Send an email to the manager requesting document reassignment"""
# #     try:
# #         # Create email content
# #         subject = f"Action Required: Document Approver Reassignment - {doc_number}"
        
# #         transition_type = "transition to a new role" if status == "Moving" else "leave the organization"
        
# #         body = f"""
# #         Dear {manager_name},
        
# #         Our records indicate that {approver_name} (current approver for document {doc_number}) 
# #         is scheduled to {transition_type} on {transition_date}.
        
# #         To prevent delays in processing this document, please reassign the approval responsibility 
# #         to another manager by suggesting an alternative approver using the link below:
        
# #         [Reassignment Portal Link]
        
# #         Please complete this reassignment within 2 business days to ensure uninterrupted processing.
        
# #         Thank you,
# #         HR Operations Team
# #         """
        
# #         # Create message
# #         msg = MIMEText(body)
# #         msg['Subject'] = subject
# #         msg['From'] = EMAIL_FROM
# #         msg['To'] = manager_email
        
# #         # Send email
# #         with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
# #             server.starttls()
# #             server.login(EMAIL_USER, EMAIL_PASSWORD)
# #             server.send_message(msg)
            
# #         print(f"Reassignment email sent to {manager_email}")
# #         return True
# #     except Exception as e:
# #         print(f"Failed to send email: {str(e)}")
# #         return False

# # def send_proactive_alerts():
# #     """Send proactive alerts 5 days before an employee's transition/exit"""
# #     try:
# #         conn = get_db_connection()
# #         cur = conn.cursor()
        
# #         # Calculate date 5 days from now
# #         alert_date = datetime.now() + timedelta(days=5)
        
# #         # Find employees transitioning in 5 days
# #         cur.execute(
# #             "SELECT employee_name, employee_email, manager_name, manager_email, status, transition_date "
# #             "FROM employees "
# #             "WHERE transition_date = %s AND status IN ('Moving', 'Leaving')",
# #             (alert_date.date(),)
# #         )
# #         employees = cur.fetchall()
        
# #         for emp in employees:
# #             # Send alert to manager
# #             send_reassignment_alert(
# #                 emp[0],  # employee_name
# #                 emp[3],  # managxer_email
# #                 emp[4],  # status
# #                 emp[5].strftime('%Y-%m-%d')  # transition_date
# #             )
        
# #         cur.close()
# #         conn.close()
# #         return True
# #     except Exception as e:
# #         print(f"Error sending proactive alerts: {str(e)}")
# #         return False

# # def send_reassignment_alert(employee_name, manager_email, status, transition_date):
# #     """Send proactive alert to manager"""
# #     try:
# #         # Create email content
# #         subject = f"Proactive Alert: Upcoming Transition - {employee_name}"
        
# #         transition_type = "role transition" if status == "Moving" else "organizational exit"
        
# #         body = f"""
# #         Dear Manager,
        
# #         This is a proactive reminder that {employee_name} is scheduled for a {transition_type} 
# #         on {transition_date} (5 days from now).
        
# #         Please review and reassign any pending documents requiring {employee_name}'s approval 
# #         using the HR Transition System:
        
# #         [System Link]
        
# #         Taking action now will help prevent any process delays.
        
# #         Thank you,
# #         HR Operations Team
# #         """
        
# #         # Create message
# #         msg = MIMEText(body)
# #         msg['Subject'] = subject
# #         msg['From'] = EMAIL_FROM
# #         msg['To'] = manager_email
        
# #         # Send email
# #         with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
# #             server.starttls()
# #             server.login(EMAIL_USER, EMAIL_PASSWORD)
# #             server.send_message(msg)
            
# #         print(f"Proactive alert sent to {manager_email}")
# #         return True
# #     except Exception as e:
# #         print(f"Failed to send proactive alert: {str(e)}")
# #         return False

# # if __name__ == '__main__':
# #     app.run(debug=True)

f = ['carol.davis@example.com', 'ivy.lee@example.com', 'ivy.taylor@example.com', 'eve.taylor@example.com']

for i in f:
    print(i)