---
name: spec-plan-ii
description: Writes and plans wiki-grounded specs with self-review, blind sanity checks, test-first self-certified development and independent hardening rounds.
argument-hint: "[hardening=N] [request]"
disable-model-invocation: true
---

# Spec and plan with hardening

Turn the user's intent into settled specs, then into a plan ready for handoff. This skill depends
on the **wiki-master** plugin to ground the work and to save specs, and it assumes subagents are
available. It finishes at handoff. The plan carries a self-contained execution contract (the
test-first triples, the hardening rounds, the finding classes, remediation, stopping and delivery)
that the executor follows.

## Arguments

- `hardening=N` may appear anywhere in the arguments; the rest is the request.
- N is a non-negative integer: the most hardening rounds the plan allows for each build spec.
- When it is omitted, N is **2**. The value comes only from the argument or this default; a spec
  never carries a round count. Record N in the plan.

## Who writes what

- **You, the orchestrator, write every spec.** Draft, revise and save each one yourself, in your
  own context, through wiki-master:wiki-project. You also write every other authored project
  page: backlog items, `specced-in` keys and the backlog entries logged from hardening.
- **Subagents only gather evidence or review:** wiki search, research and ingestion, read-only
  code exploration, the sanity check and hardening reviews. They return reports and never write
  specs.
- **Research and ingestion run one worker at a time**, through wiki-master:wiki-researcher, and
  write evidence pages only.

## Stage 1: Spec

Give each independent goal its own saved spec, and apply this stage to every requested goal.
Record dependencies between specs as links with the required outcome or interface contract.

1. **Shape the spec.**
   - Use the [spec template](references/spec-template.md), keeping the sections that settle a
     decision or make the outcome checkable. Scale the detail to the change.
   - Decide early whether it is a build or a spike (step 6).
2. **Interview around the missing decisions.**
   - Reuse answers and authorization already in the conversation.
   - Ask the rest in batches of two to four questions, each with a recommended default.
   - Cover the goal and user-visible outcome, scope, constraints, acceptance, build versus spike,
     and delivery requirements and authorization.
   - Wait for answers before drafting what depends on them. Record a choice the user delegates as
     an assumption.
3. **Ground the request in the wiki before drafting.**
   - Find the project through its overview's `repo:` field, or ask for the project slug.
   - Have a subagent search with wiki-master:wiki-search for relevant knowledge and roadmap items.
   - Report the coverage and the gaps to the user.
   - For the gaps, propose a wiki-master:wiki-researcher round that discovers sources and ingests
     them, or run it under authorization the user already gave. Draft only after it returns or
     the user declines it.
4. **Settle roadmap overlap with the user.**
   - Recommend adopting a matching item, grouping related items with the same goal as work
     packages, or linking out-of-scope items as non-goals. Ask about unresolved conflicts.
   - Mark each absorbed item yourself with `specced-in: ["[[<spec>|WPn]]"]` in its frontmatter.
5. **Explore the code read-only through subagents.**
   - Establish real files, interfaces, commands, current behavior and the project's stated
     implementation and quality rules. Keep findings that affect design or acceptance.
   - Have exploration name the project skills and plugins that fit. Propose them in one question,
     each with a reason and its packages, and record the user's confirmed selection.
   - Take decisions the evidence raises back to the interview.
6. **Shape a spike when the change is an experiment.**
   - State risk-ordered Given/When/Then questions with observable results.
   - Give validated, partial and invalidated verdicts, each with its deliverable and its promote or
     discard criterion.
   - Use the user's effort budget, or "no timebox; stops at the first met exit criterion" when
     none is given.
   - A spike keeps grounding, self-review and the sanity check, but skips TDD, certification and
     hardening, because its deliverable is a verdict with evidence.
   - Promoted work gets its own build spec.
7. **Draft and save the spec yourself.**
   - Write it from the interview, grounding and exploration evidence, using subagent reports as
     inputs, never as drafts.
   - Record decisions as statements and delegated choices as assumptions.
   - Write each acceptance criterion as a runnable command with expected output, or a repeatable
     observation, at the level its artifact can actually show.
   - Give work packages ownership, dependencies, self-contained briefs and Tools lines, with
     delivery as a planned package where the scope needs it.
   - Save it with wiki-master:wiki-project at `wiki/authored/<project>/backlog/<slug>.md`, with
     `kind: backlog-item` and `backlog-status: planned`.
