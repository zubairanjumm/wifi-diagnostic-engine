# Wi-Fi Diagnostic Engine

## Project Context

Wi-Fi Diagnostic Engine is a B2C network-diagnostics product designed for non-technical home users who experience Wi-Fi or internet problems but do not know how to diagnose them.

The core idea is simple:

> The user describes the problem in plain language. The system collects the technical network evidence required for diagnosis and turns that evidence into a clear explanation and next action.

The product is intended to diagnose problems, not simply provide generic troubleshooting articles or an AI chat interface.

## Problem

A typical home user may experience:

- Slow internet
- High latency
- Unstable connectivity
- Websites not loading correctly
- DNS-related problems
- Wi-Fi connectivity problems
- Internet working on some devices but not others

The user usually does not know which technical information is relevant. Asking them to manually run commands, understand IP addresses, check DNS, measure packet loss, or interpret network statistics creates unnecessary complexity.

The product should collect the useful evidence automatically whenever the user's connection and the platform allow it.

## Product Principle

**Do not make the user become a network engineer. Make the product collect and interpret the evidence.**

The diagnostic engine is the technical core of the product.

The product should distinguish between:

1. What the user reports.
2. What the system can directly measure.
3. What those measurements imply.
4. What action the user should take next.

## Current Stage

The project is currently at the **prototype stage**.

The first prototype is a local Python program that runs network checks on the machine where it is executed. It currently checks:

- Default gateway discovery
- Router reachability
- Internet reachability
- DNS resolution
- Approximate latency
- Basic rule-based diagnosis

The prototype exists to validate the diagnostic concept and understand what network evidence can be collected and how evidence can lead to a diagnosis.

It is not the final product architecture.

## MVP Scope

The first web MVP will focus on situations where the user can reach the diagnostic website.

Completely offline scenarios, where the user's internet connection prevents the website from loading at all, are **out of scope for the first MVP**. Deeper offline diagnostics can be considered in a later product version through mechanisms such as a local diagnostic application or agent.

The MVP should focus on proving that the product can:

1. Start a diagnostic session.
2. Collect useful network evidence using mechanisms available to the web platform and backend.
3. Evaluate that evidence.
4. Identify likely problem areas.
5. Explain the result in simple language.
6. Recommend a clear next action.

## High-Level Architecture

```text
User
  |
  v
Web Application
  |
  v
Diagnostic Session API
  |
  v
Evidence Collection Layer
  |
  +-------------------+
  |                   |
  v                   v
Network Tests     System/Connection Data
  |                   |
  +---------+---------+
            |
            v
      Evidence Model
            |
            v
    Diagnostic Engine
            |
            v
       Diagnosis
            |
            v
 Explanation + Recommended Action
```

### Main Components

#### 1. Web Application

The user-facing interface.

Responsibilities:

- Explain the diagnostic process.
- Ask simple questions when user input is necessary.
- Start and display a diagnostic session.
- Present results without unnecessary technical terminology.

#### 2. Diagnostic Session API

The backend entry point for diagnostic sessions.

Responsibilities:

- Create and manage diagnostic sessions.
- Coordinate evidence collection.
- Return diagnostic progress and results.
- Keep transport concerns separate from diagnostic logic.

FastAPI is the planned backend framework.

#### 3. Evidence Collection Layer

Responsible for obtaining measurable network information.

Potential evidence includes:

- Router/default-gateway reachability
- Internet reachability
- DNS resolution
- Latency
- Packet loss
- Download speed
- Upload speed
- Connection information
- Other measurements proven useful during validation

Not every item can be collected directly from a normal browser. The implementation must respect browser security and permission boundaries.

#### 4. Evidence Model

Raw test results should be converted into structured data rather than passed around as unstructured terminal text.

Example:

```python
{
    "router_reachable": True,
    "internet_reachable": True,
    "dns_working": True,
    "latency_ms": 41,
    "packet_loss_percent": 0
}
```

The exact schema will evolve as testing reveals which evidence is useful.

#### 5. Diagnostic Engine

The diagnostic engine consumes structured evidence and determines the most likely problem area.

Initial approach: deterministic, rule-based diagnosis.

Example:

```text
Router unreachable
        -> likely local Wi-Fi/network problem

Router reachable
Internet unreachable
        -> likely upstream/ISP problem

Internet reachable
DNS failing
        -> likely DNS problem

Connectivity working
High latency/packet loss
        -> possible quality/stability problem
```

The engine should eventually support confidence, multiple possible causes, and additional evidence rather than making unsupported absolute claims.

AI may later help interpret results or improve user communication, but AI is not the foundation of the diagnostic truth. Measurements and diagnostic rules come first.

