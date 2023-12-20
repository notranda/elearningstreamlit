import streamlit as st
import pandas as pd
import os



# Fungsi untuk menampilkan dashboard E-Learning
def show_dashboard(username):
    st.title("Dashboard E-Learning")

    # Periksa jenis akun (Mahasiswa atau Dosen)
    is_dosen = check_dosen(username)

    # Pilihan halaman
    if is_dosen:
        selected_page = st.sidebar.selectbox("Pilih Halaman", ["Manage Kelas", "Monitoring Progress", "Logout"])
    else:
        selected_page = st.sidebar.selectbox("Pilih Halaman", ["Profile", "Halaman Kelas", "Logout"])

    # Menampilkan halaman yang dipilih
    if selected_page == "Profile" and not is_dosen:
        show_profile()
    elif selected_page == "Logout":
        st.subheader("Logout")
        st.warning("Apakah Anda yakin ingin logout?")
        logout_confirmed = st.button("Logout")

        if logout_confirmed:
            st.session_state.is_logged_in = False
            st.experimental_rerun()
    elif is_dosen:
        if selected_page == "Manage Kelas":
            show_manage_kelas()
        elif selected_page == "Monitoring Progress":
            show_monitoring_progress_nilai()
    else:
        if selected_page == "Halaman Kelas":
            show_kelas()

def check_dosen(username):
    # Logika untuk memeriksa jenis akun (dalam hal ini, jika akun memiliki kata "Dosen" dalam usernamenya)
    return "Dosen" in username

def show_manage_kelas():
    st.title("Manage Kelas")
    st.write("Selamat datang di halaman untuk mengelola kelas sebagai Dosen.")

    # Cek apakah pengguna adalah dosen
    is_dosen = check_dosen(st.session_state.username)

    # Menampilkan halaman "Manage Kelas Dosen" jika pengguna adalah dosen
    if is_dosen:
        selected_class = st.selectbox("Pilih Kelas", ["Algoritma Pemrograman", "Analisis Data Statistika", "Aljabar Linier Elementer"])
        manage_kelas_dosen(selected_class)

def manage_kelas_dosen(selected_class):
    st.title(f"Manage Kelas Dosen - {selected_class}")

    new_materi = st.text_area("Tambah Materi", key=f"materi_{selected_class}")
    tambah_materi_button = st.button("Tambah Materi")

    if "submitted_materi" not in st.session_state:
        st.session_state.submitted_materi = {}

    if selected_class in st.session_state.submitted_materi:
        st.success("Materi berhasil ditambahkan!")

    if tambah_materi_button and new_materi:
        
        st.session_state.submitted_materi[selected_class] = True

        existing_materi = st.session_state.get(f"{selected_class}_materi", "")
        default_materi = set_default_materi().get(selected_class, "")
        new_combined_materi = existing_materi + "\n\n" + new_materi if existing_materi else default_materi + "\n\n" + new_materi
        st.session_state[f"{selected_class}_materi"] = new_combined_materi

        st.success("Materi berhasil ditambahkan!")

def show_monitoring_progress_nilai():
    st.title("Monitoring Progress")

    # Daftar kelas yang dapat dipilih
    selected_class = st.selectbox("Pilih Kelas", ["Algoritma Pemrograman", "Analisis Data Statistika", "Aljabar Linier Elementer"])

    # Menampilkan nilai untuk setiap kelas
    show_class_progress(selected_class)

def show_class_progress(selected_class):
    st.title(f"Progress Nilai - {selected_class}")

    quiz_score_key = f"{selected_class}_quiz_score"
    if quiz_score_key in st.session_state:

        quiz_score = st.session_state[quiz_score_key]

        percentage_score = (quiz_score / 3) * 100

        show_student_info()

        st.success(f"Nilai Kuis: {percentage_score:.2f} dari 100")

    else:
        st.info("Belum ada nilai kuis untuk kelas ini.")

