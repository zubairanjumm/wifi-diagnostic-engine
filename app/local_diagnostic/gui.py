import threading
import tkinter as tk
from tkinter import ttk

from app.local_diagnostic.collector import collect_local_diagnostic


class WiFiDiagnosticGUI:
    def __init__(self, root: tk.Tk):
        self.root = root

        self.root.title("WiFi Diagnostic")
        self.root.geometry("760x680")
        self.root.minsize(700, 620)
        self.root.configure(bg="white")

        self.title_font = ("Segoe UI", 25, "bold")
        self.heading_font = ("Segoe UI", 15, "bold")
        self.step_font = ("Segoe UI", 12, "bold")
        self.normal_font = ("Segoe UI", 11)
        self.small_font = ("Segoe UI", 9)

        self.build_start_screen()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def build_start_screen(self):
        self.clear_window()

        container = tk.Frame(
            self.root,
            bg="white",
        )
        container.pack(
            expand=True,
            fill="both",
            padx=70,
            pady=60,
        )

        tk.Label(
            container,
            text="WiFi Diagnostic",
            font=self.title_font,
            bg="white",
            fg="black",
        ).pack(pady=(70, 10))

        tk.Label(
            container,
            text="Find out what is happening with your network.",
            font=self.normal_font,
            bg="white",
            fg="#555555",
        ).pack()

        tk.Label(
            container,
            text=(
                "The diagnostic runs locally on this computer and "
                "checks your router, internet connection and DNS."
            ),
            font=self.small_font,
            bg="white",
            fg="#777777",
            wraplength=500,
            justify="center",
        ).pack(pady=(12, 45))

        tk.Button(
            container,
            text="Start Diagnosis",
            font=("Segoe UI", 12, "bold"),
            bg="black",
            fg="white",
            activebackground="#333333",
            activeforeground="white",
            relief="flat",
            padx=40,
            pady=15,
            cursor="hand2",
            command=self.start_diagnosis,
        ).pack()

        tk.Label(
            container,
            text="No account or internet service is required for the local test.",
            font=self.small_font,
            bg="white",
            fg="#888888",
        ).pack(pady=25)

    def start_diagnosis(self):
        self.clear_window()

        self.container = tk.Frame(
            self.root,
            bg="white",
        )
        self.container.pack(
            expand=True,
            fill="both",
            padx=65,
            pady=45,
        )

        tk.Label(
            self.container,
            text="Checking your connection",
            font=self.title_font,
            bg="white",
            fg="black",
        ).pack(anchor="w", pady=(20, 8))

        tk.Label(
            self.container,
            text="The diagnostic is collecting network evidence.",
            font=self.normal_font,
            bg="white",
            fg="#555555",
        ).pack(anchor="w", pady=(0, 30))

        self.step_labels = {}

        self.create_step(
            "router",
            "1",
            "LOCAL NETWORK",
            "Checking communication between your computer and router.",
        )

        self.create_step(
            "internet",
            "2",
            "INTERNET CONNECTION",
            "Checking connectivity beyond your local network.",
        )

        self.create_step(
            "dns",
            "3",
            "DNS",
            "Checking whether domain names can be resolved.",
        )

        self.create_step(
            "analysis",
            "4",
            "ANALYSIS",
            "Combining the collected evidence and determining the diagnosis.",
        )

        self.status_label = tk.Label(
            self.container,
            text="Preparing diagnostic...",
            font=("Segoe UI", 11, "bold"),
            bg="white",
            fg="black",
            anchor="w",
        )
        self.status_label.pack(
            fill="x",
            pady=(25, 10),
        )

        self.progress = ttk.Progressbar(
            self.container,
            mode="indeterminate",
            length=500,
        )
        self.progress.pack(
            fill="x",
            pady=(0, 20),
        )

        self.progress.start(10)

        threading.Thread(
            target=self.run_diagnostic,
            daemon=True,
        ).start()

    def create_step(
        self,
        key: str,
        number: str,
        title: str,
        description: str,
    ):
        frame = tk.Frame(
            self.container,
            bg="white",
        )
        frame.pack(
            fill="x",
            pady=8,
        )

        number_label = tk.Label(
            frame,
            text=number,
            font=("Segoe UI", 11, "bold"),
            bg="black",
            fg="white",
            width=3,
            height=1,
        )
        number_label.pack(
            side="left",
            padx=(0, 15),
        )

        text_frame = tk.Frame(
            frame,
            bg="white",
        )
        text_frame.pack(
            side="left",
            fill="x",
            expand=True,
        )

        title_label = tk.Label(
            text_frame,
            text=title,
            font=self.step_font,
            bg="white",
            fg="#999999",
            anchor="w",
        )
        title_label.pack(
            fill="x",
        )

        description_label = tk.Label(
            text_frame,
            text=description,
            font=self.small_font,
            bg="white",
            fg="#999999",
            anchor="w",
        )
        description_label.pack(
            fill="x",
            pady=(2, 0),
        )

        status_label = tk.Label(
            frame,
            text="WAITING",
            font=("Segoe UI", 9, "bold"),
            bg="white",
            fg="#999999",
        )
        status_label.pack(
            side="right",
        )

        self.step_labels[key] = {
            "title": title_label,
            "description": description_label,
            "status": status_label,
        }

    def update_progress(self, step: str, message: str):
        self.root.after(
            0,
            lambda: self.apply_progress(step, message),
        )

    def apply_progress(self, step: str, message: str):
        if step in self.step_labels:
            labels = self.step_labels[step]

            labels["title"].configure(
                fg="black",
            )

            labels["status"].configure(
                text="TESTING",
                fg="black",
            )

        self.status_label.configure(
            text=message,
        )

        completed_steps = {
            "internet": "router",
            "dns": "internet",
            "analysis": "dns",
            "complete": "analysis",
        }

        completed_step = completed_steps.get(step)

        if completed_step in self.step_labels:
            labels = self.step_labels[completed_step]

            labels["status"].configure(
                text="DONE",
                fg="black",
            )

            labels["title"].configure(
                fg="black",
            )

    def run_diagnostic(self):
        try:
            result = collect_local_diagnostic(
                progress_callback=self.update_progress,
            )

            self.root.after(
                0,
                lambda: self.show_result(result),
            )

        except Exception as error:
            self.root.after(
                0,
                lambda: self.show_error(str(error)),
            )

    def show_result(self, result):
        self.progress.stop()
        self.clear_window()

        container = tk.Frame(
            self.root,
            bg="white",
        )
        container.pack(
            expand=True,
            fill="both",
            padx=60,
            pady=35,
        )

        tk.Label(
            container,
            text="Diagnosis",
            font=self.heading_font,
            bg="white",
            fg="#666666",
        ).pack(anchor="w")

        tk.Label(
            container,
            text=result.diagnosis.replace("_", " ").upper(),
            font=("Segoe UI", 22, "bold"),
            bg="white",
            fg="black",
        ).pack(
            anchor="w",
            pady=(5, 12),
        )

        explanations = {
            "no_obvious_problem": (
                "Your connection looks stable based on the evidence collected."
            ),
            "local_network_problem": (
                "Your computer is having trouble communicating with the router."
            ),
            "local_network_instability": (
                "There is packet loss between your computer and the router."
            ),
            "internet_connection_problem": (
                "Your device can reach the router, but the internet is unavailable. "
                "Check another device on the same network. If it is also offline, "
                "restart the router and check whether your ISP is having an outage."
            ),
            "internet_path_instability": (
                "There is packet loss between your network and the internet."
            ),
            "high_latency": (
                "The connection is responding more slowly than expected."
            ),
            "high_jitter": (
                "Latency is varying significantly during the test."
            ),
            "dns_problem": (
                "DNS resolution is not working correctly."
            ),
            "browser_connection_instability": (
                "The connection to the diagnostic service is intermittently failing."
            ),
        }

        tk.Label(
            container,
            text=explanations.get(
                result.diagnosis,
                "The diagnostic engine detected a network condition that needs investigation.",
            ),
            font=self.normal_font,
            bg="white",
            fg="#333333",
            wraplength=600,
            justify="left",
        ).pack(
            anchor="w",
            pady=(0, 22),
        )

        evidence = result.evidence

        evidence_frame = tk.LabelFrame(
            container,
            text=" Evidence ",
            font=self.heading_font,
            bg="white",
            fg="black",
            padx=20,
            pady=15,
        )
        evidence_frame.pack(
            fill="x",
        )

        values = [
            (
                "Router packet loss",
                evidence.router_packet_loss_percent,
                "%",
            ),
            (
                "Router latency",
                evidence.router_latency_average_ms,
                " ms",
            ),
            (
                "Router jitter",
                evidence.router_jitter_ms,
                " ms",
            ),
            (
                "Internet packet loss",
                evidence.internet_packet_loss_percent,
                "%",
            ),
            (
                "Internet latency",
                evidence.internet_latency_average_ms,
                " ms",
            ),
            (
                "Internet jitter",
                evidence.internet_jitter_ms,
                " ms",
            ),
            (
                "DNS latency",
                evidence.dns_latency_ms,
                " ms",
            ),
        ]

        for label, value, unit in values:
            row = tk.Frame(
                evidence_frame,
                bg="white",
            )
            row.pack(
                fill="x",
                pady=3,
            )

            tk.Label(
                row,
                text=label,
                font=self.normal_font,
                bg="white",
                fg="#555555",
            ).pack(
                side="left",
            )

            if value is None:
                display_value = "N/A"
            else:
                display_value = f"{value:.2f}{unit}"

            tk.Label(
                row,
                text=display_value,
                font=("Segoe UI", 11, "bold"),
                bg="white",
                fg="black",
            ).pack(
                side="right",
            )

        actions = {
            "no_obvious_problem": (
                "No immediate network change is required. "
                "If you still experience problems, run another diagnostic."
            ),
            "local_network_problem": (
                "Move closer to the router and check whether other devices "
                "can connect to it."
            ),
            "local_network_instability": (
                "Move closer to the router and retest. "
                "If multiple devices have the same problem, restart the router."
            ),
            "internet_connection_problem": (
                "Check another device on the same network. "
                "If multiple devices are affected, restart the router."
            ),
            "internet_path_instability": (
                "Retest the connection. If multiple devices are affected, "
                "the problem may be beyond your local network."
            ),
            "high_latency": (
                "Move closer to the router and retest. "
                "If possible, compare the result with an Ethernet connection."
            ),
            "high_jitter": (
                "Move closer to the router and retest. "
                "If the problem continues, compare with Ethernet or another network."
            ),
            "dns_problem": (
                "Check whether other devices have the same DNS problem."
            ),
            "browser_connection_instability": (
                "Retest the connection and compare with another network."
            ),
        }

        tk.Label(
            container,
            text="What to try",
            font=self.heading_font,
            bg="white",
            fg="black",
        ).pack(
            anchor="w",
            pady=(22, 5),
        )

        tk.Label(
            container,
            text=actions.get(
                result.diagnosis,
                "Run the diagnostic again after checking your connection.",
            ),
            font=self.normal_font,
            bg="white",
            fg="#333333",
            wraplength=600,
            justify="left",
        ).pack(
            anchor="w",
        )

        tk.Button(
            container,
            text="Run Again",
            font=("Segoe UI", 11, "bold"),
            bg="black",
            fg="white",
            activebackground="#333333",
            activeforeground="white",
            relief="flat",
            padx=25,
            pady=10,
            cursor="hand2",
            command=self.build_start_screen,
        ).pack(
            anchor="w",
            pady=25,
        )

    def show_error(self, error_message):
        self.clear_window()

        container = tk.Frame(
            self.root,
            bg="white",
        )
        container.pack(
            expand=True,
            fill="both",
            padx=60,
            pady=60,
        )

        tk.Label(
            container,
            text="Diagnostic failed",
            font=self.title_font,
            bg="white",
            fg="black",
        ).pack(pady=(70, 15))

        tk.Label(
            container,
            text=error_message,
            font=self.normal_font,
            bg="white",
            fg="#555555",
            wraplength=500,
        ).pack(pady=15)

        tk.Button(
            container,
            text="Try Again",
            font=("Segoe UI", 11, "bold"),
            bg="black",
            fg="white",
            relief="flat",
            padx=25,
            pady=10,
            command=self.build_start_screen,
        ).pack(pady=25)


def main():
    root = tk.Tk()
    WiFiDiagnosticGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()