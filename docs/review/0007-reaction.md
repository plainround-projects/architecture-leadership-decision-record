# Reaction log: ADR 0007

Reader: backend engineer on the Warehouse team, not in the decision meeting
Reader kind: worked-example
ADR: 0007

## Said back
> They write the order, then send a message to the queue straight after, and we get each paid order exactly once, so the stock system does not need to check anything.

## Misunderstood
The reader took "never announced twice" in the context as a promise of the design. The record said consumers get the event, and it never said the relay can publish twice, so the reader dropped the duplicate check the stock system needs.

## Fix
Before: "we own one more table and one relay process, and a stuck relay delays every consumer."
After: "we own one more table and one relay process, a stuck relay delays every consumer, and the relay can publish an event twice, so consumers must ignore repeats by order id."
