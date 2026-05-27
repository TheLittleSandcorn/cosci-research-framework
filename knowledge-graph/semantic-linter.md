# Semantic Linter & Validation Rules

## Purpose

This document defines rules that can later be automated to detect semantic drift, conceptual inflation, 
and epistemic boundary violations.

## Core Rules

### 1. Epistemic Level Assignment

Every major claim should be assigned to one of the following levels:

- Formal
- Implementable
- Empirical
- Interpretive
- Visionary

Missing assignment should produce a linter warning.

### 2. Restricted Terms

Restricted terms such as:

- transdimensional
- emergent
- cognitive
- consciousness
- lattice
- epistemic system
- algebraically grounded

require an explicit epistemic level marker.

Missing marker should produce a linter error.

### 3. Implementation Status

Documents must clearly separate:

- implemented
- planned
- speculative

Unclear status should produce a warning.

### 4. Provenance

Major factual claims should reference either:

- a source
- a decision log entry
- a reasoning trace
- an implementation artifact

Missing provenance should produce a warning.

### 5. Knowledge Graph Files

Files inside `knowledge-graph/` should include:

- purpose
- status
- epistemic level
- validation rules if applicable

## Future Automation

Planned automation:

- Markdown parser
- rule checker
- restricted term scanner
- provenance checker
- GitHub Action
- violation report

## Current Status

- Rule definition: active
- Automation: not implemented
- Enforcement: manual review only

## Final Rule

A semantic linter is only valuable when it becomes executable.
The next step after this file is implementation.


