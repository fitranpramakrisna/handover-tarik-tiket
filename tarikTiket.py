import requests
import pandas as pd
from datetime import datetime
from date_convert import date_eng_to_indo

url = 'https://servant-be.ilcs.co.id/ticket/service_now/incident/list?page=1&perPage=30&status=openteam'


# Masukkan token Bearer yang diambil dari header Authorization
headers = {
    'Authorization': 'Bearer ZgZcYt8LHmjmDC1QKLN4wbwoTN8NAtVa',
    # ganti auth token nya setiap kali login
    'Auth-Token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjoiMzMwMWNmYTIwN2I1ZWI1NzBiNjJkMTFmNDlmNzc2NTI6MTg3MjUyZTEwODM3NWJhNjM1MjgxMmM3ZjRjNWFmNGQ0MTkxZWU1YTRkY2EwYjQ3MGJhZDIxYWZkZTAxZjM1MDlkNDFmMDAxY2Y3MWM1ZWEwZjUzODUyM2RjNDU5NjIzZTI5MGY4YjQ0YjEzODYxNTk1NTViMzM3ZDY1MWZhODk3NzUwYzQzYzgwNmIwZmQ2NDI4MWRjZDM4NGJjZDA0ODgxNGU4MDQxYjIzMDNkZDgxMjQ4ZDM4MTJlNmNkNDIyZWFiNGNlYzFmNmRkYWVkMzBjMDUxZjg4NmFhYTkyNzRkY2M3MWFkZmU5ZDFhNTk1OTlhN2Y0NzIyNDE3YWQ1M2U5Y2I2Y2VlZmRjNzdkYTU4ZWQ0NjkxMGMyNTQ2NjdjOGRhMmQ5N2Y4NjcxMjI0MGQxYTZlOWQ0OWU5ZDdjZjJkODlhODZhMGQ1ZmQ5ZjQ5OWFmMDI3Njg4YWY5N2ZhMDE1YmZkNWM2M2NkOTE0NDY3YjFhN2QyYmM4Njc4ODQ3Mzk2NjhhZTY2Y2JmNTJlNGJhOTc1YWNlNTVlMDM3ODI4YWNlOWJmYjc1M2U4ZDgwNTk3ZDdkOTNhM2MwZDdjNDk4NjQxY2U5OGM3MzZiYzE1NWZkNWRkOTEyZGMxNWRmNDQwNDczY2ExZTZlMDZjM2U4ZjVlOGUzM2VjZTg3ZGRiMmM2ZGRjYjU5NDYwMWI3ODUzNWZkNjFhNjMwZDI3NGU3ZGY0ZjYzN2U2NTg4YTc3NjFhNTRkMDg2ZjFhYTg4M2FjZTdhYjVhMTc1ZWZlNWY0ZjVmMjc3OTc0ODlhODIwMjJkNzNlNDVlMTc4ZjRmNDk1ODlmNzQ4MWQ5YmRiZjEzYTUxMDgxMzc4NGE5ZjBkNDhmYTI1MGE5MWJlZmViYWVjOTY1MjdmY2NjNzNjMzgwN2Y3MjI0MWJmMWY1N2I4YmY5MTdhMDM1YTE3ODY4OTI5NGJmYmEwNzkwODdhZTVkMDdmMDE4MWQ0YTEzM2NjMmE2YmFjMzk2YmVjZjc1OTBiYzU2Y2YyOTI1MDZmMWNkNDhiZjM1NTc0Mjk3NTFiMjEyMjdjZmU2MmYwMDc2N2RlYzFlZTFjMzk1ODY3NzJhZDJlNTBkNTE4MjA3MjcyNzYwZDc5MmZhNmEwNDUyZThmYzU0M2EzODc2NzBiN2E4MzBmNDc4NTkzYzViMThiNjEyNjA0MjY3ZDAyYjUwZWM2Y2JhYmFmOTI4ZjdlZmY0YjM3YmQ0ZWY5YjQ4ZTE4YTk5ZWE3MGE0YzNkMzhiMzJkYjc4ZDAxMmY5NzQ3NjA4YTE1ZjBiNjg1YjE5MTRiMDQxYTY3OTBlZDQ5NGIxMjYyYjg5Nzc4ODhhNWUxZGU1NDMwNTFlMWY3M2ZhNGYwYWY5ZGNjMTY5ZTljOWQzYTJkZmVlOWZlYjdkNDk2NjQzZjNmMDA5M2IzNTI0NGFlNmI0OGQ1MTg3ZDZmMDMxNDQ2M2FlYzFmMDI2MzliN2QwYzMzMjZhNjczMTUyNWQyZjY3OWY4NTJmMTNiZjQ3ZTg1ZmJhZmFlYThmNWUzODNlZWNhYjZiOTFhNDRmMmUwN2FjYzQwMTUxMTg1NGZhNGQyMDBkZmNmZTQwNThlZGY2OGUxZDliNGMyZmExYmJjNTM1ZmY0MjQ3YjI3MmM1ZjkwM2JmZTYwNmUyYmE3MjZmNzViY2MzZWQyMjE1ZDQ5M2Y0YTYxNmZiYmI5NGI1YjNjZmJjZGIwNzk4OTJmNWJiMzBlN2E3YmZjY2Q4NWMxMzA4NDMzY2ViN2JlZjljMzRjOWQ3ZWY0NTFhYTc0NjVjZTczZGM4NTkxNjk2MjI0ZTNmNzdlN2Q1YzIwMWM1YjAzZWQ0YzE2YmVhOTExYTUzNTllMDk0NWQ3NzgyNWUwZjJjMDQ1ZjUzZmQ0ZjA2M2ZkMjcyM2M0YzdmNzlhMDhmNzk0ZWEzYWJjNzVkZTQ1NmNlMmY4NWNmNjQ2MDU5YWVkMjMwOTc3NDhmMzhkNjQ5NTEzOWZkNWEyM2VmYjE0NjU0NWY2YzAzOWViMDEwNTJmNzFjMjU4ZjA2NzIwYTQ0NjRjMjhlYWVjM2ExNGJiYWJkNDkzZDg3MWRiNTc5ODRlNjM0NGJhMGRhNmRlZTA5ZDkxZjM2MGZiYjhmZWZiYzM1ZDZjYzM0YjYzMGFhODRiZjM4NTk1MTUwM2IxYTlmOTgxMDgyMWQ4ZDUxNTQ2MmJjZDk3MTUyNmMyYTQ0ODQwNzk5ZWY1YjVhMGVkZDg4MzAyMjgzMTI5ZWY4MmE3NmYwZDcxYzY3OWZkYmI4ZmM1M2M2Zjk4MjhjNzM1ZDY2Yjk0ZTY2YjI5NDI2MDVhNmIxOGUwYjZhZjczM2FhYzE5OTc5ZWQ0Y2M4ZjA2ZjU4MDFhNzgxMGUzMjI0NGIyMzRjZjdmZTJhMmI0MDIzZjdmMGU1MmE5YmRhMDcwZDE4MjUzNzE2ZDdhMWEwNGJmODUxMzllYWVjOGNmYjIwODU1YTI2OWQyMDU5N2U0NzEzMTlhNDgwOTAyZTFhNjcwZTc2OGYxYzZhMWViNWU4NGFmMTk1YWViODcyZjAwNGI5MmJiMDM0YjNmZWY0M2YyOTgwNWMyNDRkODRmOWQ2Y2VhOGU4MzMwNGU5MDkxMDRmMmRiYzRhNzI2N2QzMzJmYjlmMDU4MDBlNzY5OGEzODkwNTFjOTRjZmY5M2VkYTFlMTBjZjI3YzBiZTU0ODczM2U1ZDhmNjQ3ZmM3ODdlZWFiZjgwOWMxOWYwNTIyNjhhOWQ4NjE3ZmNhNGE3M2VkZWMwZmY4MGM1MTkwNDBmODlkNDYwOWQ3OGFhNGY3OGQyZWJjZDc2MWM1ZGE5YWMzMDhiMGZmZTJjODUyMTY4ZjU4Y2Q5Mzk5N2E5NWZmY2I3Y2E4NmU0ZTA4ODg5NmJlOGZmMDEzYzY4OWUxNGM1MmRlNmVlYTg2NzE2Y2EyZjMzNjRkNTVkOWZkNTU1OTNlODVlOGEwYzAwZGYxMjc3MmNiZDJlMjM2MTYxYWQzOTJiZjcxOTA3NWVlODQ3NzZkZWQ2ZjMwMjRmMDc0OTZlIiwiaWF0IjoxNzM1OTk2ODk2LCJleHAiOjE3MzYwNDAwOTZ9.pRqirlZeFxgnA2i-vDCRR0iK-5_KOprMrkOvEXws8Ug',
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
        
        day = date_eng_to_indo(current_date.split(',')[0])
        current_date = f"{day},{current_date.split(',')[1]}"
        # print(current_date)

        # Menambahkan header
        output_lines.append(greeting)
        output_lines.append("Izin handover tiket")
        output_lines.append(shift_message)
        output_lines.append(current_date)
        output_lines.append("")
        output_lines.append("Fariz, Inoy, Fitran")
        output_lines.append("")
        output_lines.append("======== HANDOVER CASE ========")
        output_lines.append("")

        for service_offering, group in grouped:
            output_lines.append(service_offering)  # Menambahkan nama service offering
            for _, row in group.iterrows():
                output_lines.append(f"{row['ticket_number']} {row['title']} ({row['status']})")  # Menambahkan tiket

            output_lines.append("")  # Menambahkan baris kosong untuk pemisah

        output_lines.append("CC: ")
        
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