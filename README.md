# High-Volume Data Ingestion Engine
**Status:** Senior-Level Mastery Lab | Performance & Architecture Refresher

A high-performance Python ETL (Extract, Transform, Load) engine designed to process multi-gigabyte datasets with a constant memory footprint. This project demonstrates the practical application of meta-programming, streaming data idioms, and the Strategy design pattern.

---

## 🏗️ Architectural Overview

### 1. Streaming Data Pipeline (Generators)
* **Design Goal:** Maintain a space complexity of $O(1)$ regardless of input file size.
* **Mechanism:** Implements a Python generator-based ingestor that yields row-by-row, ensuring the system can process 50GB+ files on machines with limited RAM.

### 2. Output Strategy Pattern
* **Design Goal:** Adherence to the **Open-Closed Principle (OCP)**.
* **Mechanism:** Decouples the processing engine from the data destination. The engine accepts any "Destination Strategy" (File, Console, Cloud) that implements the required interface.

### 3. Non-Intrusive Performance Monitoring (Decorators)
* **Design Goal:** Separation of Concerns between infrastructure and business logic.
* **Mechanism:** Uses a custom `@time_execution_decorator` to benchmark throughput. Leverages **Attribute Attachment** to report final metrics (Rows Per Second) to the main entry point.

---

## 📊 Performance Optimization
* **Lookup Efficiency:** Utilizing Python `Sets` for "Blocked ID" filtering to ensure membership checks remain $O(1)$ even with lists containing millions of blacklisted IDs.
* **Resource Management:** Deterministic cleanup of file handles using context managers inside streaming generators.