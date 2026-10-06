# NetSense

**Windows network diagnostics without the guesswork.**

NetSense is a Windows network diagnostic tool designed to investigate Wi-Fi and internet connectivity problems beyond a normal speed test.

Instead of only showing how fast a connection is, NetSense collects multiple network signals and uses them to determine **where the connection is having problems** — from the Windows machine and Wi-Fi adapter to the router, DNS, and internet path.

## What NetSense Does

NetSense focuses on answering a simple question:

> **What's actually wrong with my connection?**

It checks:

- Windows PC and Wi-Fi adapter connectivity
- Router reachability
- Internet-path connectivity
- DNS resolution
- Latency
- Jitter
- Packet loss
- Repeated connection failures
- Network stability patterns

The diagnostic engine then turns the collected evidence into a clear diagnosis and a downloadable report.

## Why It Exists

A speed test can tell you that your connection is slow.

It usually doesn't tell you **why**.

A poor connection could be caused by:

- Your computer or Wi-Fi adapter
- The local connection to your router
- Router instability
- DNS problems
- Internet-path instability
- Packet loss
- High latency or jitter

NetSense is designed to investigate these different parts of the connection instead of treating every problem as a simple "slow internet" issue.

## Architecture

```text
                    NetSense
                       |
          +------------+------------+
          |                         |
     Windows App                Web Interface
       (EXE)                    (Vercel)
          |                         |
          v                         v
   Local Diagnostics          Project Website
          |
          v
   Diagnostic Engine
          |
          +----------------------+
          |                      |
       Network              Diagnosis
       Evidence                Report
```

### Windows Application

The Windows application runs diagnostics directly on the machine experiencing the problem.

This allows NetSense to inspect local network conditions that a browser-based tool cannot reliably access.

### Web Interface

The NetSense website provides:

- Project explanation
- Feature overview
- Windows download
- Diagnostic workflow explanation

The website does **not** require users to create an account or provide an API key.

## Diagnostic Approach

NetSense uses multiple pieces of network evidence rather than relying on a single threshold.

For example:

```text
Latency
   +
Jitter
   +
Packet Loss
   +
Router Connectivity
   +
Internet Connectivity
   +
DNS
   |
   v
Evidence-based Diagnosis
```

This makes the diagnostic result more useful than simply reporting individual network measurements.

## Current Features

### Windows Diagnostic Application

- Local network diagnostics
- Router connectivity checks
- Internet connectivity checks
- DNS checks
- Latency measurement
- Jitter measurement
- Packet-loss detection
- Repeated request analysis
- Diagnostic report generation
- History/evidence views
- Live monitoring interface

### Website

- NetSense branding
- Responsive landing page
- Windows download
- Explanation of the diagnostic approach
- Animated network visualization
- No account required

## Technology Stack

### Backend

- Python
- FastAPI
- Uvicorn

### Windows Application

- Python
- PySide6
- PyInstaller

### Frontend

- React
- TypeScript
- Vite
- Tailwind CSS

### Development

- Python 3.13+
- uv
- Git
- GitHub

## Project Structure

```text
wifi-diagnostic-engine/
│
├── app/
│   ├── api/
│   ├── local_diagnostic/
│   └── ...
│
├── frontend/
│   ├── public/
│   │   └── netsense-icon.svg
│   └── src/
│       ├── components/
│       ├── pages/
│       ├── App.tsx
│       ├── index.css
│       └── main.tsx
│
├── api/
│   └── index.py
│
├── tests/
│
├── pyproject.toml
├── vercel.json
└── README.md
```

## Download

The current Windows release is available from the GitHub Releases page.

**NetSense v0.1.2**

The release contains the Windows diagnostic application packaged as a ZIP archive.

## Running the Frontend Locally

```powershell
cd frontend
npm install
npm run dev
```

Then open the local development URL shown by Vite.

To create a production build:

```powershell
npm run build
```

## Running the Backend Locally

Install the project dependencies with uv:

```powershell
uv sync
```

Start the FastAPI application:

```powershell
uv run uvicorn app.main:app --reload
```

The API is then available locally through the FastAPI server.

## Building the Windows Application

The Windows application is packaged using PyInstaller.

The resulting executable is distributed as a Windows ZIP release through GitHub Releases.

## Privacy

NetSense is designed around local diagnostics.

The Windows diagnostic application does not require:

- An account
- A subscription
- A paid API
- An AI API key
- A cloud account

The goal is to diagnose the machine and its network connection directly rather than collecting unnecessary user information.

## Security

Windows releases are distributed through GitHub Releases.

For release verification, the SHA-256 checksum of the current `v0.1.2` release archive is:

```text
ccf8eaad6502b3b89e91fcbd5c3950f1172454d13a7052dcc505faa970a2837d
```

You can verify a downloaded ZIP on Windows with:

```powershell
Get-FileHash .\WiFiDiagnostic-v0.1.2.zip -Algorithm SHA256
```

## Project Status

NetSense is an actively developed project.

The current version focuses on building a reliable deterministic diagnostic engine and turning its network evidence into explanations that are understandable to normal users.

Future development will focus on improving diagnostic accuracy, evidence collection, real-world testing, and the Windows user experience.

## License

This project is currently intended as a personal engineering project and portfolio project.
