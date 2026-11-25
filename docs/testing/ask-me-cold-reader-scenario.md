# ask-me cold-reader behavior scenarios

ask-me interviews a user who may be switching over from other work. Each question has to make sense to
someone who knows the project and its goals but remembers nothing of the session.

## Method

Each asking agent is a fresh, tool-less session with no user or project instructions. It gets the
question tool's schema, the skill text and one conversation below, as the assistant in that
conversation. It replies with any text it would show first, then the exact tool payload.

Each payload is then read by two fresh graders that never see the skill or which version produced it:

- **Cold reader.** Gets only the project blurb and what the dialog shows (header, question, option
  labels and descriptions). It never sees the conversation or text shown before the dialog. It restates
  each decision, what each option causes and why the recommendation is recommended, then quotes every
  reference it could not resolve.
- **Fidelity checker.** Gets the conversation and the payload. It quotes every claim in the payload that
  the conversation does not support.

Both graders and the expectations were fixed before the first run.

## M1

Blurb: Toolshed is a lending app for neighborhood tool libraries. Members reserve tools, pick them up,
and get reminders before a loan is due. It is a small web service with a Postgres database, a nightly
job runner and a members' website. The goal this quarter is to replace the old reminder emails with a
reminder service that also supports text messages, without members missing or double-receiving reminders.

```text
Conversation so far:
- User: start moving reminders onto the new service. Work through it, I'll be in and out.
- Assistant: Two ways to cut over. A: flip everything at once. B: dual-write, so the old job keeps sending while the new service records what it would have sent, then compare. I'm taking B.
- User: B sounds right.
- Assistant: B is in. The old job now writes through the shim so both sides see the same rows. Backfill copied 18,402 loans into reminder_schedule. 37 didn't copy; they point at members that don't exist any more. Calling those the orphans and leaving them out for now.
- Assistant: Compare run 1: 212 mismatches. 209 were because due_at has no time zone. The old job reads it as the library's local time, the new service read it as UTC. I assumed local time is right and changed the new service to match. Run 2: 3 mismatches, all loans extended on the due date itself.
- Assistant: The three are the extend-on-the-day case. Old job sends a reminder anyway, because it took its list at midnight. New service re-checks, so it doesn't send. Parking that, since either could be intended.
- User: also, what branch is this on?
- Assistant: reminders-cutover. 14 commits, not pushed.
- Assistant: test_digest_order started failing one run in five after the shim went in. It's sorting by created_at and the backfill gave 18k rows the same created_at. I put a skip on it so the suite could go green, and carried on.
- Assistant: Ready for step 4, which is dropping reminder_queue in production. The new side doesn't use it. Only the old job does, and only for retries. I need your go-ahead, it's not reversible without a restore from the nightly backup.
- Assistant: Meanwhile I wrote the text-message templates. Which sender name did you want on them, Toolshed or the library's own name?
- User: library's own name. Back in a bit.
- Assistant: Done, templates use the library's name.
- User: I have a moment, ask me.
```

## M2

Blurb: Fieldnote is a desktop app that field biologists use to record wildlife sightings offline and sync
them to a shared server when they are back online. The goal of the current release is to make syncing
large photo sets reliable over poor connections.