def show_student_info():
    if "student_info" in st.session_state:
        student_info = st.session_state["student_info"]

        st.write(f"Nama Mahasiswa: {student_info['nama']}")
        st.write(f"NIM Mahasiswa: {student_info['nim']}")
    else:
        st.warning("Informasi mahasiswa tidak tersedia.")

def show_profile():
    st.title("Profil Pengguna")
    
    if "user_profile" not in st.session_state:
        st.session_state.user_profile = {
            "nama": "Nama Pengguna",
            "nim": "NIM Pengguna",
            "foto_path": "default_profile_pic.jpg"
        }

    new_name = st.text_input("Masukkan Nama Baru:", value=st.session_state.user_profile["nama"])
    update_name_button = st.button("Ganti Nama")

    new_nim = st.text_input("Masukkan NIM Baru:", value=st.session_state.user_profile["nim"])
    update_nim_button = st.button("Ganti NIM")

    if update_name_button:
        st.session_state.user_profile["nama"] = new_name
        st.success("Nama berhasil diubah!")

    if update_nim_button:
        st.session_state.user_profile["nim"] = new_nim
        st.success("NIM berhasil diubah!")

    # Menampilkan informasi profil yang baru
    st.write(f"Profil Pengguna - {st.session_state.user_profile['nama']}")
    st.write(f"NIM: {st.session_state.user_profile['nim']}")

    # Menampilkan foto profil
    st.image(st.session_state.user_profile["foto_path"], caption="Foto Profil", use_column_width=True)

    # Simpan informasi nama dan NIM ke sesi Streamlit
    st.session_state["student_info"] = {
        "nama": st.session_state.user_profile["nama"],
        "nim": st.session_state.user_profile["nim"]
    }

# Fungsi untuk menampilkan halaman kelas
def show_kelas():
    st.title("Halaman Kelas")
    st.write("Selamat datang di halaman kelas! Pilih salah satu kelas di bawah ini:")

    # Daftar kelas yang dapat dipilih
    selected_class = st.selectbox("Pilih Kelas", ["Algoritma Pemrograman", "Analisis Data Statistika", "Aljabar Linier Elementer"])

    # Subpages di bawah "Halaman Kelas"
    with st.sidebar.subheader(""):
        subpage = st.sidebar.radio("", ["Lihat Materi", "Kuis", "Tugas"])

    if subpage == "Lihat Materi":
        show_materi(selected_class)
    elif subpage == "Kuis":
        show_kuis(selected_class)
    elif subpage == "Tugas":
        show_tugas(selected_class)

# Fungsi untuk menampilkan halaman materi
def show_materi(selected_class):
    st.title(f"Materi - {selected_class}")

    # Cek apakah materi sudah diubah oleh dosen
    materi_dosen = st.session_state.get(f"{selected_class}_materi", "")

    # Cek apakah materi default ada
    default_materi = set_default_materi().get(selected_class, "")

    # Gabungkan materi default dan materi dosen
    materi_mahasiswa = materi_dosen + "\n\n" + default_materi if materi_dosen else default_materi

    st.write(materi_mahasiswa)

