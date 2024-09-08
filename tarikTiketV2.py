import requests
import pandas as pd
from datetime import datetime, timedelta

# URL dan header yang diperlukan
url = 'https://servant-be.ilcs.co.id/ticket/service_now/list?page=1&perPage=30&status=openteam&search='

# Token yang diambil dari header Authorization
headers = {
    'Authorization': 'Bearer ZgZcYt8LHmjmDC1QKLN4wbwoTN8NAtVa',
    'Auth-Token': 'your_auth_token',  # Masukkan Auth-Token Anda
    'Content-Type': 'application/json'
}

# Variabel untuk menyimpan token dan waktu kedaluwarsa
access_token = 'your_initial_access_token'
refresh_token = 'your_initial_refresh_token'
token_expiration = datetime.now() + timedelta(minutes=60)  # Misalkan token valid selama 60 menit

def refresh_access_token():
    global access_token, refresh_token, token_expiration
    refresh_url = 'https://your-auth-server.com/refresh'  # URL untuk refresh token
    data = {
        'refresh_token': refresh_token,
        'grant_type': 'refresh_token'
    }

    try:
        response = requests.post(refresh_url, json=data)
        response.raise_for_status()  # Memeriksa apakah permintaan berhasil
        tokens = response.json()

        # Memperbarui access token dan refresh token
        access_token = tokens.get('access_token')
        refresh_token = tokens.get('refresh_token', refresh_token)  # Hanya perbarui jika ada
        token_expiration = datetime.now() + timedelta(minutes=60)  # Perbarui waktu kedaluwarsa

        print("Access token berhasil diperbarui.")
    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP error occurred during token refresh: {http_err}')
    except Exception as err:
        print(f'An error occurred during token refresh: {err}')

def is_token_expired():
    return datetime.now() >= token_expiration

try:
    # Periksa apakah token perlu diperbarui
    if is_token_expired():
        refresh_access_token()

    # Perbarui header dengan access token yang valid
    headers['Authorization'] = f'Bearer {access_token}'

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
        
        # Mengelompokkan berdasarkan service_offering
        grouped = df.groupby('service_offering')

        # Menyiapkan format output
        output_lines = []
        
        # Menentukan salam berdasarkan waktu
        current_hour = datetime.now().hour
        if current_hour < 12:
            greeting = "Selamat Pagi, rekan-rekan semua"
        else:
            greeting = "Selamat Malam, rekan-rekan semua"

        # Mengambil tanggal saat ini
        current_date = datetime.now().strftime("%A, %d %B %Y")

        # Menambahkan header
        output_lines.append(greeting)
        output_lines.append("Izin handover tiket")
        output_lines.append("Handover ke shift Malam")
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
