# ADR 0007: How the orders service announces paid orders

Status: Accepted
Date: 2026-10-22
Deciders: Orders tech lead, database owner, Warehouse team lead
Supersedes: ADR 0005

## Context
Orders are announced by a worker that scans the orders table every 10 seconds for paid rows. Volume grew from 2,000 to 40,000 orders a day. A scan now takes about 6 seconds, so confirmation emails arrive up to 25 seconds late, and the database owner has asked us to reduce the load. The Warehouse team needs the same event. The team has 6 engineers and no one has run a message broker. Black Friday is in 10 weeks and the tooling budget is small. Orders must never be announced twice to the stock system, and must never be lost.

## Options considered
### Option A: keep polling, make it cheap
Advantage: nothing new to run; it ships this week.
Main cost: the Warehouse team polls too, so load grows with every new reader, and latency stays at the poll interval.
Pick it if: the team has no time to learn anything new before Black Friday.

### Option B: publish to a managed queue
Advantage: any team can subscribe without touching the orders database.
Main cost: a failure between the database commit and the publish can lose or repeat a message, and we must handle that.
Pick it if: more consumers are coming and a clean boundary matters.

### Option C: an outbox table with a relay
Advantage: the event is written in the same transaction as the order, so no event is lost and no second system has to be kept in step with the database.
Main cost: one more table and a relay process to run, and someone on the team must learn to operate it.
Pick it if: events must never be lost and the team can own one small process.

## Decision
We will write an event row in the same transaction as the order (an outbox) and forward it to a managed queue with a small relay, because it takes the polling load off the database without ever losing an event.

## Consequences
Good: the Warehouse team subscribes without touching our database; emails arrive in under 2 seconds.
Bad: we own one more table and one relay process, a stuck relay delays every consumer, and the relay can publish an event twice, so consumers must ignore repeats by order id.
Revisit when: the relay's backlog is over 1,000 events for more than 5 minutes, or a third consumer needs ordering guarantees the queue cannot give.
