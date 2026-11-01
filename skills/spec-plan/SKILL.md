---
name: spec-plan
description: Produces wiki-grounded specifications and reviewable plans for one or more changes, with standard or enhanced rigor.
when_to_use: Use when asked to spec, scope or write up features, changes or spikes before building them; to preload specs on the roadmap; or to plan one or more ready specs, including "/plan the spec" and "/plan the ready specs".
argument-hint: "[rigor=standard|enhanced] [request]"
---

# Spec and Plan

Turn the user's intent into a settled specification, then a plan ready for handoff. This
skill uses wiki-master for project grounding and saving the spec, and assumes subagents
are available. Implementation belongs to the subsequent workflow, so finish at handoff.

## Prerequisites

Start with wiki-master available and the host outside plan mode, so the skill can ground and
save its artifacts. If either prerequisite is unmet, stop the skill and tell the user which
conditions apply: wiki-master is unavailable, plan mode is active, or both. Explain that they
can invoke the skill again once wiki-master is available and they have left plan mode.

## Rigor

Accept `rigor=standard` or `rigor=enhanced` anywhere in the arguments; the remainder is the
request. Carry the selected rigor from the spec into the plan unless the user changes it.
When it is unspecified, ask in the first interview batch, recommending standard for routine
work. **Standard** uses the spec and plan procedures below. **Enhanced** adds the fresh-agent
spec review and the planned work-package reviews described in their respective sections.
The user may select either enhancement individually; record the selection and its reason.
For a batch, use the requested rigor as the default for new specs and record any per-spec
choices. Preserve each saved spec's rigor when planning a set unless the user changes it.

## Stage 1: Spec

**Preload one or more specs.** Use the project's existing wiki backlog as the queue. Give
each independent goal its own saved spec and apply this stage to every requested goal,
reusing shared interview answers while settling each spec's own decisions. Complete the
requested batch before the final handoff; creating or reviewing specs prepares the queue
for later planning. Specs can also accumulate across sessions. Record dependencies as links
to other specs with the required outcomes or interface contracts, so later planning can
order them without relying on conversation memory.

1. **Shape the requested spec.** Use the [spec template](references/spec-template.md),
   including the sections that help settle a decision or make the outcome checkable.
   Scale the detail to the change so even a small spec stays useful and concise.
2. **Interview around the missing decisions.** Reuse answers and authorization already in
   the conversation. Ask remaining questions in small batches of two to four, or fewer when
   fewer remain or the question tool has a lower limit. Give recommended defaults. Cover the
   goal and user-visible outcome, scope, constraints, acceptance, build versus spike, and
   applicable delivery requirements and authorization. Include the rigor choice when needed.
   Wait for answers before drafting dependent content; when the user delegates a choice,
   record the chosen default as an assumption. Small batches make decisions easier to answer.
3. **Ground the request in the wiki.** Find the project through its overview's `repo:` field;
   ask for the project slug if needed. Delegate a search using wiki-master:wiki-search for
   relevant knowledge and roadmap items. Report coverage and gaps. When coverage is light,
   propose wiki-master:wiki-discover and wiki-master:wiki-ingest for the named gaps, using
   existing authorization where given. Grounding keeps the spec connected to prior decisions.
4. **Settle roadmap overlap with the user.** Recommend adopting a matching item, grouping
   related items with the same goal as work packages, or linking out-of-scope items as
   non-goals. Ask about unresolved conflicts. Give independent goals separate specs. Keep
   absorbed items discoverable with `Specced in [[<spec>]] (WP-n)` on their roadmap entries.
5. **Explore the code read-only through subagents.** Establish real files, interfaces,
   commands and current behavior. Keep the findings that affect design or acceptance.
   Have exploration identify the available project skills and plugins that fit the work;
   propose them together in one structured question, each with a reason and relevant
   packages, and record the user's confirmed selection. Use further interview batches for
   decisions the evidence raises. Concise reports preserve the orchestrator's context for
   decisions rather than repository traversal.
