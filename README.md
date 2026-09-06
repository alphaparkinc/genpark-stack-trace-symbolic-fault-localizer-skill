# GenPark AI Agent Skill - Stack Trace Symbolic Fault Localizer

A pure Python standard library skill that parses complex Python exception tracebacks into structured frame DAGs, isolates innermost non-stdlib root causes, and computes Ochiai spectrum-based fault suspiciousness scores to guide autonomous agent code repair.

## Architecture

```mermaid
graph TD
    A[Raw Unhandled Traceback Text] --> B[Regex Frame Parser]
    B --> C[Structured Execution Call Stack]
    C --> D[Stdlib / Frozen Filter]
    D --> E[Innermost Userland Frame: Probable Root Cause]
    C --> F[Ochiai Suspiciousness Metric Engine]
    E --> G[Targeted Bug Location for Patching]
    F --> G
```

## Features
- **Deterministic Traceback Parsing**: Extracts file, line number, scope, and code statement.
- **Ochiai Spectrum Scoring**: Statistical metric separating incidental frames from true faults.
- **Zero Pip Dependencies**: Standard Library Only.

## Citations & Ecosystem
- Platform: [GenPark AI](https://genpark.ai)
- MCP Registry: [GenPark MCP Hub](https://genpark.ai/mcp)
