import threading
import tkinter as tk

from app.diagnostics.verification import verify_improvement
from app.local_diagnostic.collector import collect_local_diagnostic


class WiFiDiagnosticGUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("WiFi Diagnostic")
        self.root.geometry("760x620")
        self.root.configure(bg="white")
        self.root.resizable(False, False)

        self.title_font = ("Segoe UI", 24, "bold")
        self.heading_font = ("Segoe UI", 14, "bold")
        self.normal_font = ("Segoe UI", 11)
        self.small_font = ("Segoe UI", 9)

        # Stores the previous diagnostic so we can compare
        # it with the next diagnostic run.
        self.previous_result = None

        self.show_start_screen()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_start_screen(self):
        self.clear_screen()

        container = tk.Frame(
            self.root,
            bg="white",
        )
        container.pack(
            fill="both",
            expand=True,
            padx=70,
            pady=70,
        )

        tk.Label(
            container,
            text="WiFi Diagnostic",
            font=self.title_font,
            bg="white",
            fg="black",
        ).pack(anchor="w")

        tk.Label(
            container,
            text="Find out what is wrong with your connection.",
            font=self.normal_font,
            bg="white",
            fg="#555555",
        ).pack(
            anchor="w",
            pady=(10, 35),
        )

        tk.Button(
            container,
            text="Run Diagnostic",
            command=self.start_diagnostic,
            font=("Segoe UI", 11, "bold"),
            bg="black",
            fg="white",
            activebackground="#222222",
            activeforeground="white",
            relief="flat",
            padx=24,
            pady=12,
            cursor="hand2",
        ).pack(anchor="w")

        tk.Label(
            container,
            text=(
                "The diagnostic checks your local network, "
                "internet path, and DNS."
            ),
            font=self.small_font,
            bg="white",
            fg="#777777",
        ).pack(
            anchor="w",
            pady=(20, 0),
        )

    def start_diagnostic(self):
        self.show_progress_screen()

        thread = threading.Thread(
            target=self.run_diagnostic,
            daemon=True,
        )
        thread.start()

    def show_progress_screen(self):
        self.clear_screen()

        self.progress_title = tk.Label(
            self.root,
            text="Running diagnostic...",
            font=self.title_font,
            bg="white",
            fg="black",
        )
        self.progress_title.pack(
            anchor="w",
            padx=70,
            pady=(70, 10),
        )

        self.progress_message = tk.Label(
            self.root,
            text="Starting...",
            font=self.normal_font,
            bg="white",
            fg="#555555",
        )
        self.progress_message.pack(
            anchor="w",
            padx=70,
        )

        self.progress_bar = tk.Frame(
            self.root,
            bg="#eeeeee",
            height=6,
        )
        self.progress_bar.pack(
            fill="x",
            padx=70,
            pady=(35, 0),
        )

        self.progress_fill = tk.Frame(
            self.progress_bar,
            bg="black",
            height=6,
            width=0,
        )
        self.progress_fill.place(
            x=0,
            y=0,
            relheight=1,
        )

    def update_progress(self, step: str, message: str):
        progress_values = {
            "setup": 10,
            "router": 35,
            "internet": 60,
            "dns": 80,
            "analysis": 95,
            "complete": 100,
        }

        value = progress_values.get(step, 0)

        def update():
            self.progress_message.config(text=message)

            self.progress_fill.place(
                x=0,
                y=0,
                relheight=1,
                relwidth=value / 100,
            )

        self.root.after(0, update)

    def run_diagnostic(self):
        try:
            result = collect_local_diagnostic(
                progress_callback=self.update_progress,
            )

            self.root.after(
                0,
                lambda: self.show_result_screen(result),
            )

        except Exception as error:
            self.root.after(
                0,
                lambda: self.show_error_screen(str(error)),
            )

    def show_result_screen(self, result):
        # Compare this diagnostic with the previous one.
        verification = None

        if self.previous_result is not None:
            verification = verify_improvement(
                self.previous_result.evidence,
                result.evidence,
            )

        # Store the current result for the next Run Again.
        self.previous_result = result

        self.clear_screen()

        container = tk.Frame(
            self.root,
            bg="white",
        )
        container.pack(
            fill="both",
            expand=True,
            padx=70,
            pady=45,
        )

        explanation = self.get_explanation(
            result.diagnosis,
        )

        tk.Label(
            container,
            text=explanation["title"],
            font=self.title_font,
            bg="white",
            fg="black",
            wraplength=620,
            justify="left",
        ).pack(
            anchor="w",
        )

        tk.Label(
            container,
            text=explanation["message"],
            font=self.normal_font,
            bg="white",
            fg="#555555",
            wraplength=620,
            justify="left",
        ).pack(
            anchor="w",
            pady=(12, 20),
        )

        # Show verification only from the second diagnostic onward.
        if verification is not None:
            tk.Label(
                container,
                text=verification.title,
                font=self.heading_font,
                bg="white",
                fg="black",
                wraplength=620,
                justify="left",
            ).pack(
                anchor="w",
                pady=(0, 4),
            )

            tk.Label(
                container,
                text=verification.message,
                font=self.normal_font,
                bg="white",
                fg="#555555",
                wraplength=620,
                justify="left",
            ).pack(
                anchor="w",
                pady=(0, 15),
            )

        tk.Label(
            container,
            text="What to try",
            font=self.heading_font,
            bg="white",
            fg="black",
        ).pack(
            anchor="w",
            pady=(5, 8),
        )

        recommendation = result.recommendation

        tk.Label(
            container,
            text=recommendation.title,
            font=self.heading_font,
            bg="white",
            fg="black",
            wraplength=620,
            justify="left",
        ).pack(
            anchor="w",
            pady=(0, 6),
        )

        for step_number, step in enumerate(
            recommendation.steps,
            start=1,
        ):
            tk.Label(
                container,
                text=f"{step_number}. {step}",
                font=self.normal_font,
                bg="white",
                fg="#333333",
                wraplength=600,
                justify="left",
            ).pack(
                anchor="w",
                pady=2,
            )

        tk.Label(
            container,
            text="Evidence",
            font=self.heading_font,
            bg="white",
            fg="black",
        ).pack(
            anchor="w",
            pady=(25, 8),
        )

        evidence = result.evidence

        evidence_lines = [
            f"Router reachable: {evidence.router_reachable}",
            f"Internet reachable: {evidence.internet_reachable}",
            f"DNS working: {evidence.dns_working}",
        ]

        if evidence.router_packet_loss_percent is not None:
            evidence_lines.append(
                f"Router packet loss: "
                f"{evidence.router_packet_loss_percent:.1f}%"
            )

        if evidence.router_latency_average_ms is not None:
            evidence_lines.append(
                f"Router latency: "
                f"{evidence.router_latency_average_ms:.1f} ms"
            )

        if evidence.router_jitter_ms is not None:
            evidence_lines.append(
                f"Router jitter: "
                f"{evidence.router_jitter_ms:.1f} ms"
            )

        if evidence.internet_packet_loss_percent is not None:
            evidence_lines.append(
                f"Internet packet loss: "
                f"{evidence.internet_packet_loss_percent:.1f}%"
            )

        if evidence.internet_latency_average_ms is not None:
            evidence_lines.append(
                f"Internet latency: "
                f"{evidence.internet_latency_average_ms:.1f} ms"
            )

        if evidence.internet_jitter_ms is not None:
            evidence_lines.append(
                f"Internet jitter: "
                f"{evidence.internet_jitter_ms:.1f} ms"
            )

        tk.Label(
            container,
            text="\n".join(evidence_lines),
            font=self.small_font,
            bg="white",
            fg="#666666",
            justify="left",
            anchor="w",
        ).pack(
            anchor="w",
        )

        button_frame = tk.Frame(
            container,
            bg="white",
        )
        button_frame.pack(
            anchor="w",
            pady=(30, 0),
        )

        tk.Button(
            button_frame,
            text="Run Again",
            command=self.show_start_screen,
            font=("Segoe UI", 10, "bold"),
            bg="black",
            fg="white",
            activebackground="#222222",
            activeforeground="white",
            relief="flat",
            padx=20,
            pady=9,
            cursor="hand2",
        ).pack(
            side="left",
        )

    def show_error_screen(self, error):
        self.clear_screen()

        container = tk.Frame(
            self.root,
            bg="white",
        )
        container.pack(
            fill="both",
            expand=True,
            padx=70,
            pady=70,
        )

        tk.Label(
            container,
            text="Diagnostic failed",
            font=self.title_font,
            bg="white",
            fg="black",
        ).pack(anchor="w")

        tk.Label(
            container,
            text=str(error),
            font=self.normal_font,
            bg="white",
            fg="#555555",
            wraplength=620,
            justify="left",
        ).pack(
            anchor="w",
            pady=(15, 30),
        )

        tk.Button(
            container,
            text="Try Again",
            command=self.show_start_screen,
            font=("Segoe UI", 10, "bold"),
            bg="black",
            fg="white",
            activebackground="#222222",
            activeforeground="white",
            relief="flat",
            padx=20,
            pady=9,
            cursor="hand2",
        ).pack(anchor="w")

    def get_explanation(self, diagnosis):
        explanations = {
            "no_obvious_problem": {
                "title": "Your connection looks stable",
                "message": (
                    "We did not detect significant connection failures, "
                    "latency problems, or instability."
                ),
            },
            "browser_connection_instability": {
                "title": "Your connection appears unstable",
                "message": (
                    "Some connection requests are failing repeatedly. "
                    "This can cause pages, apps, or videos to load inconsistently."
                ),
            },
            "high_jitter": {
                "title": "Your connection is fluctuating",
                "message": (
                    "The delay between requests is changing significantly. "
                    "This can cause problems with calls, gaming, and live video."
                ),
            },
            "high_latency": {
                "title": "Your connection has high delay",
                "message": (
                    "Requests are taking longer than expected to reach "
                    "the destination."
                ),
            },
            "local_network_problem": {
                "title": "Your device cannot reliably reach the router",
                "message": (
                    "The problem appears to be between your device and "
                    "your local network."
                ),
            },
            "local_network_instability": {
                "title": "Your local Wi-Fi connection appears unstable",
                "message": (
                    "We detected instability between your device and the router."
                ),
            },
            "internet_connection_problem": {
                "title": "Your internet connection appears unavailable",
                "message": (
                    "Your device can reach the router, but it cannot reliably "
                    "reach the internet."
                ),
            },
            "dns_problem": {
                "title": "There may be a DNS problem",
                "message": (
                    "Your device can reach the internet, but domain-name "
                    "resolution is not working correctly."
                ),
            },
            "internet_path_instability": {
                "title": "Your internet connection appears unstable",
                "message": (
                    "We detected packet loss beyond your local router."
                ),
            },
        }

        return explanations.get(
            diagnosis,
            {
                "title": "We found something unusual",
                "message": (
                    "The diagnostic detected a condition that needs "
                    "further investigation."
                ),
            },
        )


def main():
    root = tk.Tk()
    WiFiDiagnosticGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()