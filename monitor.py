
import customtkinter as ctk
import subprocess
import psutil
import threading
import shutil

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("WSL Monitor")
app.geometry("320x440+1000+50")
app.attributes("-topmost", True)
app.resizable(False, False)

DISTROS = ["Ubuntu", "kali-linux"]
widgets = {}

def command(args):
    result = subprocess.run(
        args,
        capture_output=True,
        timeout=10,
        creationflags=subprocess.CREATE_NO_WINDOW
    )
    raw = result.stdout
    encoding = "utf-16-le" if b"\x00" in raw else "utf-8"
    return raw.decode(encoding, errors="replace").strip()

ctk.CTkLabel(
    app,
    text="WSL SYSTEM MONITOR",
    font=("Segoe UI", 18, "bold")
).pack(pady=12)

system_label = ctk.CTkLabel(
    app,
    text="Windows CPU: -- | RAM: --"
)
system_label.pack()

disk_label = ctk.CTkLabel(app, text="C: Drive: --")
disk_label.pack(pady=(0, 8))

for distro in DISTROS:
    color = "#F97316" if distro == "Ubuntu" else "#38BDF8"

    frame = ctk.CTkFrame(app)
    frame.pack(fill="x", padx=12, pady=6)

    ctk.CTkLabel(
        frame,
        text=distro.upper(),
        text_color=color,
        font=("Segoe UI", 16, "bold")
    ).pack(pady=(8, 2))

    status = ctk.CTkLabel(frame, text="Checking...")
    status.pack()

    disk = ctk.CTkLabel(frame, text="Disk: --")
    disk.pack()

    bar = ctk.CTkProgressBar(
        frame,
        progress_color=color
    )
    bar.pack(fill="x", padx=15, pady=6)
    bar.set(0)

    processes = ctk.CTkLabel(
        frame,
        text="Processes: --"
    )
    processes.pack(pady=(0, 8))

    widgets[distro] = (status, disk, bar, processes)

def update_ui(cpu, ram, windows_disk, results):
    system_label.configure(
        text=f"Windows CPU: {cpu}% | RAM: {ram}%"
    )

    disk_label.configure(
        text=f"C: Free: {windows_disk.free / 1024**3:.1f} GB"
    )

    for distro, data in results.items():
        status, disk, bar, processes = widgets[distro]

        if data is None:
            status.configure(
                text="● Stopped",
                text_color="#EF4444"
            )
            disk.configure(text="Disk: --")
            processes.configure(text="Processes: --")
            bar.set(0)

        elif data == "error":
            status.configure(
                text="● Unavailable",
                text_color="#F59E0B"
            )
            disk.configure(text="Disk: --")
            processes.configure(text="Processes: --")
            bar.set(0)

        else:
            used, total, percent, count = data

            status.configure(
                text="● Running",
                text_color="#22C55E"
            )

            disk.configure(
                text=f"Disk: {used:.1f} / {total:.0f} GB"
            )

            bar.set(percent / 100)

            processes.configure(
                text=f"Processes: {count}"
            )

    app.after(5000, refresh)

def collect():
    cpu = psutil.cpu_percent(interval=0.5)
    ram = psutil.virtual_memory().percent
    windows_disk = shutil.disk_usage("C:\\")

    results = {}

    try:
        running = command([
            "wsl.exe", "--list", "--running", "--quiet"
        ]).splitlines()

        running = [x.strip() for x in running]

        for distro in DISTROS:
            if distro not in running:
                results[distro] = None
                continue

            try:
                output = command([
                    "wsl.exe", "-d", distro,
                    "--exec", "sh", "-c",
                    "df -kP / | tail -1; ps -e --no-headers | wc -l"
                ])

                lines = output.splitlines()
                fields = lines[0].split()

                total = int(fields[1]) / 1024**2
                used = int(fields[2]) / 1024**2
                percent = int(fields[4].rstrip("%"))
                count = int(lines[1])

                results[distro] = (
                    used, total, percent, count
                )

            except Exception:
                results[distro] = "error"

    except Exception:
        results = {d: "error" for d in DISTROS}

    app.after(
        0,
        lambda: update_ui(
            cpu, ram, windows_disk, results
        )
    )

def refresh():
    threading.Thread(
        target=collect,
        daemon=True
    ).start()

ctk.CTkLabel(
    app,
    text="Auto refresh: 5 seconds",
    text_color="gray",
    font=("Segoe UI", 11)
).pack(pady=8)

refresh()
app.mainloop()
