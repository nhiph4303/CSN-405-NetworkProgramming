import tkinter as tk
from tkinter import filedialog, messagebox
import hashlib
import socket

# ==========================================
# [LOGIC ĐỀ BÀI: CÁC HÀM XỬ LÝ SỰ KIỆN]
# ==========================================
def select_file():
    # Mở hộp thoại chọn file
    filepath = filedialog.askopenfilename(title="Select a text file")
    if filepath:
        # Cập nhật đường dẫn vào ô File Path
        file_path_entry.delete(0, tk.END)
        file_path_entry.insert(0, filepath)
        
        try:
            # Mở file và đọc nội dung
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            # Xóa nội dung cũ trong Text box và chèn nội dung mới
            content_text.delete(1.0, tk.END)
            content_text.insert(tk.END, content)
        except Exception as e:
            messagebox.showerror("Error", f"Không thể đọc file: {e}")

def integrity_check():
    # 1. Lấy thông tin IP và Port từ giao diện
    ip = ip_entry.get().strip()
    try:
        port = int(port_entry.get().strip())
    except ValueError:
        messagebox.showerror("Error", "Port phải là một số nguyên!")
        return
        
    # 2. Lấy nội dung cần mã hóa từ khung Text
    content = content_text.get(1.0, tk.END).strip()
    if not content:
        messagebox.showwarning("Warning", "Không có nội dung để mã hóa!")
        return
        
    # 3. YÊU CẦU ĐỀ BÀI: Băm nội dung bằng thuật toán SHA-256 (Giống Lab 8)
    file_hash = hashlib.sha256(content.encode('utf-8')).hexdigest()
    
    # 4. Giao tiếp với Server qua Socket TCP (Giống Lab 7)
    client_socket = socket.socket(socket.AF_INET, socket.socket.SOCK_STREAM)
    try:
        # Kết nối tới Server
        client_socket.connect((ip, port))
        
        # Gửi mã băm lên Server
        client_socket.sendall(file_hash.encode('utf-8'))
        
        # Nhận kết quả từ Server trả về
        response = client_socket.recv(1024).decode('utf-8')
        
        # Cập nhật kết quả vào ô Result
        result_entry.delete(0, tk.END)
        result_entry.insert(0, response)
        
        # Hiển thị Popup báo cáo
        messagebox.showinfo("Result", f"Server response: {response}\nYour Hash: {file_hash}")
        
    except Exception as e:
        messagebox.showerror("Connection Error", f"Không thể kết nối Server: {e}")
    finally:
        client_socket.close()

# ==========================================
# [SƯỜN BẮT BUỘC: VẼ GIAO DIỆN TKINTER CƠ BẢN]
# ==========================================
root = tk.Tk()
root.title("Integrity Checking")
root.geometry("550x350")
root.resizable(False, False)

# Tạo khung (Frame) bao ngoài
frame = tk.LabelFrame(root, text="Client Side", padx=15, pady=15)
frame.pack(padx=10, pady=10, fill="both", expand=True)

# Hàng 1: Server IP và Port
tk.Label(frame, text="Server IP:").grid(row=0, column=0, sticky="w", pady=5)
ip_entry = tk.Entry(frame, width=20)
ip_entry.insert(0, "127.0.0.1")
ip_entry.grid(row=0, column=1, sticky="w", pady=5)

tk.Label(frame, text="Port:").grid(row=0, column=2, sticky="e", pady=5, padx=10)
port_entry = tk.Entry(frame, width=10)
port_entry.insert(0, "30000")
port_entry.grid(row=0, column=3, sticky="w", pady=5)

# Hàng 2: Chọn File
select_btn = tk.Button(frame, text="Select File", command=select_file)
select_btn.grid(row=1, column=0, pady=10, sticky="w")

file_path_entry = tk.Entry(frame, width=45)
file_path_entry.grid(row=1, column=1, columnspan=3, pady=10, sticky="w")

# Hàng 3: Result và Nút Integrity Check
tk.Label(frame, text="Result:").grid(row=2, column=1, sticky="e", pady=5, padx=5)
result_entry = tk.Entry(frame, width=15)
result_entry.grid(row=2, column=2, sticky="w", pady=5)

check_btn = tk.Button(frame, text="Integrity Check", command=integrity_check)
check_btn.grid(row=2, column=3, pady=5, sticky="e")

# Hàng 4: Khung nội dung
tk.Label(frame, text="Content:").grid(row=3, column=0, sticky="nw", pady=5)
content_text = tk.Text(frame, height=8, width=55)
content_text.grid(row=4, column=0, columnspan=4, pady=5)

# Bắt đầu vòng lặp đồ họa
root.mainloop()
