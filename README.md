# DMS Backend (Delivery Management System)

An enterprise-grade, high-performance backend architecture for a Delivery Management System (DMS), built with **FastAPI** and managed as a polyglot-ready **uv workspace monorepo**. 

This project is engineered to demonstrate advanced software architecture patterns, prioritizing strict decoupling, maintainability, and domain purity.

### 🚀 Key Architectural Highlights
- **uv Workspace Monorepo:** Clean separation between orchestrator applications (`apps/`) and isolated domain packages (`packages/features/`).
- **Domain-Driven Design (DDD):** Pure domain layers free of third-party I/O dependencies, with explicit ORM-to-Entity mappers.
- **CQRS Pattern:** Strict separation of read (Queries) and write (Commands) operations at the application use-case level.
- **Functional Error Handling:** Utilizing `returns` monads (`Success`/`Failure`) for deterministic domain error propagation instead of raising HTTP exceptions.
- **Advanced Dependency Injection:** Centralized container composition using `dependency_injector`.