8. **Self-review the saved draft, before the sanity check.**
   - Re-read it as saved and check four things: every decision is settled, each acceptance
     criterion can be observed from its artifact, existing and new behavior are labeled as such,
     and every work package can start from its brief alone.
   - Fix what you find in the spec's text, and save.
   - Keep the self-review's record out of the spec until the sanity check returns, so the checker
     never reads it. Write that record at step 10.
9. **Run the blind sanity check.**
   - **Give a fresh subagent that has not seen this work only** the user's request verbatim, the
     saved spec's path, and read-only access to the repository and the wiki.
   - **Withhold** the self-review notes, the interview rationale and your own conclusions.
   - **Ask it to disagree**, through three broad lenses: (a) a false premise (are we thinking
     about this wrong?), (b) an architectural anti-pattern, over-engineering, or a KISS or YAGNI
     breach, and (c) blind spots (things not considered at all).
   - Say it is a broad-strokes check, not a line-by-line review of process or wording.
   - Ask for a few points, each with its reason and what it would change, and accept "No concerns"
     as a valid result.
10. **Triage the sanity check and record the review.** Its advice is not a directive.
    - Adopt the points you agree with by revising the spec.
    - Present every point you disagree with to the user, with its position, yours and a
      recommendation. The user decides, not you.
    - Now record the self-review outcome, the adopted points, the disputed points and the user's
      decisions in the Review section, and save.

### Spec handoff

- **Settle decisions.** A fresh agent must be able to begin each work package without another
  decision about scope, behavior, interfaces, dependencies, acceptance or authorization. Replace
  placeholders and "decide during implementation" with settled choices; leave routine details to
  the implementer.
- **Settle a spike's method.** Its questions may stay open, but its method, observable outcomes
  and exit criteria are settled. When its verdict decides a later build, plan the spike first.
- **Check the Review section.** It records the self-review, the sanity-check points adopted and
  disputed, and the user's decisions. A spec still waiting on one of these is not ready.
- **Close.** Link the saved specs and say which are ready. If planning was requested and the
  delegated path below is authorized, continue into Stage 2. Otherwise end with "When you're
  ready, run `/spec-plan-ii plan the spec` in Plan mode (add `hardening=N` to change the default
  of 2)."

## Stage 2: Plan

**Mode.** Plan ready specs in the host's Plan mode. Plan outside it only on the delegated path:
the user explicitly authorizes planning outside Plan mode or without being present. Default mode,
a request to implement or silence is not that authorization. On the delegated path:

- record the actual host mode and the source and scope of the authorization;
- save the complete plan as a durable Markdown artifact (the project's plan location, or a named
  file in the task workspace) and project its steps into todos, or a task table in the plan, with
  stable IDs, dependencies and status;
- treat planning authorization as separate from execution authorization, and carry only the
  execution authority the user actually gave.

Without that authorization, stop the stage outside Plan mode and say what must change. Spec edits
are saved outside Plan mode.

1. **Select the specs.**
   - A ready spec has a For the planner section and status planned or in-progress.
   - Plan the named specs, the sole ready spec, or all ready specs when asked. Otherwise list the
     candidates and ask.
   - Recheck each one's decisions and handoff conditions against the current repository.
2. **Reconcile the set into one plan.**
   - Send gaps, contradictions and shared-interface conflicts back to Stage 1 before planning them.
   - Produce one combined plan with a section per spec, qualifying package IDs with the spec slug,
     such as `csv-export/WP1`.
   - Keep specs sequential, with parallel groups inside each spec.
   - A build that depends on an unresolved spike waits for its verdict.
3. **Review a spec that arrives without a review record.**
   - When a selected spec lacks a record of either a self-review or a sanity check, as with a spec
     written by another workflow, run whichever is missing before planning it: Stage 1 step 8 for
     the self-review, steps 9 and 10 for the sanity check. Do not ask whether to.
   - Save the outcome to its Review section, outside Plan mode, then resume planning. When only
     the self-review was missing, record it there directly.
   - Disputed points wait for the user's decision, and the spec is planned only after it.
4. **Plan each build development task as a triple.**
   - Carry the package's brief, owned files, dependencies, done-when and confirmed tools into the
     plan.
   - Assign the whole triple to **one developer agent**:
     - **TDD:** write the tests for the intended behavior, run them, and confirm the expected
       failure.
     - **Dev:** make them pass, then refactor while they stay green.
     - **Certification:** the developer self-certifies that all relevant tests pass and that its
       assigned acceptance criteria are met.
   - Relevant tests are the project's full test command where one exists, otherwise the package's
     new tests plus its acceptance commands.
