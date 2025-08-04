#/ backend/app/scanner.py
import socket

def run_scan():
    target = "127.0.0.1"  # 你可以改为其他目标或从前端传入
    ports = [22, 80, 443, 3306, 5432]
    results = []

    for port in ports:
        s = socket.socket()
        s.settimeout(0.5)
        try:
            s.connect((target, port))
            results.append({"port": port, "status": "open"})
        except (socket.timeout, ConnectionRefusedError):
            results.append({"port": port, "status": "closed"})
        except Exception as e:
            results.append({"port": port, "status": f"error: {str(e)}"})
        finally:
            s.close()

    return results
