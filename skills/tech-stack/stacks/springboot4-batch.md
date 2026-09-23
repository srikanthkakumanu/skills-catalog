# Spring Boot 4 · Spring Batch

Large-volume, scheduled or bulk chunk-oriented processing. Not for user-facing request paths.

## Fits
- **Workload:** ETL, scheduled imports/exports, any chunk-oriented bulk job
- **Reliability:** needs restartability and checkpointing — job state persisted, not fire-and-forget

## Does NOT fit
- User-facing, low-latency API endpoints — route to `springboot4-webmvc-jpa-postgres.md`
- Small one-off scripts with no restart/audit requirement — the job-repository overhead isn't earned
- Real-time/streaming processing — that's `springboot4-event-driven-kafka.md`'s territory

## Stack
| Component | Choice |
|---|---|
| Language | Java 27 (see `java-baseline.md`) |
| Framework | Spring Batch 6 (Boot 4's line — API changed materially from 5.x) |
| Job repository | `spring-boot-starter-batch-jdbc` for persistent, restartable job metadata (the plain starter's repository is in-memory/resourceless) |
| Scheduling | Explicit launch (`spring.batch.job.enabled=false` in a web app) — don't let jobs run on startup unintentionally |

## Prerequisites
- Inject `JobOperator`, not `JobLauncher`/`JobExplorer` (consolidated in Batch 6)
- `new JobBuilder(name, repo)` / `new StepBuilder(name, repo)` — the `*BuilderFactory` classes are gone
- A unique/incrementing job parameter for restart-as-new-instance; omit it when the intent is
  resume-on-failure
- Paging readers need a stable `ORDER BY` on an immutable column, or pages skip/duplicate rows

## Tradeoffs
- A materially different runtime model from request/response Spring Boot — budget for the team to
  learn Batch 6's builder API specifically; Batch 5 knowledge doesn't transfer cleanly

## Implementation detail
`implementation-guide` (Phase 7) — spring-batch.