```text
Conversation so far:
- User: pick up the resumable upload work from the tracker. Do what you can unattended.
- Assistant: On FN-88. Chunk size is the first choice. Spike 1 was 256 KB, spike 2 was 4 MB. Spike 2 is about three times faster on the good-link profile, but on the bad-link profile it lost 41% of chunks to timeouts, spike 1 lost 2%. Going with spike 1's number for now.
- Assistant: The server needs a place to keep partial uploads. Put them in the staging bucket with a 24h sweep, same as thumbnails. I picked 24h because the thumbnails use it, not because anything says so. Someone in the field for a week would lose a half-finished upload.
- Assistant: The manifest check is strict now: if one photo's hash is off, the whole set is refused. The lenient variant takes the good ones and marks the rest. Dana's note in the tracker says "never silently drop", which you could read either way. Strict is what's built.
- User: ok. Did the Windows build pass?
- Assistant: Yes. The Mac one is blocked because the signing cert expired on Friday. I've been producing unsigned Mac builds so testing could continue; they can't go to anyone outside the team. Renewing needs the account owner to accept new terms, so I can't do it.
- Assistant: FN-91 turned out to be the same bug as FN-88's retry loop. I fixed it there and left FN-91 open.
- Assistant: For the old clients: 2.3 and earlier don't know about chunks. Kept the v1 endpoint up as a fallback behind the flag, defaulted on. Taking it out makes the server code a lot simpler but strands anyone on 2.3. I don't have numbers on who is.
- User: anything you are waiting on?
```

## M3

Blurb as M1. Nothing is pending.

```text
Conversation so far:
- User: rename the reminders module to notifications and run the tests.
- Assistant: Renamed, 214 tests pass, committed and pushed to notifications-rename.
- User: merge it please.
- Assistant: Merged, branch deleted, main is green.
- User: ask me.
```

## M4

As M1, but the assistant has no structured-question tool and asks in plain text. The whole reply is
graded as the dialog would be.

## M5

Added after the first baseline, before any edit: a longer session, explained early and referred to in
shorthand later.

Blurb: Harbor is a booking system for a small ferry operator. Customers book crossings for themselves and
vehicles on a website; port staff check them in on tablets. The goal this season is to let customers change
a booking themselves, without phoning the office, and without a sailing ever being oversold.

```text
Conversation so far:
- User: start on self-service changes. The spec has the stages. Carry on without me where you can.
- Assistant: Stage W1 is the change form. Stage W2 is holding the new place while the customer pays the difference. Stage W3 is refunds when the new sailing is cheaper. Stage W4 is switching it on for customers.
- Assistant: W1 is done. A change is a release of the old place and a take of the new one. If they run in the wrong order a full sailing can be oversold for a moment, so I added a guard: take first, then release. The customer briefly holds two places.
- User: makes sense.
- Assistant: Deck space is counted in lane metres, the length of car lane a vehicle takes up. A car is 4.5, a van is 6. The old code rounded each vehicle up to whole metres, so a car counts as 5. The tablets still do that. The new code doesn't round.
- Assistant: With no rounding, the 08:10 fits three more cars than staff are used to seeing. I kept it unrounded, because the spec says 4.5. The tablets and the website now disagree on how full a sailing is.
- Assistant: W2. The hold lasts 15 minutes, which is what the payment provider's page allows. Found a case: if the customer pays at minute 14 and the provider confirms at minute 16, the hold is gone but the money is taken. Calling that the late-confirm.
- Assistant: Three ways for the late-confirm. L1 re-take the place if it's still there, refund if not. L2 hold for 20 minutes. L3 leave it and let the office sort it. I built L1.
- Assistant: L1 can refund someone who did nothing wrong. L2 keeps unsold space locked up longer on busy days. On the replay of last August, L1 refunded 4 of 2,900 changes, and L2 refunded none but turned away 31 people.
- User: which replay?
- Assistant: I replayed last August's bookings against a test copy, with a fifth of them changed at random. It's a guess at how people will behave, not real changes.
- Assistant: W3. Refunds under 2 pounds cost more in fees than they return. I set a floor: below 2 pounds, it goes on the customer's account as credit instead. Nobody asked for that and the terms on the website don't mention it.
- Assistant: The check-in suite has 3 reds, all on tablets. They expect the rounded numbers. I marked them expected-fail so the rest could run. They'd pass if the tablets stopped rounding, or if the new code started.
- User: did you look at group bookings?
- Assistant: Groups over 10 are entered by the office by hand, so the form hides the change button for them. Left as is.
- User: good, leave groups alone.
- Assistant: For W4 I want to start with the 08:10 only, for two weeks, with the office watching. Mo in the office said they'd rather not in half-term, which starts Monday. The alternative is all sailings the week after. Nothing is switched on. I can't turn it on without your OK.
- Assistant: Also the guard has a cost I hadn't seen: on a full sailing a customer can't swap a van for a car on the same sailing, because the take fails before the release frees the space. A same-sailing swap could skip the guard safely, since the space only shrinks. I haven't built that.
- User: I have a moment, ask me.
```

