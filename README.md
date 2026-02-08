# High-Performance Data Ingestion Engine

A memory-efficient ETL (Extract, Transform, Load) pipeline built in Python. This engine is designed to process large-scale CSV datasets (1M+ rows) with a constant memory footprint ($O(1)$ space complexity) and high throughput using **Generator Composition** and the **Strategy Pattern**.



---

## 🚀 Performance Metrics
* **Throughput:** ~360,000 rows per second.
* **Processing Time:** ~2.78 seconds for 1,000,000 rows.
* **Memory Usage:** Constant $O(1)$ (approx. < 50MB RAM), regardless of input file size.

---

## 🛠 Architectural Highlights
* **Generator-Based Extraction:** Uses lazy evaluation to stream data one row at a time, preventing memory overflows.
* **Strategy Pattern:** Decoupled output logic allows for swappable destinations (Console, Local File, or Cloud) without modifying the core engine.
* **Dependency Injection:** The ingestion runner accepts abstract `Destination` types and path configurations, making the system highly testable.
* **Meta-programming:** A custom execution-time decorator provides non-intrusive performance monitoring and telemetry via attribute attachment.
* **Robust Data Mapping:** Uses `dict(zip(keys, values))` for schema-aware row processing, making the filter logic resilient to CSV column reordering.



---

## 📁 Project Structure

* **data/**: Data storage (ignored by git, except .gitkeep)
* **utils/**: Utilities including `data_gen.py` and `time_execution.py`
* **engine.py**: Core Extractor and Transformer logic
* **destinations.py**: Strategy Pattern implementations (ABC)
* **main.py**: Application bootstrap and orchestration

---

## ⚙️ Setup and Usage

### 1. Environment Setup
Clone the repository. The directory structure uses `pathlib` for cross-platform compatibility between Windows and Unix-based systems.

### 2. Generate Test Data
To stress-test the engine with a million-row dataset, run the utility script from the root:
`python utils/data_gen.py`

### 3. Configure Filter
Add IDs to `data/blocked_ids.txt` (one per line). The engine uses a **Set** for these IDs to maintain $O(1)$ lookup speeds during the transformation phase.

### 4. Run the Pipeline
Execute the main orchestrator:
`python main.py`

---

## 📝 Design Patterns Applied
* **Strategy:** `Destination` Abstract Base Class (ABC) for polymorphic output.
* **Context Manager:** Resource lifecycle management (`__enter__`/`__exit__`) for safe, lazy file handling.
* **Decorator:** Clean separation of concerns for telemetry and performance logging.
* **Liskov Substitution:** All destination subclasses can be swapped without altering the `run_ingestion` logic.