# Fungsi untuk menetapkan materi default pada setiap kelas
# Fungsi untuk menetapkan materi default pada setiap kelas
def set_default_materi():
    default_materi = {
        "Algoritma Pemrograman": (
            "Materi Minggu ke-1\n"
            "\nMateri tentang dasar-dasar algoritma pemrograman.\n"
            "Contoh bahasa pemrograman: Python\n"
            "Python adalah bahasa pemrograman tingkat tinggi yang mudah dipelajari dan digunakan.\n"
            "Beberapa fitur Python:\n"
            "- Sintaksis yang bersih dan mudah dibaca.\n"
            "- Berbagai macam library dan framework.\n"
            "- Cocok untuk pengembangan web, analisis data, dan kecerdasan buatan."
        ),
        "Analisis Data Statistika": (
            "Materi Minggu ke-1\n"
            "\nMateri tentang analisis data menggunakan statistika.\n"
            "Statistika adalah ilmu yang mempelajari cara mengumpulkan, menganalisis, dan menafsirkan data.\n"
            "Beberapa konsep dalam statistika:\n"
            "- Mean, median, dan modus.\n"
            "- Distribusi probabilitas.\n"
            "- Uji hipotesis."
        ),
        "Aljabar Linier Elementer": (
            "Materi Minggu ke-1\n"
            "\nMateri tentang aljabar linier elementer.\n"
            "Aljabar linier elementer mempelajari matriks, vektor, dan operasi-operasi terkait.\n"
            "Beberapa konsep dalam aljabar linier elementer:\n"
            "- Sistem persamaan linear.\n"
            "- Transformasi matriks.\n"
            "- Ruang vektor dan subruang."
        ),
    }

    return default_materi

# Fungsi untuk menampilkan halaman Materi di sidebar
def show_materi(selected_class):
    st.title(f"Materi - {selected_class}")

    # Cek apakah materi sudah diubah oleh dosen
    if f"{selected_class}_materi" in st.session_state:
        materi_mahasiswa = st.session_state[f"{selected_class}_materi"]
    else:
        # Jika belum diubah, gunakan materi default
        default_materi = set_default_materi()
        materi_mahasiswa = default_materi.get(selected_class, "Materi belum tersedia.")

    st.write(materi_mahasiswa)

