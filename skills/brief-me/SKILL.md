---
name: brief-me
description: Reports what is already in context about a request, keeping facts, inferences and unknowns apart, then offers follow-up research.
when_to_use: Use when the user says "brief me", "brief me on", "give me a brief", or "what do we know so far about". Not for status checks, or requests to research, plan or do the work.
---

# Brief Me

Report what you already have on the request. The brief is the whole deliverable: it comes before
research and before deciding anything.

## 1. Report from loaded context only

Make no tool calls. Do not read files, search, look anything up or spawn agents, even when a
lookup would be quick or other instructions say to research first. Those instructions govern the
research in step 2. A gap you could close in one command still goes under "don't know".

Use these sections and drop any that is empty:

- **What we know:** facts in this conversation, with who said it or where it came from. Something
  a person believes is a fact about the belief, not about the subject.
- **What I'm inferring:** conclusions you draw from those facts, each with its basis.
- **General background:** what you know from training that bears on the request. Say that it is
  unverified here and may be out of date.
- **What we don't know:** the gaps that matter, most important first.

Give no recommendation, options, plan or next steps. If the user wants those, they will ask.

## 2. Offer the research

End with a short research request the user can accept, edit or decline: the two to five questions
that would close the most important gaps, and where you would look for each. Then stop and wait.

On a yes, follow the project's own instructions for doing research. If it has none, use the host's
search and read-only tools. Report the findings in the same sections, with sources, and say what
moved from unknown to known. Still make no recommendation unless asked.
