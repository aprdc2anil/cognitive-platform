# Platform Validation — Application Index

Consumer applications that validate platform generality and reuse.
Each application is built in a separate repo and must be buildable using platform components
with minimal custom infrastructure.

For how to build on this platform see [platform-application-guide.md](../platform/platform-application-guide.md).

---

## Validation Applications

| Application | Repo | Purpose | Platform components consumed |
|---|---|---|---|
| Examiner Brain + Trainer Brain | `upsc-agent` | UPSC AI exam generation and adaptive learning platform | LLM Gateway, RAG Service, Agent Service, ML + Evaluation Service, Event Runtime, core/database, core/redis, core/metrics, core/logging |

---

## How to Add a New Validation Application

1. Create a requirements doc under `docs/application-validation/` — see [examiner-brain-requirements.md](examiner-brain-requirements.md) as a reference
2. Add a row to the table above
3. Map each application capability to a platform component and platform phase
4. Identify POC paths for platform components not yet built
5. Register the external repo in [platform-repo-structure.md](../platform/platform-repo-structure.md)
