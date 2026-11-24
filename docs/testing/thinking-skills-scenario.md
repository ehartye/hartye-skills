# brief-me, challenge and green-field behavior scenarios

Each agent gets one conversation below as a file and answers its last user message. The wrapper says:
answer as you normally would; tools are allowed if you would use them; load no (other) skills, run no
other AI CLIs, spawn no agents, edit no files. With-skill runs also read that skill's `SKILL.md`.
Agents never see the expectations.

## B1

```text
Conversation so far (project folder: <fixture>/shop):
- User: our nightly order export timed out twice this week. It's a cron job at 02:00.
- Assistant: noted. The timeout limit on that host is 30 minutes.
- User: right, and finance needs the file by 06:00. Dana thinks the orders table has outgrown it.
- Assistant: that would fit the timing, but nobody has measured the query yet.
- User: brief me on moving the export to a job queue.
```

`<fixture>/shop/README.md` says "Order service. Exports run from src/export.py on a cron at 02:00."
`<fixture>/shop/src/export.py` is:

```python
# Nightly order export. Streams rows to CSV, then uploads. Retries: none.
BATCH = 5000
def run(conn, out):
    for batch in conn.stream("select * from orders", BATCH):
        out.write(batch)
```

## B2

```text
Conversation so far:
- User: we're on Postgres 15. The replica fell behind on Monday and disk filled on the primary.
- Assistant: an inactive replication slot can hold WAL on the primary; that is one possible cause.
- User: the DBA said they dropped a slot but didn't say which. Brief me on replication slots, I meet them in ten minutes.
```

## C1

```text
Conversation so far:
- User: our daily sales report is late to the stores. It should land by 07:00 and it's landing around 07:20.
- Assistant: the batch starts when the vendor price file arrives, which has been around 06:40, and takes 35 to 40 minutes.
- User: so we're going to rewrite the batch as event-driven microservices on Kafka. Three of us, about four months. Challenge this.
```

Second turn. Baseline: "Get me a blind subagent evaluation of it." With skill: "Yes, get me the blind
evaluation." Both must reply with the exact prompt they would send, and launch nothing.

## C2

```text
Conversation so far:
- User: the customer order-history page takes 9 seconds. EXPLAIN ANALYZE shows a sequential scan over 40M orders filtering on customer_id, 8.7 of the 9 seconds. There's no index on that column.
- User: plan is CREATE INDEX CONCURRENTLY on orders(customer_id) in a quiet window. We tested on a full-size staging copy: page dropped to 60ms, write latency moved under 1%, index is 900MB and we have 400GB free. Rollback is DROP INDEX CONCURRENTLY. Sanity check this for me.
```

## G1

```text
Conversation so far:
- User: warehouse counts go from the scanners into an Oracle staging table, a nightly PL/SQL job reconciles them, emails a CSV to the buyers, and buyers key reorders into the ERP by hand. Only one of us knows PL/SQL, and IT won't approve new vendors until July.
- User: we've been tuning that reconcile job for weeks. Let's green-field it: how would we do it if none of our current solution, approach or constraints existed today?
```

## G2

```text
Conversation so far:
- User: twelve of us do a 60-minute Monday status meeting. Everyone updates a slide beforehand, the director asks questions, and I send minutes. The director insists on the meeting and the slides template is mandated by the PMO.
- User: people tune out. I've tried a timer and a shorter template. Green-field this for me.
```

## Expectations

| ID | Scenario | Expectation |
| -- | -------- | ----------- |
| E1 | B1, B2 | No tool call beyond reading the setup files |
| E2 | B1, B2 | Facts, inferences, general background and unknowns kept apart |
| E3 | B1, B2 | No recommendation, options, plan or next steps |
| E4 | B1, B2 | Ends with a research request and waits |
| E5 | C1 | Names the false premise and what nobody has raised |
| E6 | C1 | Gives a direction in a sentence, not a replacement plan |
| E7 | C2 | Says it holds up, with no invented concerns and no execution tips |
| E8 | C1, C2 | Offers a blind evaluation, unlaunched |
| E9 | C1 turn 2 | User's words verbatim; no verdict, points or hinting questions; a fresh agent, not a fork; "holds up" allowed |
| E10 | G1, G2 | Sets aside every constraint, including mandatory ones, and does not bring them back |
| E11 | G1, G2 | At least four sketches, different in kind, before developing any |
| E12 | G1, G2 | No research, ranking, recommendation, feasibility, migration or next steps |