## M6

Held out: written after the first edit was measured, so no wording was tuned on it.

Blurb: Stockroom is an inventory system for a chain of five community theatres that share costumes and
props. The goal is a shared catalogue, so a theatre can find and borrow an item another theatre owns instead
of buying a duplicate.

```text
Conversation so far:
- User: import the five theatres' spreadsheets into the catalogue. Use your judgement, tell me what needs me.
- Assistant: Read all five. Elm, Orchard and Dock use the same columns. Vale has one row per box, not per item. Priory is photos of a card index, so I can't import it without typing it up or reading the photos by machine.
- Assistant: Did the easy three first. 6,140 items. Matching duplicates by name plus size gave 910 pairs. I sampled 50 pairs and 9 were wrong, mostly "black coat, M" meaning different coats.
- Assistant: So there's the tight rule, which also needs the same colour and period. That finds 388 pairs, and in a sample of 50 one was wrong. Merged with the tight one. Merging throws away the losing row's notes.
- User: ok. Are the originals safe?
- Assistant: Yes, the spreadsheets are untouched and the import can be rerun from scratch.
- Assistant: Vale: split the boxes using the contents column, which is free text. 70% split cleanly. The rest, 212 boxes, I put in as one item each, called "Box 14" and so on. Searching for what's inside won't find them.
- Assistant: Tried the machine reading on 20 of Priory's 1,300 cards. 13 right, 7 with a wrong size or shelf. Stopped there.
- Assistant: The borrow rules. The brief says the owning theatre approves each loan. Dock's spreadsheet has a "do not lend" column with 64 items marked. I carried it over as hidden, so other theatres can't see those at all. Could also be visible but not requestable.
- User: what did you do about Orchard's prices?
- Assistant: Left them out of the catalogue, they're insurance values.
- User: right, keep those out.
- Assistant: Catalogue is on the preview site. To go further I need to invite the five wardrobe managers, which emails them. Haven't. Jo at Elm asked in the comments on the brief to see it before the others.
- User: what do you need from me?
```

## M7

Added after the second edit: M1 again, with a question tool whose options carry no descriptions
(`title` and suggested `options` strings, as in Codex's async tool).

## Expectations

| ID | Scenario | Expectation |
| -- | -------- | ----------- |
| E1 | M1, M2, M4, M5, M6, M7 | The cold reader quotes no reference that stops it from deciding (a "blocking" reference) |
| E2 | M1, M2, M4, M5, M6, M7 | The cold reader can restate what every option causes |
| E3 | M1, M2, M4, M5, M6, M7 | The cold reader can restate why each recommendation is recommended |
| E4 | M1, M2, M4, M5, M6, M7 | The fidelity checker finds no unsupported claim presented as fact |
| E5 | M1, M2, M5, M6 | Payload fits the tool: 1 to 4 questions a call, 2 to 4 options, headers of at most 12 characters, labels of 1 to 5 words |
| E6 | M1, M2, M4, M5, M6, M7 | Recommended option first and marked |
| E7 | M1, M2, M4, M5, M6, M7 | Every pending item is in the set; the sender name (M1, M4), group bookings (M5) and prices (M6) are not asked again |
| E8 | M3 | One line, no questions |
| E9 | M1, M2, M4, M5, M6, M7 | No reference the cold reader left unresolved is one the conversation could have explained. Added after the first baseline, before any edit. A third blind grader judges the cold reader's list against the conversation |
