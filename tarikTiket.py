import requests
import pandas as pd
from datetime import datetime

url = 'https://servant-be.ilcs.co.id/ticket/service_now/list?page=1&perPage=30&status=openteam&search='

# Masukkan token Bearer yang diambil dari header Authorization
headers = {
    'Authorization': 'Bearer ZgZcYt8LHmjmDC1QKLN4wbwoTN8NAtVa',
    'Auth-Token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1dWlkIjoiODA3ODgyNTEtZmUyZi00M2Y4LTlhNDktMGY0OTJmMDNmMzA5IiwidXNlcm5hbWUiOiJuaWNob2xhcyIsIm5hbWUiOiJOaWNob2xhcyBDaHJpc3Rob2ZlciIsImVtYWlsIjoibmljaG9sYXMuY2hyaXN0aG9mZXJAaWxjcy5jby5pZCIsIm5pcHAiOiIxMTAwMjc3MyIsImluaXRpYWxzX25hbWUiOiJOQ1MiLCJzdGF0dXMiOjEsImFjdGl2ZSI6MSwiaXNsZWFkIjowLCJyb2xlX2lkIjoxLCJyb2xlX25hbWUiOiJMMS9MMiBPcHMiLCJmYXZlb190ZWFtaWQiOjUsInNlcnZpY2Vub3dfZ3JvdXBpZCI6IltcIjRmNTBlYzg5NDc2MmMyOTA0MTVmNzU2OTExNmQ0MzQxXCJdIiwic3dhZ19pZCI6IjYyODIyOTczNDk5MzItMTYzNTY0OTI0NyIsImlzX3JvbGVoaWRlIjpmYWxzZSwiaWF0IjoxNzI1NzE0NzAxLCJleHAiOjE3MjU3NTc5MDF9.ORq_8ZmXDnx7SThHBv2-rjj0pidR5RjdzJZVt_jgeT0',
    'Content-Type': 'application/json'
}

try:
    # Mengirim permintaan GET
    response = requests.get(url, headers=headers)
    
    # Memeriksa status kode respon
    response.raise_for_status()  # Menghasilkan pengecualian untuk status kode tidak berhasil

    data = response.json()
    
    # Debugging: Cetak data JSON untuk melihat strukturnya
    print(data)  # Menampilkan struktur JSON
    
    # Memastikan data yang diterima adalah list
    if 'message' in data and 'data' in data['message'] and isinstance(data['message']['data'], list):
        # Mengonversi data menjadi DataFrame dan mengambil kolom yang diinginkan
        df = pd.json_normalize(data['message']['data'])[['ticket_number', 'service_offering', 'title', 'status']]
        
        # Memotong karakter pada kolom 'title' agar maksimal 50 karakter dan menambahkan '...'
        df['title'] = df['title'].apply(lambda x: x[:50] + '...' if isinstance(x, str) and len(x) > 50 else x)
        
        # Mengubah format ticket_number menjadi [nomortiket]
        df['ticket_number'] = df['ticket_number'].apply(lambda x: f"[{x}]" if isinstance(x, str) else x)

        # Mengelompokkan berdasarkan service_offering dengan modifikasi untuk IBS
        df['service_offering'] = df['service_offering'].apply(lambda x: 'IBS' if 'IBS' in x else x)

        
        # Mengelompokkan berdasarkan service_offering
        grouped = df.groupby('service_offering')

        # Menyiapkan format output
        output_lines = []
        
        # Menentukan salam berdasarkan waktu
        current_hour = datetime.now().hour
        if current_hour < 12:
            greeting = "Selamat Pagi, rekan-rekan semua"
            shift_message = "Handover ke shift Pagi"
        else:
            greeting = "Selamat Malam, rekan-rekan semua"
            shift_message = "Handover ke shift Malam"


        # Mengambil tanggal saat ini
        current_date = datetime.now().strftime("%A, %d %B %Y")

        # Menambahkan header
        output_lines.append(greeting)
        output_lines.append("Izin handover tiket")
        output_lines.append(shift_message)
        output_lines.append(current_date)
        output_lines.append("")
        output_lines.append("Fitran, Nicho, Sony")
        output_lines.append("")
        output_lines.append("======== HANDOVER CASE ========")
        output_lines.append("")

        for service_offering, group in grouped:
            output_lines.append(service_offering)  # Menambahkan nama service offering
            for _, row in group.iterrows():
                output_lines.append(f"{row['ticket_number']} {row['title']} ({row['status']})")  # Menambahkan tiket

            output_lines.append("")  # Menambahkan baris kosong untuk pemisah

        # Menyimpan hasil output ke dalam file text
        output_filename = f"formatted_output_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write("\n".join(output_lines))
        
        print(f"Data berhasil disimpan ke dalam file: {output_filename}")
    else:
        print("Data tidak dalam format list yang diharapkan.")
except requests.exceptions.HTTPError as http_err:
    print(f'HTTP error occurred: {http_err}')  # Menampilkan kesalahan HTTP
except Exception as err:
    print(f'An error occurred: {err}')  # Menangani kesalahan lainnya