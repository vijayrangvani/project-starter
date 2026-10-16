# Design decisions

One entry per significant choice. This file is your interview preparation: "why did you choose X?"

## 001: <decision title>  (YYYY-MM-DD)
- **Context:** what problem / constraint forced a choice
- **Options:** A, B, C
- **Decision:** what you picked
- **Why:** the deciding reasons
- **Trade-off:** what you gave up, and when you'd revisit it

## 001: Readiness checks rely on client timeouts, not a thread-pool timeout  (2026-10-16)
- **Context:** a hung dependency inside a readiness check can stall `/ready` until the probe times out.
- **Options:** (A) run checks in a thread pool with a deadline; (B) require each check to use its client's own timeout (DB `connect_timeout`, Redis `socket_timeout`, httpx `timeout=`).
- **Decision:** B.
- **Why:** Python can't kill a hung thread. With A, repeated probes against a hung dependency leave stuck threads until the pool is exhausted; then healthy checks also time out and `/ready` misreports which dependency is broken. B fixes the cause, with less code.
- **Trade-off:** relies on discipline: a check written without a timeout can still hang. Revisit if checks call code that has no timeout option (wrap that one check, not all of them).