6. **Choose review depth deliberately.** Recommend enhanced spec rigor when assumptions,
   consequential constraints or complex requirements need an independent reading. Recommend
   enhanced plan rigor for packages involving shared contracts, security, data handling,
   concurrency or changes that are hard to reverse. Put applicable suggestions together in
   one interview question; carry forward accepted and declined choices so the user decides
   each once. Enhanced rigor already selects both enhancements.
7. **Turn experimental unknowns into a spike spec.** State risk-ordered Given/When/Then
   questions, observable results, and validated, partial or invalidated verdicts with
   deliverables and promote-or-discard criteria. Use the user's effort budget when supplied;
   otherwise state "no timebox; stops at the first met exit criterion". The deliverable here
   is the experiment's specification, which makes its eventual result useful to the next decision.
8. **Resolve the spec's decisions and check its criteria.** Apply the decision and spike
   checks under Spec handoff before saving. Record user-delegated choices as explicit
   assumptions. For each acceptance criterion, open the artifact or template
   it reads and record what it can actually show; write the criterion at that level. Where
   an artifact is new, identify its planned shape and observable result explicitly. This ties
   acceptance to evidence a later reader can obtain.
9. **Save the specification.** Use wiki-master:wiki-author to save it at
   `wiki/authored/<project>/backlog/<slug>.md`, with `kind: backlog-item` and
   `backlog-status: planned`. Write outcomes and high-level design, with acceptance expressed
   as runnable commands and expected output or repeatable observations. Give work packages
   clear ownership, dependencies and self-contained briefs. Include applicable delivery
   requirements as planned work, using the project's procedure and settled authorization.
   Record rigor, any stage-specific selections, confirmed tools and the corresponding package
   Tools lines. Persistence gives the planner a stable starting point.

### Enhanced spec rigor

Review the saved draft before handing it to planning. Start a **fresh agent for this review
alone**, separate from the spec author and orchestrator, with the user request, interview
decisions, saved spec path and relevant evidence. An independent reading can catch assumptions
the author has become accustomed to.

Ask the reviewer to check that the spec captures the user's decisions, accurately describes
the existing code, resolves dependencies and makes acceptance observable. Have it inspect the
referenced artifacts and check acceptance commands that are safe and meaningful before a build;
record expected baseline failures and checks that require future work as such. The review
returns findings with evidence and locations, plus PASS or changes needed. The author revises
the spec and obtains a fresh-agent recheck of confirmed findings. Questions that need the
user's decision return to the interview. Record the review outcome and any pending findings
in the spec's Rigor section so planning inherits the actual state of review.

### Spec handoff

**Settle decisions before handoff.** Confirm that a fresh agent can begin each work package
without needing another decision about scope, behavior, interfaces, dependencies, acceptance
or authorization. Resolve those decisions with the user and record the answers as statements.
Replace placeholders, open questions and "decide during implementation" instructions with
settled choices. Keep routine implementation details within those choices for the implementing
agent to determine.

**Make spike uncertainty explicit.** A spike may contain questions it is designed to answer.
Settle the experiment's method, observable outcomes and exit criteria before handoff. When
its findings determine a later build decision, plan the spike first and complete the affected
build plan after its verdict.

Confirm that decisions, tools and rigor selections are recorded and any selected spec review
has passed, or that the user has explicitly changed the selection. For a batch, apply these
checks independently to each spec, with a fresh reviewer for each selected spec review.
Link the saved specs and summarize each scope and whether it is ready for planning. Identify
any draft still awaiting a decision or review separately; readiness follows from these checks,
not a new backlog status. Close with "When you're ready, tell me `/plan the spec`." For a set,
use "When you're ready, tell me `/plan the ready specs`, or name the specs you want planned."

## Stage 2: Plan