# Fungsi untuk menampilkan halaman kuis
def show_kuis(selected_class):
    st.title(f"Kuis {selected_class}")
    st.write(f"Selamat datang di kuis untuk kelas {selected_class}.")

    # Pertanyaan kuis (contoh)
    if selected_class == "Algoritma Pemrograman":
        questions = [
            {
                'question': 'Apa itu Python?',
                'options': ['Bahasa pemrograman', 'Nama ular', 'Nama batu'],
                'correct_option': 'Bahasa pemrograman'
            },
            {
                'question': 'Apa kegunaan Python?',
                'options': ['Pengembangan web', 'Analisis data', 'Kecerdasan buatan', 'Semua jawaban benar'],
                'correct_option': 'Semua jawaban benar'
            },
            {
                'question': 'Siapa penemu Python?',
                'options': ['Guido van Rossum', 'Bill Gates', 'Mark Zuckerberg'],
                'correct_option': 'Guido van Rossum'
            },
            # Tambahkan pertanyaan baru
            # ...
        ]

    elif selected_class == "Analisis Data Statistika":
        questions = [
            {
                'question': 'Apa itu mean?',
                'options': ['Nilai tengah', 'Jumlah data dibagi jumlah observasi', 'Modus'],
                'correct_option': 'Jumlah data dibagi jumlah observasi'
            },
            {
                'question': 'Apa yang diukur oleh distribusi probabilitas?',
                'options': ['Kemungkinan kejadian', 'Rerata', 'Median'],
                'correct_option': 'Kemungkinan kejadian'
            },
            {
                'question': 'Apa fungsi median dalam statistika?',
                'options': ['Menunjukkan nilai tengah', 'Menunjukkan nilai rata-rata', 'Menunjukkan nilai terkecil'],
                'correct_option': 'Menunjukkan nilai tengah'
            },
            # Tambahkan pertanyaan baru
            # ...
        ]

    elif selected_class == "Aljabar Linier Elementer":
        questions = [
            {
                'question': 'Apa itu matriks identitas?',
                'options': ['Matriks dengan semua elemen nol', 'Matriks dengan semua elemen satu', 'Matriks segitiga bawah'],
                'correct_option': 'Matriks dengan semua elemen satu'
            },
            {
                'question': 'Bagaimana menyelesaikan sistem persamaan linear menggunakan matriks?',
                'options': ['Metode eliminasi Gauss', 'Metode substitusi', 'Metode invers'],
                'correct_option': 'Metode eliminasi Gauss'
            },
            {
                'question': 'Apa yang dimaksud dengan determinan matriks?',
                'options': ['Hasil perkalian elemen-elemen diagonal', 'Hasil penjumlahan elemen-elemen diagonal', 'Hasil pengurangan elemen-elemen diagonal'],
                'correct_option': 'Hasil perkalian elemen-elemen diagonal'
            },
            # Tambahkan pertanyaan baru
            # ...
        ]

    # Cek apakah pengguna sudah mengerjakan kuis untuk kelas ini
    quiz_key = f"{selected_class}_quiz_done"
    if quiz_key not in st.session_state:
        st.session_state[quiz_key] = False

    # Formulir untuk submit kuis
    if not st.session_state[quiz_key]:
        submitted_answers = []
        for i, question in enumerate(questions, start=1):
            st.write(f"**Pertanyaan {i}:** {question['question']}")
            selected_option = st.radio(f"Pilihan untuk Pertanyaan {i}:", question['options'])
            submitted_answers.append({'question': question['question'], 'selected_option': selected_option})

        submit_kuis_button = st.button("Submit Kuis")

        if submit_kuis_button:
            # Jika tombol "Submit Kuis" diklik, maka lakukan penghitungan skor dan tampilkan pesan
            score = 0
            for i, answer in enumerate(submitted_answers, start=1):
                correct_option = questions[i - 1]['correct_option']
                if answer['selected_option'] == correct_option:
                    score += 1

            # Simpan nilai akhir di sesi Streamlit
            st.session_state[f"{selected_class}_quiz_score"] = score

            # Proses penyimpanan jawaban kuis dan nilai ke database atau tempat penyimpanan lainnya
            # Misalnya: submitted_answers dan score dapat disimpan di database untuk pengorehan lebih lanjut

            # Set status quiz_done ke True agar pengguna tidak dapat mengerjakan kuis lagi
            st.session_state[quiz_key] = True

            # Tampilkan nilai akhir
            st.success(f"Kuis berhasil disubmit! Nilai akhir: {score} dari {len(questions)} pertanyaan.")
    elif st.session_state[quiz_key]:
        # Jika kuis sudah dikerjakan, tampilkan nilai akhir dari sesi Streamlit
        score = st.session_state.get(f"{selected_class}_quiz_score", None)
        if score is not None:
            st.warning("Anda sudah mengerjakan kuis untuk kelas ini. Tidak dapat mengerjakan lagi.")
            st.success(f"Nilai akhir: {score} dari {len(questions)} pertanyaan.")

def show_tugas(selected_class):
    st.title(f"Tugas {selected_class}")

    # Mengecek apakah sudah ada session_state untuk menyimpan tugas
    if "submitted_tugas" not in st.session_state:
        st.session_state.submitted_tugas = {}

    # Tugas (contoh)
    if selected_class == "Algoritma Pemrograman":
        allowed_file_types = [".pdf", ".py", ".ipynb"]
        st.write("Buatlah beberapa program (tema bebas) dalam file Python atau notebook Jupyter.")
    elif selected_class == "Analisis Data Statistika":
        allowed_file_types = [".pdf"]
        st.write("Jelaskan apa itu ANOVA dalam analisis data statistika. Scan dan submit dalam bentuk .pdf.")
    elif selected_class == "Aljabar Linier Elementer":
        allowed_file_types = [".pdf"]
        st.write("Selesaikan sistem persamaan linear berikut menggunakan metode matriks, scan dan submit dalam bentuk .pdf:")
        st.write("3x + 2y - z = 10")
        st.write("2x - 4y + 5z = 5")
        st.write("x + y + z = 3")
    else:
        st.warning("Kelas yang Anda pilih tidak valid.")

    # Mengecek apakah sudah ada tugas yang disubmit di session_state
    if selected_class in st.session_state.submitted_tugas:
        st.success("Tugas Berhasil!")

    # Formulir untuk submit tugas
    uploaded_file = st.file_uploader("Upload Tugas:", type=allowed_file_types)

    submit_tugas_button = st.button("Submit Tugas")

    if submit_tugas_button and uploaded_file:
        # Proses penyimpanan file tugas ke tempat penyimpanan yang sesuai
        # Misalnya: uploaded_file dapat disimpan di database atau sistem penyimpanan lainnya

        # Menyimpan informasi bahwa tugas sudah disubmit ke session_state
        st.session_state.submitted_tugas[selected_class] = True

        # Tampilkan pesan bahwa tugas berhasil disubmit
        st.success("Tugas berhasil disubmit!")

