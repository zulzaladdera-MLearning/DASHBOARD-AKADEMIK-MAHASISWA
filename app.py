# ============================================
# 🎓 DASHBOARD AKADEMIK MAHASISWA — FINAL CODE
# ============================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import gradio as gr

# ============================================
# LOAD DATASET LOKAL (WAJIB 1 FOLDER DENGAN app.py)
# ============================================

df = pd.read_csv("data_mahasiswa_terbaru.csv")

semester_cols = [c for c in df.columns if "ip_semester_" in c]
df["RATA_IP"] = df[semester_cols].mean(axis=1)


# ==========================================================
# 1) VISUALISASI IP PER SEMESTER
# ==========================================================
def visualisasi_ip_per_semester():
    means = df[semester_cols].mean().values
    labels = [c.replace("ip_semester_", "Semester ") for c in semester_cols]

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(labels, means, marker="o", linewidth=3)
    ax.set_title("Rata-Rata IP per Semester", fontsize=14)
    ax.set_ylim(2.0, 4.0)
    ax.grid(True)

    return fig


# ==========================================================
# 2) DISTRIBUSI IPK
# ==========================================================
def visualisasi_distribusi_ip():
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.hist(df["RATA_IP"], bins=20, color="skyblue", edgecolor="black")
    ax.set_title("Distribusi Rata-Rata IP Mahasiswa", fontsize=14)
    ax.set_xlabel("IPK")
    ax.set_ylabel("Frekuensi")
    return fig


# ==========================================================
# 3) VISUALISASI PER FAKULTAS
# ==========================================================
def visualisasi_fakultas(fak):
    data = df[df["NamaFakultas"] == fak]

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.hist(data["RATA_IP"], bins=15, edgecolor="black")
    ax.set_title(f"Distribusi IPK Fakultas {fak}")
    ax.set_xlabel("IPK")
    ax.set_ylabel("Frekuensi")
    return fig


# ==========================================================
# 4) VISUALISASI PER JALUR MASUK
# ==========================================================
def visualisasi_jalur(jalur):
    data = df[df["jalur_masuk"] == jalur]

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.boxplot(data["RATA_IP"], vert=False)
    ax.set_title(f"IPK Berdasarkan Jalur Masuk: {jalur}")
    ax.set_xlabel("IPK")
    return fig


# ==========================================================
# 5) VISUALISASI LATAR BELAKANG KELUARGA
# ==========================================================
def visualisasi_keluarga():
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle("📘 Analisis Pengaruh Latar Belakang Keluarga", fontsize=16)

    # Pendidikan Ayah
    ayah = df.groupby("pendidikan_ayah")["RATA_IP"].mean().sort_values()
    axes[0, 0].barh(ayah.index, ayah.values, color="navy")
    axes[0, 0].set_title("Pendidikan Ayah vs IPK")

    # Pendidikan Ibu
    ibu = df.groupby("pendidikan_ibu")["RATA_IP"].mean().sort_values()
    axes[0, 1].barh(ibu.index, ibu.values, color="darkred")
    axes[0, 1].set_title("Pendidikan Ibu vs IPK")

    # Pendapatan Orang Tua
    df["total_pendapatan"] = df["peng_ayah"] + df["peng_ibu"]
    df["kategori_pend"] = pd.cut(
        df["total_pendapatan"],
        bins=[0, 5_000_000, 10_000_000, 20_000_000, np.inf],
        labels=["< 5 Jt", "5–10 Jt", "10–20 Jt", "> 20 Jt"]
    )
    pend = df.groupby("kategori_pend")["RATA_IP"].mean()
    axes[1, 0].bar(pend.index.astype(str), pend.values, color="green")
    axes[1, 0].set_title("Pendapatan Orang Tua vs IPK")

    # Jumlah Tanggungan (line chart)
    tang = df.groupby("tanggungan")["RATA_IP"].mean()
    axes[1, 1].plot(tang.index, tang.values, marker="o")
    axes[1, 1].set_title("Jumlah Tanggungan vs IPK")

    return fig


