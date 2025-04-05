
from flask import Flask, render_template_string, request, send_file
from colorama import init, Fore, Style
import time
import sys
import tkinter as tk
from io import BytesIO
import pdfkit

init(autoreset=True)
app = Flask(__name__)

FORM_TEMPLATE = """
<!DOCTYPE html>
<html lang='ar' dir='rtl'>
<head>
    <meta charset='UTF-8'>
    <title>kader11000 OSINT</title>
    <link href='https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.rtl.min.css' rel='stylesheet'>
</head>
<body class='bg-dark text-white'>
<div class='container mt-5'>
    <h1 class='text-center mb-4'>kader11000 OSINT Tool</h1>
    <form method='post'>
        <div class='mb-3'>
            <label for='domain' class='form-label'>Enter the domain:</label>
            <input type='text' class='form-control' id='domain' name='domain' required>
        </div>
        <button type='submit' class='btn btn-primary'>Start Scan</button>
    </form>
</div>
</body>
</html>
"""

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang='ar' dir='rtl'>
<head>
    <meta charset='UTF-8'>
    <title>نتائج الفحص</title>
    <link href='https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.rtl.min.css' rel='stylesheet'>
    <script>
        window.onload = function() {
            alert("Scan completed successfully!\nThanks for using kader11000");
        }
    </script>
</head>
<body class='bg-dark text-white'>
<div class='container mt-5'>
    <h2 class='mb-4 text-center'>Scan results for {{ domain }}</h2>
    <ul class='list-group mb-4'>
        <li class='list-group-item bg-secondary text-white'>Possible IP: {{ ip }}</li>
        <li class='list-group-item bg-secondary text-white'>Additional Information: {{ info }}</li>
    </ul>
    <form action='/download' method='post'>
        <input type='hidden' name='domain' value='{{ domain }}'>
        <input type='hidden' name='ip' value='{{ ip }}'>
        <input type='hidden' name='info' value='{{ info }}'>
        <button type='submit' class='btn btn-success'>Download Report PDF</button>
    </form>
</div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        domain = request.form['domain']
        ip = "192.0.2.1"
        info = "معلومات OSINT وهمية"
        return render_template_string(HTML_TEMPLATE, domain=domain, ip=ip, info=info)
    return render_template_string(FORM_TEMPLATE)

@app.route('/download', methods=['POST'])
def download():
    domain = request.form['domain']
    ip = request.form['ip']
    info = request.form['info']
    rendered = render_template_string(HTML_TEMPLATE, domain=domain, ip=ip, info=info)
    pdf = pdfkit.from_string(rendered, False)
    return send_file(BytesIO(pdf), download_name=f"{domain}_report.pdf", as_attachment=True)

def print_banner():
    banner = """
    ██╗  ██╗ █████╗ ██████╗ ███████╗██████╗     ██╗███╗   ██╗██╗ ██████╗  █████╗ 
    ██║ ██╔╝██╔══██╗██╔══██╗██╔════╝██╔══██╗    ██║████╗  ██║██║██╔════╝ ██╔══██╗
    █████╔╝ ███████║██████╔╝█████╗  ██████╔╝    ██║██╔██╗ ██║██║██║  ███╗███████║
    ██╔═██╗ ██╔══██║██╔═══╝ ██╔══╝  ██╔═══╝     ██║██║╚██╗██║██║██║   ██║██╔══██║
    ██║  ██╗██║  ██║██║     ███████╗██║         ██║██║ ╚████║██║╚██████╔╝██║  ██║
    ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚══════╝╚═╝         ╚═╝╚═╝  ╚═══╝╚═╝ ╚═════╝ ╚═╝  ╚═╝

             kader11000 OSINT Tool - Terminal Mode Activated
    """
    print(Fore.CYAN + Style.BRIGHT + banner)

def fake_loading():
    print(Fore.YELLOW + Style.BRIGHT + "\n[+] Starting the server...", end='')
    for _ in range(5):
        sys.stdout.write(Fore.YELLOW + '.')
        sys.stdout.flush()
        time.sleep(0.5)
    print(Fore.GREEN + " Started!\n")

def show_gui_mode_selector():
    selected_mode = {"mode": "127.0.0.1"}
    def start_server():
        window.destroy()
    def select_local():
        selected_mode["mode"] = "127.0.0.1"
        start_server()
    def select_network():
        selected_mode["mode"] = "0.0.0.0"
        start_server()
    window = tk.Tk()
    window.title("Start kader11000 Server")
    window.geometry("300x180")
    window.resizable(False, False)
    tk.Label(window, text="Select server mode:", font=("Arial", 12)).pack(pady=20)
    tk.Button(window, text="Local (127.0.0.1)", command=select_local, width=25).pack(pady=5)
    tk.Button(window, text="Full Network (0.0.0.0)", command=select_network, width=25).pack(pady=5)
    window.mainloop()
    return selected_mode["mode"]

if __name__ == '__main__':
    print_banner()
    fake_loading()
    host = show_gui_mode_selector()
    print(Fore.GREEN + f"\n[+] Server is now running on: http://{host}:5000")
    app.run(host=host, port=5000, debug=True)