## Important Technical Constraint

A normal website cannot freely execute operating-system commands such as `ipconfig` on a visitor's computer.

The current Python prototype can do this because it executes locally on the machine running Python.

The web product therefore needs to distinguish between:

- Measurements available through browser/web mechanisms.
- Measurements that can be performed by the backend.
- Measurements requiring an explicitly installed local component in a later version.

The product architecture must not assume unrestricted access to the user's device.

## Current Prototype Flow

```text
prototype.py
    |
    +--> Find default gateway
    |
    +--> Ping router
    |
    +--> Ping 8.8.8.8
    |
    +--> Resolve google.com
    |
    +--> Measure approximate latency
    |
    +--> Apply basic diagnosis rules
    |
    +--> Print result
```

This prototype is intentionally simple. Its purpose is to establish the first working diagnostic loop before introducing a web stack, database, WebSocket layer, or frontend.

## Development Direction

### Phase 1 — Diagnostic Core

- Define required network evidence.
- Improve the accuracy of individual tests.
- Add packet-loss measurement.
- Add speed measurement where appropriate.
- Create a structured evidence model.
- Build deterministic diagnostic rules.
- Test different network failure scenarios.

### Phase 2 — Backend

Planned technologies:

- Python
- FastAPI
- Pydantic
- WebSocket where live diagnostic progress benefits from persistent communication

The diagnostic engine should remain independent from FastAPI/WebSocket code so it can also be tested and run independently.

### Phase 3 — Web MVP

- Professional consumer-facing interface.
- Simple diagnostic start flow.
- Live diagnostic progress.
- Clear diagnosis screen.
- Recommended actions.
- Basic error handling and observability.

The UI should look like a real consumer technology product, not a developer demo.

### Phase 4 — Validation

The primary goal is not feature count. It is evidence that real users have real problems and that the product can diagnose them better or more conveniently than their existing alternatives.

Validation should measure:

- Whether users complete a diagnosis.
- Whether the diagnosis is understandable.
- Whether users believe the result.
- Whether the recommended action helps.
- Which network problems occur most often.
- Which evidence is actually useful.

### Later Versions

Potential future capabilities may include deeper device/network diagnostics, local diagnostic software, historical diagnostics, stronger diagnosis confidence, and additional network-quality measurements.

These are not part of the first MVP unless validation shows they are necessary.

## Design Principles

### Evidence before assumptions

Do not claim a root cause without supporting evidence.

### Diagnosis before information

The product should answer "what is likely wrong?" rather than simply displaying networking statistics.

### Simple language

Technical measurements should be translated into language a normal home user understands.

### Modular architecture

Network tests, evidence models, diagnostic rules, API transport, and UI should remain separable.

### Accuracy over AI

AI should not be used to hide weak diagnostics. The system should first establish reliable evidence and deterministic reasoning.

### Build incrementally

Start with a working diagnostic loop and add complexity only when it solves a demonstrated problem.

## Planned Repository Structure

```text
wifi-diagnostic-engine/
|
+-- app/
|   +-- api/
|   |   +-- websocket.py
|   |   +-- routes/
|   |       +-- session.py
|   |       +-- diagnostics.py
|   |
|   +-- core/
|   |   +-- config.py
|   |   +-- session_manager.py
|   |
|   +-- diagnostics/
|   |   +-- engine.py
|   |   +-- rules.py
|   |   +-- models.py
|   |
|   +-- network/
|   |   +-- connectivity.py
|   |   +-- dns.py
|   |   +-- latency.py
|   |   +-- system_info.py
|   |
|   +-- schemas/
|       +-- session.py
|       +-- diagnostic.py
|
+-- tests/
|   +-- test_session.py
|   +-- test_network.py
|   +-- test_diagnostics.py
|
+-- prototype.py
+-- PROJECT_CONTEXT.md
+-- README.md
+-- .gitignore
+-- pyproject.toml
```

The repository does not need to adopt this entire structure immediately. The architecture should evolve as the prototype proves what components are actually needed.

## What This Project Is Not

This project is not intended to become:

- A generic ChatGPT troubleshooting chatbot.
- A collection of networking articles.
- A developer-only network scanner.
- A command-line utility as the final product.
- A system that blindly runs every possible network test.

The intended product is a consumer diagnostic system that collects relevant evidence and converts it into an understandable diagnosis.

## Immediate Next Step

The next engineering task is to define the **minimum useful evidence set** for common home Wi-Fi problems and then improve the prototype tests around that evidence.

Do not build the full web application yet.

First make the diagnostic reasoning reliable.