5. **Define the certification evidence.**
   - It is the **raw test-runner output**, a **diff of the test files since the red step**, and an
     **explicit flag** for any test changed after red or that the developer believes contradicts
     the spec.
   - Nobody re-runs the checks at certification. Hardening reviewers see the same evidence.
6. **Keep spikes out of the triple.** Spike packages get no TDD, certification or hardening. They
   deliver the verdict and its evidence.
7. **Write the hardening contract into the plan** for each build spec, using the
   [hardening contract](#hardening-contract) below.
   - Record N and place up to N rounds after all of that spec's development packages are
     certified and before its delivery package.
   - When N is 0, plan no rounds, and state in the plan and in the handoff: "No independent review
     of the self-certified work will happen."
8. **Plan delegation and delivery.**
   - Default to a subagent per package, running independent packages in parallel with
     self-contained briefs and concise reports of changed files, checks and blockers.
   - Give concurrent packages disjoint file ownership. Sequence shared-file changes and
     dependencies explicitly, and state the reason for any exception.
   - Include delivery, verification, synchronization, evidence capture and workspace cleanup as
     explicit tasks.
9. **Hand off.**
   - Check that the plan covers every selected spec's acceptance criteria and constraints, and
     apply the Spec handoff decision checks to it.
   - In Plan mode, present the plan in the host's plan format. On the delegated path, link the
     saved plan and its task projection.
   - State what was planned, what was actually checked, the hardening value per spec (with the
     zero-round warning when N is 0), remaining blockers and the next action under the recorded
     execution authority.
   - When the checks pass, end with "The spec and plan are ready for handoff," or "The selected
     specs and combined plan are ready for handoff." Planning leaves backlog status unchanged.

## Hardening contract

Copy this contract into each build spec's section of the plan. The executor follows it.

**Rounds.** Rounds run per spec, after its development packages are certified and before its
delivery package. N is a ceiling, not a quota. The plan holds a hardening log (in the saved plan,
or in the host's plan in Plan mode) so each round can read earlier dispositions.

**Reviewer.** Each round uses a fresh independent subagent: not a developer, not the orchestrator,
and not an earlier round's reviewer.

- Give it the spec, its acceptance criteria, the stated project and quality rules, the resulting
  artifacts and diff, and the certification evidence.
- Never give it the developers' narrative conclusions.
- It returns findings, each with a class, evidence and a location. "No findings" is a valid result.

**Classes.** A borderline finding, or one the reviewer labels with two classes, takes the higher.

| Class | Test |
| ----- | ---- |
| **IMMINENT** | Definite data loss, a business-continuity risk, or a terrible user experience. |
| **COMPLIANCE** | Delivered without following the spec, the supplied requirements, or the implementation or quality rules known to apply. |
| **BEST-PRACTICE** | Any relevant business or technology expert would agree a good solution would not behave this way. |
| **EDGE** | Clearly a good idea, but neither a show-stopper nor an MVP element. |

**Triage.** The orchestrator verifies every finding against its evidence.

- IMMINENT and COMPLIANCE findings are always fixed.
- Before refuting or downgrading one, present it to the user with the evidence and wait for the
  decision. Do not act on a refutation alone.
- Weigh each BEST-PRACTICE and EDGE finding against its risk and its fit with current objectives.
  Fix it, or log it yourself to the project's wiki backlog through wiki-master:wiki-project.
  Record the reason either way.
- Enter every disposition in the hardening log: round, finding, class, verification, disposition,
  reason and any backlog link.

**Remediation.** Every fix follows the same TDD, dev and certification triple.

- The original developer agent makes it where it is still available, continued in place with its
  context intact (for example through SendMessage).
- Otherwise a fresh developer agent makes it, given the original package brief, that package's
  certification evidence and the findings.
- The new certification evidence goes to the next round.

**Stopping.**

- **Early stop:** after a round with no IMMINENT or COMPLIANCE findings, once its BEST-PRACTICE
  and EDGE items are dispositioned, stop hardening and go to delivery, even if rounds remain.
- **Otherwise** the next round reviews the fixed work.
- **Rounds used up:** continue to delivery, unless another round is VERY LIKELY to surface further
  IMMINENT items. Evidence of that: the final round found an IMMINENT item, or an IMMINENT fix
  landed in code no later round has reviewed.
- **In that case, pause before delivery**, state the evidence, and ask the user for more rounds or
  for permission to deliver.

## Evidence

Read [the evidence reference](references/evidence.md) when a rule needs justifying or the skill is
being revised. The stage order, the sanity-check lenses, the finding classes and the stopping rules
are workflow choices; the sources support their rationale rather than prove this exact procedure.
