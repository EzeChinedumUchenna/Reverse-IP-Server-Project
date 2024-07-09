from http.server import BaseHTTPRequestHandler, HTTPServer
import mysql.connector
import os

def create_table(conn):
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INT AUTO_INCREMENT PRIMARY KEY,
            original_ip VARCHAR(255) NOT NULL,
            reversed_ip VARCHAR(255) NOT NULL
        )
    ''')
    conn.commit()

def get_client_ip(request_handler):
    client_ip = request_handler.headers.get('X-Forwarded-For')
    if not client_ip:
        client_ip = request_handler.client_address[0]
    return client_ip

def get_database_connection():
    #db_host = os.getenv('DB_HOST', 'db')
    #db_user = os.getenv('DB_USER', 'root')
    #db_password = os.getenv('DB_PASSWORD', 'root')
    #db_name = os.getenv('DB_NAME', 'ip_logs_db')

    #print(f"DB_HOST: {db_host}")
    #print(f"DB_USER: {db_user}")
    #print(f"DB_PASSWORD: {db_password}")
    #print(f"DB_NAME: {db_name}")

    conn = mysql.connector.connect(
        host='db',
        user='root',
        password='root',
        database='ip_logs_db',
        port=3306
    )
    return conn

def initialize_database():
    conn = get_database_connection()
    create_table(conn)
    conn.close()

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            client_ip = get_client_ip(self)
            reversed_ip = '.'.join(reversed(client_ip.split('.')))
            log_to_database(client_ip, reversed_ip)
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(reversed_ip.encode('utf-8'))
            print(f"Logged reversed IP: {reversed_ip} (Original IP: {client_ip})")
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            error_message = f"Error: {str(e)}"
            self.wfile.write(error_message.encode('utf-8'))
            print(error_message)

def log_to_database(original_ip, reversed_ip):
    conn = get_database_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO logs (original_ip, reversed_ip)
        VALUES (%s, %s)
    ''', (original_ip, reversed_ip))
    conn.commit()
    conn.close()

def run(server_class=HTTPServer, handler_class=RequestHandler, port=8080):
    server_address = ('0.0.0.0', port)  # Bind to 0.0.0.0 to be accessible from outside the container
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd server on port {port}...')
    httpd.serve_forever()

if __name__ == "__main__":
    initialize_database()
    run()
