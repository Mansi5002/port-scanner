import socket
import threading
import tkinter as tk
from tkinter import ttk, filedialog

# Simple service names
PORT_SERVICES = {
    21: 'FTP', 22: 'SSH', 80: 'HTTP',
    443: 'HTTPS', 3306: 'MySQL', 8080: 'HTTP-Alt'
}

class PortScannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Port Scanner Tool")

        self.running = False
        self.results = []

        # UI
        tk.Label(root, text="Target IP / Host").pack()
        self.target = tk.Entry(root)
        self.target.pack()

        tk.Label(root, text="Start Port").pack()
        self.start = tk.Entry(root)
        self.start.insert(0, "1")
        self.start.pack()

        tk.Label(root, text="End Port").pack()
        self.end = tk.Entry(root)
        self.end.insert(0, "100")
        self.end.pack()

        tk.Button(root, text="Start Scan", command=self.start_scan).pack()
        tk.Button(root, text="Stop", command=self.stop_scan).pack()

        self.progress = ttk.Progressbar(root, length=300)
        self.progress.pack()

        self.output = tk.Text(root, height=15)
        self.output.pack()

        tk.Button(root, text="Save Results", command=self.save_results).pack()

    def scan_port(self, host, port):
        if not self.running:
            return

        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.5)
            result = s.connect_ex((host, port))

            if result == 0:
                service = PORT_SERVICES.get(port, "Unknown")
                self.results.append((port, service))
                self.output.insert(tk.END, f"Port {port} ({service}) OPEN\n")

            s.close()
        except:
            pass

    def run_scan(self, host, start, end):
        total = end - start + 1
        count = 0

        for port in range(start, end + 1):
            if not self.running:
                break

            threading.Thread(target=self.scan_port, args=(host, port)).start()

            count += 1
            self.progress["value"] = (count / total) * 100

        self.running = False
        self.output.insert(tk.END, "\nScan Finished\n")
        self.output.insert(tk.END, f"Total Open Ports: {len(self.results)}\n")

    def start_scan(self):
        host = self.target.get()
        start = int(self.start.get())
        end = int(self.end.get())

        self.output.delete(1.0, tk.END)
        self.results.clear()

        self.running = True

        threading.Thread(target=self.run_scan, args=(host, start, end)).start()

    def stop_scan(self):
        self.running = False

    def save_results(self):
        file = filedialog.asksaveasfile(defaultextension=".txt")
        if file:
            for port, service in self.results:
                file.write(f"Port {port} ({service}) OPEN\n")
            file.close()


root = tk.Tk()
app = PortScannerApp(root)
root.mainloop()