# ==========================================================
# 6) STATUS KELULUSAN PER FAKULTAS
# ==========================================================
def visualisasi_status_fakultas(fakultas):

    status_label = {0: "Belum Lulus", 1: "Lulus"}

    data = df[df["NamaFakultas"] == fakultas]
    counts = data["status_mahasiswa"].value_counts().sort_index()
    counts.index = [status_label[i] for i in counts.index]

    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(counts.index, counts.values, color=["#ff6b6b", "#4ecdc4"])

    ax.set_title(f"Status Kelulusan Mahasiswa\nFakultas {fakultas}")

    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, h, str(int(h)),
                ha="center", va="bottom")

    return fig


# ==========================================================
# 7) ANALISIS JALUR MASUK (LENGKAP)
# ==========================================================
def visualisasi_jalur_masuk():
    jalur_list = ["SNMPTN", "SBMPTN", "Mandiri"]

    avg_ip = df.groupby("jalur_masuk")["RATA_IP"].mean().reindex(jalur_list)
    jumlah_mhs = df["jalur_masuk"].value_counts().reindex(jalur_list)

    status = df.groupby(["jalur_masuk", "status_mahasiswa"]).size().unstack(fill_value=0)
    status = status.reindex(jalur_list)

    fig, axes = plt.subplots(3, 1, figsize=(10, 18))

    # Grafik 1 — IPK rata-rata
    axes[0].bar(avg_ip.index, avg_ip.values, color="#4ecdc4")
    axes[0].set_title("Rata-Rata IPK per Jalur Masuk")

    # Grafik 2 — jumlah mhs
    axes[1].bar(jumlah_mhs.index, jumlah_mhs.values, color="#ffbe76")
    axes[1].set_title("Jumlah Mahasiswa per Jalur Masuk")

    # Grafik 3 — Kelulusan
    axes[2].bar(status.index, status[0], label="Belum Lulus", color="#ff6b6b")
    axes[2].bar(status.index, status[1], bottom=status[0], label="Lulus", color="#4ecdc4")
    axes[2].set_title("Status Kelulusan per Jalur Masuk")
    axes[2].legend()

    return fig


# ==========================================================
# 🚀 GRADIO UI
# ==========================================================
def build_dashboard():

    with gr.Blocks(title="Dashboard Akademik Mahasiswa") as demo:

        gr.Markdown("""
        # 🎓 DASHBOARD AKADEMIK MAHASISWA
        Analisis prestasi mahasiswa berdasarkan IPK, fakultas, jalur masuk, dan latar belakang keluarga.
        ---
        """)

        # --------------------
        # TAB 1
        with gr.Tab("📈 IP Per Semester"):
            btn1 = gr.Button("Tampilkan Grafik")
            out1 = gr.Plot()
            btn1.click(visualisasi_ip_per_semester, outputs=out1)

        # --------------------
        # TAB 2
        with gr.Tab("📊 Distribusi IPK"):
            btn2 = gr.Button("Tampilkan Grafik")
            out2 = gr.Plot()
            btn2.click(visualisasi_distribusi_ip, outputs=out2)

        # --------------------
        # TAB 3
        with gr.Tab("🎓 Analisis Per Fakultas"):
            fak = gr.Dropdown(df["NamaFakultas"].unique().tolist(), label="Pilih Fakultas")
            out3 = gr.Plot()
            fak.change(visualisasi_fakultas, inputs=fak, outputs=out3)

        # --------------------
        # TAB 4
        with gr.Tab("🛣 Analisis Jalur Masuk"):
            btn_jalur = gr.Button("Tampilkan Analisis")
            out_jalur = gr.Plot()
            btn_jalur.click(visualisasi_jalur_masuk, outputs=out_jalur)

        # --------------------
        # TAB 5
        with gr.Tab("🏠 Latar Belakang Keluarga"):
            btn5 = gr.Button("Tampilkan Grafik")
            out5 = gr.Plot()
            btn5.click(visualisasi_keluarga, outputs=out5)

        # --------------------
        # TAB 6
        with gr.Tab("📘 Status Kelulusan per Fakultas"):
            fak2 = gr.Dropdown(df["NamaFakultas"].unique().tolist(), label="Pilih Fakultas")
            out6 = gr.Plot()
            fak2.change(visualisasi_status_fakultas, inputs=fak2, outputs=out6)

    return demo


app = build_dashboard()
app.launch()
# Jika untuk HuggingFace gunakan:
# app.launch(server_name="0.0.0.0", server_port=7860)
