import tkinter as tk
from tkinter import ttk, messagebox
import csv, os

# =============================
# 1️⃣ Lớp Phòng trọ
# =============================
class PhongTro:
    def __init__(self, ma_phong, ten_phong, gia_thue, trang_thai="Trống"):
        self.ma_phong = ma_phong
        self.ten_phong = ten_phong
        self.gia_thue = gia_thue
        self.trang_thai = trang_thai

    def xem_thong_tin(self):
        return f"Mã phòng: {self.ma_phong}\nTên phòng: {self.ten_phong}\nGiá thuê: {self.gia_thue}\nTrạng thái: {self.trang_thai}"

    def cap_nhat_thong_tin(self, ten_phong=None, gia_thue=None, trang_thai=None):
        if ten_phong:
            self.ten_phong = ten_phong
        if gia_thue:
            self.gia_thue = gia_thue
        if trang_thai:
            self.trang_thai = trang_thai


# =============================
# 2️⃣ Lớp Quản lý phòng trọ
# =============================
class QuanLyPhongTro:
    FILE_CSV = "danh_sach_phong.csv"

    def __init__(self):
        self.ds_phong = []
        self.tao_file_csv_neu_chua_co()
        self.doc_file_csv()

    def tao_file_csv_neu_chua_co(self):
        if not os.path.exists(self.FILE_CSV):
            with open(self.FILE_CSV, "w", encoding="utf-8", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["Mã phòng", "Tên phòng", "Giá thuê", "Trạng thái"])

    def ghi_file_csv(self):
        with open(self.FILE_CSV, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Mã phòng", "Tên phòng", "Giá thuê", "Trạng thái"])
            for p in self.ds_phong:
                writer.writerow([p.ma_phong, p.ten_phong, p.gia_thue, p.trang_thai])

    def doc_file_csv(self):
        try:
            with open(self.FILE_CSV, mode="r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    phong = PhongTro(
                        ma_phong=row["Mã phòng"],
                        ten_phong=row["Tên phòng"],
                        gia_thue=float(row["Giá thuê"]),
                        trang_thai=row["Trạng thái"]
                    )
                    self.ds_phong.append(phong)
        except Exception as e:
            print("⚠️ Lỗi đọc file CSV:", e)

    def them_phong(self, phong):
        for p in self.ds_phong:
            if p.ma_phong == phong.ma_phong:
                return False
        self.ds_phong.append(phong)
        self.ghi_file_csv()
        return True

    def tim_phong(self, ma_phong):
        for p in self.ds_phong:
            if p.ma_phong == ma_phong:
                return p
        return None

    def xoa_phong(self, ma_phong):
        phong = self.tim_phong(ma_phong)
        if phong:
            self.ds_phong.remove(phong)
            self.ghi_file_csv()
            return True
        return False

    def cap_nhat_phong(self, ma_phong, ten_phong=None, gia_thue=None, trang_thai=None):
        phong = self.tim_phong(ma_phong)
        if phong:
            phong.cap_nhat_thong_tin(ten_phong, gia_thue, trang_thai)
            self.ghi_file_csv()
            return True
        return False

    def lay_ds_phong(self):
        return self.ds_phong


# =============================
# 3️⃣ Giao diện Tkinter
# =============================
class QuanLyPhongTroUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🏠 Quản Lý Phòng Trọ")
        self.root.geometry("900x650")
        self.root.configure(bg="#f3f3f3")

        self.ql = QuanLyPhongTro()
        self.menu_open = False
        self.menu_x = -200
        self.active_menu = None  # menu đang được chọn
        self.build_ui()

    def build_ui(self):
        # === THANH TIÊU ĐỀ + MENU ===
        menu_frame = tk.Frame(self.root, bg="#1565C0", height=50)
        menu_frame.pack(fill="x", side="top")

        # Nút ba gạch ☰ (màu sáng hơn nền)
        self.menu_button = tk.Button(menu_frame, text="☰", font=("Segoe UI", 16, "bold"),
                                     bg="#42A5F5", fg="white", bd=0, activebackground="#1E88E5",
                                     command=self.toggle_menu)
        self.menu_button.pack(side="left", padx=15, pady=5)

        tk.Label(menu_frame, text="🏠 Quản Lý Phòng Trọ", font=("Segoe UI", 16, "bold"),
                 bg="#1565C0", fg="white").pack(side="left", padx=10)

        # MENU ẨN BÊN TRÁI
        self.side_menu = tk.Frame(self.root, bg="#E0E0E0", width=200, height=650)
        self.side_menu.place(x=self.menu_x, y=50)

        # Các nút menu
        self.menu_buttons = {}

        self.menu_buttons["Trang chủ"] = tk.Button(self.side_menu, text="🏡 Trang chủ",
                                                   font=("Segoe UI", 12), bg="#E0E0E0",
                                                   bd=0, anchor="w",
                                                   command=lambda: self.chon_menu("Trang chủ"))
        self.menu_buttons["Trang chủ"].pack(fill="x", pady=5, padx=10)

        self.menu_buttons["Quản lý phòng trọ"] = tk.Button(self.side_menu, text="🛏️ Quản lý phòng trọ",
                                                           font=("Segoe UI", 12), bg="#1565C0", fg="white",
                                                           bd=0, anchor="w",
                                                           command=lambda: self.chon_menu("Quản lý phòng trọ"))
        self.menu_buttons["Quản lý phòng trọ"].pack(fill="x", pady=5, padx=0)

        self.menu_buttons["Quản lý người thuê"] = tk.Button(self.side_menu, text="👤 Quản lý người thuê",
                                                            font=("Segoe UI", 12), bg="#E0E0E0",
                                                            bd=0, anchor="w",
                                                            command=lambda: self.chon_menu("Quản lý người thuê"))
        self.menu_buttons["Quản lý người thuê"].pack(fill="x", pady=5, padx=0)

        self.menu_buttons["Quản lý hợp đồng"] = tk.Button(self.side_menu, text="📄 Quản lý hợp đồng",
                                                          font=("Segoe UI", 12), bg="#E0E0E0",
                                                          bd=0, anchor="w",
                                                          command=lambda: self.chon_menu("Quản lý hợp đồng"))
        self.menu_buttons["Quản lý hợp đồng"].pack(fill="x", pady=5, padx=0)

        # === KHUNG NHẬP THÔNG TIN ===
        frame_input = tk.LabelFrame(self.root, text="📋 Thông tin phòng", font=("Segoe UI", 12, "bold"),
                                    bg="#ffffff", padx=15, pady=10, labelanchor="n", fg="#444")
        frame_input.pack(fill="x", padx=30, pady=15)

        tk.Label(frame_input, text="Mã phòng:", font=("Segoe UI", 11), bg="white").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        tk.Label(frame_input, text="Tên phòng:", font=("Segoe UI", 11), bg="white").grid(row=0, column=2, padx=10, pady=5, sticky="e")
        tk.Label(frame_input, text="Giá thuê:", font=("Segoe UI", 11), bg="white").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        tk.Label(frame_input, text="Trạng thái:", font=("Segoe UI", 11), bg="white").grid(row=1, column=2, padx=10, pady=5, sticky="e")

        self.ma_phong_var = tk.StringVar()
        self.ten_phong_var = tk.StringVar()
        self.gia_thue_var = tk.StringVar()
        self.trang_thai_var = tk.StringVar(value="Trống")

        tk.Entry(frame_input, textvariable=self.ma_phong_var, font=("Segoe UI", 11), width=15).grid(row=0, column=1, padx=10)
        tk.Entry(frame_input, textvariable=self.ten_phong_var, font=("Segoe UI", 11), width=20).grid(row=0, column=3, padx=10)
        tk.Entry(frame_input, textvariable=self.gia_thue_var, font=("Segoe UI", 11), width=15).grid(row=1, column=1, padx=10)
        ttk.Combobox(frame_input, textvariable=self.trang_thai_var,
                     values=["Trống", "Đang thuê", "Bảo trì"],
                     font=("Segoe UI", 11), width=17, state="readonly").grid(row=1, column=3, padx=10)

        # === NÚT CHỨC NĂNG ===
        frame_btn = tk.Frame(self.root, bg="#f3f3f3")
        frame_btn.pack(pady=10)
        style = {"font": ("Segoe UI", 11, "bold"), "bg": "#1565C0", "fg": "white", "width": 15, "height": 1}
        tk.Button(frame_btn, text="➕ Thêm phòng", command=self.them_phong, **style).grid(row=0, column=0, padx=10)
        tk.Button(frame_btn, text="🔍 Tìm phòng", command=self.tim_phong, **style).grid(row=0, column=1, padx=10)
        tk.Button(frame_btn, text="📝 Cập nhật", command=self.cap_nhat_phong, **style).grid(row=0, column=2, padx=10)
        tk.Button(frame_btn, text="🗑️ Xóa phòng", command=self.xoa_phong, **style).grid(row=0, column=3, padx=10)
        tk.Button(frame_btn, text="📜 Làm mới", command=self.hien_thi_ds_phong, **style).grid(row=0, column=4, padx=10)

        # === DANH SÁCH PHÒNG ===
        frame_list = tk.LabelFrame(self.root, text="📄 Danh sách phòng trọ", font=("Segoe UI", 12, "bold"),
                                   bg="#ffffff", padx=10, pady=10, labelanchor="n", fg="#444")
        frame_list.pack(fill="both", expand=True, padx=30, pady=10)

        self.tree = ttk.Treeview(frame_list, columns=("Mã phòng", "Tên phòng", "Giá thuê", "Trạng thái"), show="headings", height=10)
        for col in ("Mã phòng", "Tên phòng", "Giá thuê", "Trạng thái"):
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=150, stretch=False)
        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<Button-1>", self.disable_column_resize)
        self.hien_thi_ds_phong()

    # ============================
    # 🚀 Các hàm chức năng
    # ============================
    def chon_menu(self, ten_menu):
        """Đổi màu menu được chọn"""
        for name, btn in self.menu_buttons.items():
            if name == ten_menu:
                btn.configure(bg="#1565C0", fg="white")
            else:
                btn.configure(bg="#E0E0E0", fg="black")

        if ten_menu == "Trang chủ":
            self.thoat_ung_dung()

    def animate_menu(self, target_x):
        """Hiệu ứng trượt menu"""
        step = 20 if target_x > self.menu_x else -20
        if (step > 0 and self.menu_x < target_x) or (step < 0 and self.menu_x > target_x):
            self.menu_x += step
            self.side_menu.place(x=self.menu_x, y=50)
            self.root.after(10, lambda: self.animate_menu(target_x))
        else:
            self.menu_x = target_x
            self.side_menu.place(x=self.menu_x, y=50)
        self.side_menu.lift()

    def toggle_menu(self):
        if self.menu_open:
            self.animate_menu(-200)
            self.menu_open = False
        else:
            self.animate_menu(0)
            self.menu_open = True

    def thoat_ung_dung(self):
        self.root.destroy()

    def them_phong(self):
        ma = self.ma_phong_var.get().strip()
        ten = self.ten_phong_var.get().strip()
        gia = self.gia_thue_var.get().strip()
        tt = self.trang_thai_var.get().strip()
        if not ma or not ten or not gia:
            messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin!")
            return
        try:
            gia = float(gia)
        except ValueError:
            messagebox.showerror("Lỗi", "Giá thuê phải là số!")
            return
        phong = PhongTro(ma, ten, gia, tt)
        if self.ql.them_phong(phong):
            messagebox.showinfo("Thành công", f"Đã thêm phòng {ten}")
            self.hien_thi_ds_phong()
        else:
            messagebox.showwarning("Trùng mã", "Mã phòng đã tồn tại!")

    def tim_phong(self):
        ma = self.ma_phong_var.get().strip()
        phong = self.ql.tim_phong(ma)
        if phong:
            messagebox.showinfo("Thông tin phòng", phong.xem_thong_tin())
        else:
            messagebox.showerror("Không tìm thấy", "Không tồn tại phòng này!")

    def cap_nhat_phong(self):
        ma = self.ma_phong_var.get().strip()
        ten = self.ten_phong_var.get().strip()
        gia = self.gia_thue_var.get().strip()
        tt = self.trang_thai_var.get().strip()
        if not ma:
            messagebox.showerror("Lỗi", "Vui lòng nhập mã phòng cần cập nhật!")
            return
        if gia:
            try:
                gia = float(gia)
            except ValueError:
                messagebox.showerror("Lỗi", "Giá thuê phải là số!")
                return
        if self.ql.cap_nhat_phong(ma, ten_phong=ten or None, gia_thue=gia or None, trang_thai=tt or None):
            messagebox.showinfo("Thành công", "Đã cập nhật thông tin phòng.")
            self.hien_thi_ds_phong()
        else:
            messagebox.showerror("Lỗi", "Không tìm thấy phòng cần cập nhật!")

    def xoa_phong(self):
        ma = self.ma_phong_var.get().strip()
        if not ma:
            messagebox.showwarning("Lỗi", "Vui lòng nhập mã phòng cần xóa!")
            return
        if self.ql.xoa_phong(ma):
            messagebox.showinfo("Đã xóa", f"Đã xóa phòng {ma}")
            self.hien_thi_ds_phong()
        else:
            messagebox.showerror("Lỗi", "Không tìm thấy phòng cần xóa!")

    def hien_thi_ds_phong(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for p in self.ql.lay_ds_phong():
            self.tree.insert("", "end", values=(p.ma_phong, p.ten_phong, p.gia_thue, p.trang_thai))

    def disable_column_resize(self, event):
        region = self.tree.identify_region(event.x, event.y)
        if region == "separator":
            return "break"


if __name__ == "__main__":
    root = tk.Tk()
    app = QuanLyPhongTroUI(root)
    root.mainloop()
