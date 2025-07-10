import csv
from datetime import datetime

PAKET_FILE = 'kelas c/paket.csv'
TRANSAKSI_FILE = 'kelas c/transaksi.csv'
ADMIN_PIN = '12345'

# ========== UTILITAS ==========

def load_paket():
    try:
        with open(PAKET_FILE, mode='r') as file:
            reader = csv.DictReader(file)
            return list(reader)
    except FileNotFoundError:
        return []

def save_paket(pakets):
    with open(PAKET_FILE, mode='w', newline='') as file:
        fieldnames = ['ID', 'Provider', 'Paket', 'Harga']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(pakets)

# ========== FITUR ADMIN ==========

def tampilkan_paket():
    pakets = load_paket()
    if not pakets:
        print("Belum ada data paket.")
        return
    print("\n=== Daftar Paket Internet ===")
    for p in pakets:
        print(f"{p['ID']}. {p['Provider']} - {p['Paket']} - Rp{p['Harga']}")

def tambah_paket():
    pakets = load_paket()
    new_id = str(int(pakets[-1]['ID']) + 1) if pakets else '1'
    provider = input("Provider: ")
    paket = input("Nama Paket (kuota + masa aktif): ")
    harga = input("Harga: ")
    pakets.append({'ID': new_id, 'Provider': provider, 'Paket': paket, 'Harga': harga})
    save_paket(pakets)
    print("✅ Paket berhasil ditambahkan.")

def edit_paket():
    pakets = load_paket()
    tampilkan_paket()
    id_edit = input("Masukkan ID paket yang ingin diedit: ")
    for p in pakets:
        if p['ID'] == id_edit:
            p['Provider'] = input("Provider baru: ")
            p['Paket'] = input("Nama paket baru: ")
            p['Harga'] = input("Harga baru: ")
            save_paket(pakets)
            print("✅ Paket berhasil diubah.")
            return
    print("❌ ID tidak ditemukan.")

def hapus_paket():
    pakets = load_paket()
    tampilkan_paket()
    id_hapus = input("Masukkan ID paket yang ingin dihapus: ")
    pakets_baru = [p for p in pakets if p['ID'] != id_hapus]
    if len(pakets_baru) < len(pakets):
        save_paket(pakets_baru)
        print("✅ Paket berhasil dihapus.")
    else:
        print("❌ ID tidak ditemukan.")

def lihat_transaksi():
    print("\n=== Riwayat Transaksi ===")
    try:
        with open(TRANSAKSI_FILE, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                print(" | ".join(row))
    except FileNotFoundError:
        print("Belum ada transaksi.")

# ========== FITUR PEMBELI ==========

def beli_paket():
    pakets = load_paket()
    tampilkan_paket()
    id_pilih = input("Pilih ID Paket: ")
    jumlah = int(input("Jumlah beli: "))
    id_pembeli = input("ID Pembeli (No HP): ")
    waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for p in pakets:
        if p['ID'] == id_pilih:
            total = int(p['Harga']) * jumlah
            data = [id_pembeli, p['Provider'], p['Paket'], str(jumlah), p['Harga'], str(total), waktu]
            with open(TRANSAKSI_FILE, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(data)
            print(f"✅ Transaksi berhasil. Total: Rp{total:,}")
            return
    print("❌ Paket tidak ditemukan.")

# ========== MENU ADMIN ==========

def menu_admin():
    while True:
        print("\n=== MENU ADMIN ===")
        print("1. Lihat Daftar Paket")
        print("2. Tambah Paket")
        print("3. Edit Paket")
        print("4. Hapus Paket")
        print("5. Lihat Transaksi")
        print("0. Logout")
        pilih = input("Pilih menu: ")
        if pilih == "1":
            tampilkan_paket()
        elif pilih == "2":
            tambah_paket()
        elif pilih == "3":
            edit_paket()
        elif pilih == "4":
            hapus_paket()
        elif pilih == "5":
            lihat_transaksi()
        elif pilih == "0":
            break
        else:
            print("❌ Pilihan tidak valid.")

# ========== MENU PEMBELI ==========

def menu_pembeli():
    while True:
        print("\n=== MENU PEMBELI ===")
        print("1. Lihat Paket")
        print("2. Beli Paket")
        print("0. Kembali")
        pilih = input("Pilih menu: ")
        if pilih == "1":
            tampilkan_paket()
        elif pilih == "2":
            beli_paket()
        elif pilih == "0":
            break
        else:
            print("❌ Pilihan tidak valid.")

# ========== MENU UTAMA ==========

def main():
    while True:
        print("\n=== APLIKASI PAKET INTERNET ===")
        print("1. Masuk sebagai Admin")
        print("2. Masuk sebagai Pembeli")
        print("0. Keluar")
        role = input("Pilih: ")
        if role == "1":
            pin = input("Masukkan PIN Admin: ")
            if pin == ADMIN_PIN:
                menu_admin()
            else:
                print("❌ PIN salah.")
        elif role == "2":
            menu_pembeli()
        elif role == "0":
            print("Terima kasih!")
            break
        else:
            print("❌ Pilihan tidak valid.")

if __name__ == "__main__":
    main()
