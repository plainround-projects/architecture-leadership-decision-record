# ADR 0007 as a three-minute talk

Our shop sends a confirmation email and tells the stock system about every paid order. For a year and a half a small worker did that by scanning the orders table every ten seconds. That was a fair choice when we sold two thousand orders a day. Now we sell forty thousand. A scan takes six seconds, emails arrive up to twenty-five seconds late, and the database owner asked us to stop. The Warehouse team also wants the event, and Black Friday is ten weeks away. We are six engineers and nobody has run a message broker.

We looked at three options, and each has a real champion. The first is to keep polling and make it cheap with an index. Nothing new to run, and it ships this week. But every new reader adds load, and the delay stays at the poll interval. The second is to publish to a managed queue straight from the service. Other teams subscribe without touching our database. The cost is the gap between the database commit and the publish, where a crash can lose or repeat a message. The third is an outbox. We write the event in the same transaction as the order, and a small relay forwards it to the queue. Nothing is lost, and there is no second system to keep in step with the database.

We chose the outbox, because it takes the polling load off the database without ever losing an event.

Here is what we accepted. We own one more table and one relay process. If the relay sticks, every consumer waits. And the relay can publish an event twice, so the stock system must ignore repeats by order id. A reader who was not in the room told us the design gave exactly one message per order. We had never written down that it can repeat, so we changed the record.

We will look again if the relay's backlog stays over a thousand events for more than five minutes, or if a third consumer needs ordering the queue cannot give. Emails should arrive in under two seconds, before Black Friday.