1. **Select the ready specs.** Find queued backlog items with a `For the planner` section
   and status planned or in-progress. Use the named specs, the sole ready spec, or all ready
   specs in the current project when the user asks for that set. Otherwise list the ready
   candidates with their scope and rigor and ask which to plan together, supporting multiple
   selections. Read each spec's decisions, dependencies and Rigor section and recheck the
   handoff conditions against the current repository. A saved draft or planned status alone
   establishes neither settled decisions nor a passed review. Report pending candidates and
   their reasons separately. For an explicitly requested spec with gaps or an affected review,
   return to Stage 1 to settle it before including it in the final plan. For in-progress specs,
   establish the remaining scope from recorded results and preserve ongoing work.
2. **Reconcile the selected set.** Resolve cross-spec contradictions, dependency cycles,
   missing prerequisites and shared-interface decisions through the spec interview, updating
   affected specs and reviews before handoff. A prerequisite may be an already verified result
   or another selected ready spec with a settled output contract. A build decision depending
   on an unresolved spike waits for its verdict. Produce one combined plan with a section per
   spec, in the user's selected order where dependencies permit; state any required reordering.
   Keep specs sequential, with parallel groups inside each spec, so later work can account
   for earlier changes to shared files. This preserves separate goals while coordinating them.
3. **Translate packages into concrete steps.** Name each source spec and its selected rigor.
   Qualify package IDs with the spec slug, such as `csv-export/WP1`, so dependencies and review
   findings identify the right package across the set. Preserve each spec's acceptance criteria.
   Carry each package's brief, owned files, dependencies, done-when and confirmed tools into
   its plan step. Add technical steps appropriate to the current code and the spec's scope.
   Include applicable verification and delivery requirements from the spec as future work.
   Apply the Enhanced plan rigor section below to every package selected for review.
   Keep each step traceable to a requirement or package so the user can assess coverage.
4. **Plan delegation around context and dependencies.** Default to subagents for work
   packages, scheduling independent packages in parallel and passing self-contained briefs.
   Specify concise reports of changed artifacts, checks and blockers so the orchestrator
   preserves context for coordination. Give concurrent packages disjoint file ownership;
   sequence shared-file changes and dependencies explicitly. When tight coupling or another
   concrete constraint demands a different approach,
   state the exception and its reason in the plan. This makes parallelism purposeful.
5. **Make the plan reviewable and hand it off.** Check that the plan covers every selected
   spec's acceptance criteria, settled constraints and selected rigor. Apply the same decision and
   spike checks from Spec handoff to the resulting plan, so each package can begin with its
   execution-informing decisions settled. Present the plan in the
   reply or the project's designated plan artifact. End with
   "The spec and plan are ready for handoff," or "The selected specs and combined plan are
   ready for handoff." This completes the skill's scope; the saved specs remain available
   for later use and their backlog status stays unchanged by planning.

### Enhanced plan rigor

Build **fresh-agent work-package review into the plan**, after each package's work and before
dependent packages consume it. These are scheduled reviews of the eventual work products;
this stage produces their briefs and placement in the plan.

For each package, specify a new reviewer distinct from its author and the orchestrator,
given the package brief, relevant spec criteria and resulting artifacts. Ask that reviewer
to check correctness, scope and acceptance against the artifacts, with evidence-linked
findings. Keep the author's conclusions separate from the review inputs so the reviewer
forms an independent assessment. State that confirmed findings need resolution and a fresh
review before dependent work proceeds. For a delivery package, place the review of prepared
delivery artifacts before the outward-facing action. This review dependency makes enhanced
rigor part of the work plan rather than a vague promise of extra care.

## Evidence

Read [the evidence reference](references/evidence.md) when a rule needs justification or the
skill is being revised. It preserves the supporting synthesis, source links and limitations.
The stage boundaries and the two enhanced rigor contracts are workflow choices; the sources
support their rationale rather than establishing this exact procedure experimentally.
