# Audience versions: ADR 0007

## Engineers
The order and its event row are written in one database transaction. A small relay process reads the unsent rows and publishes them to the managed queue, then marks them sent. If the relay crashes between the publish and the mark, it publishes the row again, so every consumer must ignore a repeat by order id. We chose this over publishing straight from the service because that path can lose or repeat a message when the commit and the publish disagree. The code change is one insert next to the order insert, the relay, and an alert on its backlog.

## Manager
Paid-order emails drop from up to 25 seconds to under 2 seconds before Black Friday in 10 weeks, and the load from scanning goes away. The risk is 1 new process to run, covered by an alert when its backlog passes 1,000 events.

## Warehouse team
From 3 November, subscribe to the "order.paid" queue instead of polling our table. Expect an occasional duplicate, so use the order id to ignore repeats. The old table access stays open until 1 December.
