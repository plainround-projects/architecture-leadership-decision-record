# ADR 0005: Announce paid orders by polling the orders table

Status: Superseded by ADR 0007
Date: 2025-03-04
Deciders: Orders tech lead

## Context
Written in October 2026 from the pull request that added the worker, as the record the decision should have had. In March 2025 the shop sold about 2,000 orders a day. Customers got a confirmation email, and the stock system had to be told about each paid order. The team had 4 engineers and no message broker, and the first release was due in 3 weeks.

## Options considered
### Option A: a worker that scans for paid rows
Advantage: nothing new to run; the worker is 60 lines in the service the team already owns.
Main cost: every scan reads the orders table, so the load grows with the number of orders.
Pick it if: volume is low and the team has no spare time to learn a new part.

### Option B: a database trigger that calls the stock system
Advantage: the stock system hears about a paid order in the same moment it is paid.
Main cost: a slow or failing stock system would hold up every payment.
Pick it if: the stock system is fast and never fails.

## Decision
We will scan the orders table for paid rows every 10 seconds with one worker, because it ships in the 3 weeks we have and needs nothing new to run.

## Consequences
Good: the first release shipped on time with one small worker.
Bad: the load grows with every order and every new reader of the same event.
Revisit when: a scan takes longer than 5 seconds, or orders pass 20,000 a day.