# Fungsi untuk menampilkan halaman utama
def main():
    st.set_page_config(page_title="E-Learning", page_icon=":books:")

    # Inisialisasi state untuk menyimpan status login
    if "is_logged_in" not in st.session_state:
        st.session_state.is_logged_in = False

    # Jika belum login, tampilkan halaman login
    if not st.session_state.is_logged_in:
        show_login()
    else:
        # Jika sudah login, tampilkan dashboard E-Learning
        show_dashboard(st.session_state.username)

# Fungsi untuk menampilkan halaman login
def show_login():
    st.title("E-Learning Login")

    # Tampilkan form login
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_button = st.button("Login")

    # Tampilkan form register
    st.subheader("Belum punya akun? Daftar sekarang!")
    new_username = st.text_input("Username baru")
    new_password = st.text_input("Password baru", type="password")
    register_button = st.button("Daftar")

    # Handle login
    if login_button:
        if check_credentials(username, password):
            st.success("Login berhasil!")
            # Set status login untuk menunjukkan bahwa user sudah login
            st.session_state.is_logged_in = True
            st.session_state.username = username
            # Redirect ke dashboard setelah login
            st.experimental_rerun()
        else:
            st.error("Login gagal. Pastikan username dan password benar.")

    # Handle register
    if register_button:
        if register_user(new_username, new_password):
            st.success("Pendaftaran berhasil! Silakan login.")
        else:
            st.error("Pendaftaran gagal. Username mungkin sudah digunakan.")

# Fungsi untuk memeriksa kredensial login
def check_credentials(username, password):
    # Baca data pengguna dari dataframe
    users_df = read_users_data()

    # Periksa apakah username dan password cocok
    if username in users_df.index:
        stored_password = users_df.loc[username, 'password']
        if str(stored_password) == str(password):
            return True
    
    return False


# Fungsi untuk mendaftarkan pengguna baru
def register_user(username, password):
    # Baca data pengguna dari dataframe
    users_df = read_users_data()

    # Periksa apakah username sudah digunakan
    if username in users_df.index:
        return False

    # Tambahkan pengguna baru ke dataframe
    users_df.loc[username] = {'password': password}
    
    # Simpan dataframe kembali
    save_users_data(users_df)

    return True

# Fungsi untuk membaca data pengguna dari file CSV
def read_users_data():
    users_csv_path = "users_data.csv"
    
    # Buat file CSV jika belum ada
    if not os.path.exists(users_csv_path):
        with open(users_csv_path, 'w') as f:
            f.write("username,password\n")
    
    # Baca dataframe dari file CSV
    users_df = pd.read_csv(users_csv_path, index_col='username')
    
    return users_df

# Fungsi untuk menyimpan data pengguna ke file CSV
def save_users_data(users_df):
    users_csv_path = "users_data.csv"
    
    # Simpan dataframe ke file CSV
    users_df.to_csv(users_csv_path)

# Fungsi untuk mendapatkan foto pengguna dari file
def get_user_photo(username):
    # Misalnya, kita menggunakan foto default
    return "default_profile_pic.jpg"

if __name__ == "__main__":
    main()