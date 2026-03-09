# 🐍 High-Performance Data Ingestion Engine

A memory-efficient ETL (Extract, Transform, Load) pipeline built in Python. This engine is designed to process large-scale datasets with a constant memory footprint ($O(1)$ space complexity) and features a **Hybrid AI Transformation** layer for RAG-ready data enrichment.

---

## 🚀 Performance & AI Metrics
* **Throughput:** ~360,000 rows per second (Standard ETL).
* **AI Latency:** Dependent on Azure OpenAI API response times (~200ms per embedding).
* **Memory Usage:** Constant $O(1)$ (approx. < 50MB RAM), regardless of input file size.
* **Vector Dimensionality:** 1536-dimension embeddings via `text-embedding-3-small`.

---

## 🛠 Architectural Highlights
* **Hybrid Pipeline:** Combines traditional $O(1)$ membership filtering (via Sets) with unstructured text enrichment using **Azure OpenAI**.
* **Generator-Based Extraction:** Uses lazy evaluation to stream data one row at a time, preventing memory overflows.
* **Strategy Pattern:** Decoupled output logic via `Destination` ABC. Supports `CSVDestination` for traditional reporting and `JSONLDestination` for AI/Vector workloads.
* **Cross-Platform Pathing:** Fully migrated to `pathlib.Path` for robust file handling across Windows, macOS, and Linux.
* **Cloud-Native AI Integration:** Implements the **Project Gateway** pattern via Microsoft Foundry for centralized model management.
* **Meta-programming:** A custom execution-time decorator provides non-intrusive performance monitoring and telemetry.

---

## 🔍 Semantic Search Utility
The engine includes a `search.py` utility that demonstrates the practical application of the ingested vectors. Unlike traditional keyword search, this utility uses **Cosine Similarity** to find relevant data based on meaning.

* **Vector Comparison:** Uses `numpy` for high-performance linear algebra operations on 1536-dimension arrays.
* **Semantic Retrieval:** Capable of finding "battery issues" even if the query uses different terminology (e.g., "power problems").
* **Memory Efficient:** Streams the `.jsonl` source file to maintain a low memory profile during search.

---

## 📁 Project Structure

* **data/**: Data storage (CSV, TXT, JSONL).
* **utils/**: 
    * `data_gen.py`: Mock and Semantic data generators.
    * `ai_utils.py`: Azure OpenAI client and embedding logic.
    * `time_execution.py`: Telemetry decorator.
* **engine.py**: Core Extractor, Filter, and `AITransformer` logic.
* **destinations.py**: Strategy Pattern implementations (ABC).
    * `CSVDestination`: Standard tabular output.
    * `JSONLDestination`: Optimized for vectors/RAG (preserves arrays).
    * `ConsoleDestination`: High-readability terminal output with vector truncation.
* **search.py**: Semantic search interface using NumPy and Azure OpenAI embeddings.
* **main.py**: Application bootstrap and orchestration.

---

## ⚙️ Setup and Usage

### 1. Environment Setup
Create a `.env` file in the root with your Azure credentials:
```text
AZURE_OPENAI_API_KEY=your_key
AZURE_OPENAI_ENDPOINT=your_endpoint
AZURE_OPENAI_DEPLOYMENT_NAME=text-embedding-3
```

### 2. Generate Semantic Data
Generate a dataset with natural language text for AI processing:
`python utils/data_gen.py`

### 3. Run the AI-Enriched Pipeline
Execute the main orchestrator to filter data and generate embeddings:
`python main.py`

### 4. Interactive Semantic Search
The engine includes a REPL (Read-Eval-Print Loop) for real-time data querying:
`python search.py`

* **Natural Language:** Ask questions like "Which products have power issues?"
* **Contextual Ranking:** Results are returned with a similarity score (0.0 to 1.0).
* **Interactive:** Stay in the session to refine queries or test different semantic angles.

---

## 📝 Design Patterns Applied
* **Strategy:** `Destination` Abstract Base Class (ABC) for polymorphic output.
* **Adapter/Wrapper:** `AITransformer` wraps the OpenAI API to provide a clean interface for the engine.
* **Context Manager:** Resource lifecycle management for safe, lazy file handling.
* **Liskov Substitution:** AI-enriched rows remain compatible with all existing destination types.

---
**Last Refined:** March 2026