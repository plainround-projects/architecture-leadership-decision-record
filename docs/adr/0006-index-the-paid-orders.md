# ADR 0006: Index the paid orders while the announcement decision is open

Status: Accepted
Date: 2026-10-08
Deciders: Orders tech lead, database owner

## Context
The worker that announces paid orders scans the orders table every 10 seconds, and a scan takes about 6 seconds at 40,000 orders a day. The database owner sees the scan as the largest single read load on the orders database. The broader decision on how to announce orders needs the Warehouse team and will take about 2 weeks. Black Friday is in 12 weeks.

## Options considered
### Option A: a partial index on paid orders
Advantage: one migration, no new part, and the scan reads only the rows it needs.
Main cost: the index adds a small write cost to every order and does nothing for latency or for new readers.
Pick it if: the load must come down this week and the real decision is still open.

### Option B: a read replica for the scan
Advantage: the primary database stops serving the scan entirely.
Main cost: a replica to pay for and monitor, and paid rows can appear a few seconds late on it.
Pick it if: the scan cannot be made cheap with an index.

## Decision
We will add a partial index on paid orders, because it lowers the scan time this week without adding anything to run.

## Consequences
Good: the scan should fall from about 6 seconds to under 1 second.
Bad: the emails stay as late as the poll interval, and the index is a patch that hides the real problem for a while.
Revisit when: ADR 0007 is accepted, or the scan is still over 2 seconds on 20 October.
