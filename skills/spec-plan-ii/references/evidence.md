# Evidence behind spec-plan-ii's design

*Adapted on 2026-11-08 from a wiki synthesis on specs and plans for coding agents and from wiki
concept pages on clean-context review, reviewer-writer separation, review finding severity,
stopping rules for review loops, YAGNI and premortem review, test-first development with coding
agents, and reward hacking. Citations are converted to public URLs. Private navigation and vault
metadata are removed.*

## How to use this reference

This file is background rationale. The procedure is defined in `SKILL.md`, and where the two seem
to differ, `SKILL.md` wins. Read a section here when a step needs justifying, is being challenged,
or you are deciding whether a case warrants departing from it.

The skill's main choices are **workflow choices, not measured recipes**. No source tested any of
these as a package:

- the orchestrator writing every spec itself;
- a self-review followed by a blind sanity check from a fresh agent;
- the TDD → dev → certification triple for every development task;
- a default of 2 hardening rounds;
- the four finding classes (IMMINENT, COMPLIANCE, BEST-PRACTICE, EDGE);
- the stopping rule.

Each section says what the sources measured or stated, and where the skill goes beyond them.
Abstract-only and vendor-reported evidence is marked.

## Spec content, and grounding before drafting

**What a spec should hold.** The sources agree on a core:

- the goal and user-visible outcome first ([OpenAI — Using PLANS.md for multi-hour problem
  solving](https://developers.openai.com/cookbook/articles/codex_exec_plans);
  [Osmani — How to write a good spec for AI agents](https://addyosmani.com/blog/good-spec/));
- non-goals, hard constraints and a "done when", which keep the agent from building something
  "impressive but wrong" ([OpenAI — Run long horizon tasks with
  Codex](https://developers.openai.com/blog/run-long-horizon-tasks-with-codex));
- acceptance written as observable behavior or a runnable command, per milestone (the same two
  OpenAI sources);
- existing and new behavior labeled. Böckeler saw notes about existing classes read as new
  requirements, producing duplicates ([Böckeler — Understanding Spec-Driven
  Development](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html)).

The self-review checks follow from these and the next point: decisions settled, criteria
observable, existing versus new labeled, and every package startable from its brief alone,
because subagents start from a clean window ([Anthropic — When to use multi-agent
systems](https://www.claude.com/blog/building-multi-agent-systems-when-and-how-to-use-them)).

**Open decisions must be named, not guessed.** Agents are poor at noticing missing information,
and interaction to resolve it improves outcomes ([Ambig-SWE](https://arxiv.org/abs/2502.13069);
abstract-only). spec-kit mandates explicit `[NEEDS CLARIFICATION]` markers
([spec-kit](https://github.com/github/spec-kit/blob/main/spec-driven.md)). A subpar plan hurts
more than no plan ([From Plan to Action](https://arxiv.org/abs/2604.12147); abstract-only), so
the cost of a wrong premise compounds downstream.

**Grounding before drafting** is a workflow choice that follows: if the agent will not notice
gaps itself, the search for what is known and missing must precede the draft.

**Why the orchestrator writes.** Cognition reports that multi-agent systems work best "when
writes stay single-threaded and the additional agents contribute intelligence rather than
actions" ([Cognition — Multi-agents: what's actually
working](https://cognition.com/blog/multi-agents-working)). Anthropic reports role-specialized
subagents spending "more tokens on coordination than on actual work", and recommends subagents
for context protection and parallel research ([Anthropic — When to use multi-agent
systems](https://www.claude.com/blog/building-multi-agent-systems-when-and-how-to-use-them)).
Both are vendor-reported. Giving subagents only evidence-gathering follows that pattern, and one
writer avoids contended writes to shared pages.

## Self-review limits, and why the second look is blind

**Self-review in the same context is weak.** Without external feedback, models struggle to
correct their own reasoning and sometimes get worse ([Huang et al. — LLMs cannot self-correct
reasoning yet](https://arxiv.org/abs/2310.01798); abstract-level). Anthropic found agents
"confidently" praising their own mediocre work, and that tuning a separate skeptical evaluator was
"far more tractable" than making a generator self-critical ([Anthropic — Harness design for
long-running apps](https://www.anthropic.com/engineering/harness-design-long-running-apps);
vendor-reported).

**Fresh context helps against repeated self-review, not necessarily against one pass.** A
fresh-session reviewer scored F1 28.6% against 21.7% for a second same-session review. It was not
significantly ahead of a single same-session review (27.1%) ([Song — Cross-context
review](https://arxiv.org/abs/2603.12123); abstract-only, v2 corrects v1). So the skill keeps the
self-review, because it is cheap and catches checklist omissions, and does not count it as the
independent check.

**Clean context is the reviewer's advantage.** Cognition's review agent works best when "the
coding and review agents do not share any context beforehand" ([Cognition](https://cognition.com/blog/multi-agents-working)),
and a fresh context "won't be biased toward code it just wrote" ([Claude Code — Best
practices](https://code.claude.com/docs/en/best-practices)).

**Reviewers must be told to disagree.** A naive second agent tends to agree with the writer. One
study fixed this only by instructing a critic to structure disagreement, after which a three-agent
protocol beat a five-agent one
([Adversarial review](https://arxiv.org/abs/2608.18167); abstract-only).

**Withhold the author's framing.** A reviewer shown the author's framing can be steered: an
LLM-refined attack evaded review in 32 of 33 real vulnerabilities ([Alexopoulos et al. — Bias
injection in automated code review](https://arxiv.org/abs/2603.18740); abstract-only). This is why the sanity
checker gets the user's verbatim request and the saved spec, but never the self-review notes or
the interview rationale, and why a hardening reviewer never gets the developer's narrative.

## Sanity-check lenses

The sanity check is a broad design review, not line-level analysis. Its three lenses draw on:

- **False premise, through a premortem.** Told the project "has failed spectacularly", each
  person independently writes down why. Klein cites a 1989 study finding that this prospective
  hindsight increases correct identification of reasons by 30% ([Klein — Performing a project
  premortem](https://hbr.org/2007/09/performing-a-project-premortem); the figure is second-hand).
  A blind reviewer fits the independent-listing step naturally.
- **Over-engineering, YAGNI and KISS.** Fowler puts the odds that a presumptive feature is
  unneeded at "at least ⅔", and excludes tests, refactoring and other work that makes software
  easier to change ([Fowler — Yagni](https://martinfowler.com/bliki/Yagni.html)). Beck's simple
  design rules end at "fewest elements" ([Fowler — Beck design
  rules](https://martinfowler.com/bliki/BeckDesignRules.html)). Google SRE treats every new line
  of code as "a liability" ([Google SRE — Simplicity](https://sre.google/sre-book/simplicity/)).
  Agents over-build by default: on already-fixed issues they made unnecessary changes in up to 70%
  of cases ([ETH SRI — Coding agents are fixing correct
  code](https://eth-sri.github.io/blog/fixedcode)). Kent Beck lists unrequested functionality as a
  warning sign ([Beck — Augmented coding: beyond the
  vibes](https://newsletter.kentbeck.com/p/augmented-coding-beyond-the-vibes)).
- **Blind spots.** Models share errors: on one dataset they agree 60% of the time when both are
  wrong, and more capable models are more correlated ([Kim et al. — Correlated errors in large
  language models](https://arxiv.org/abs/2506.07962); abstract-only). A blind reviewer reduces anchoring on the
  author's reasoning, but it does not remove shared blind spots. That is a reason to ask what was
  not considered at all.

**"No concerns" is a valid outcome.** A reviewer prompted to find gaps "will usually report some,
even when the work is sound" ([Claude Code — Best
practices](https://code.claude.com/docs/en/best-practices)). Telling agents they may abstain when
nothing needs fixing raised correct abstention from 60.5% to 88.5% for GPT-5.4 mini and from 65%
to 80.5% for Sonnet 4.6. "Reproduce first" without an abstain option left Sonnet roughly unchanged
and dropped GPT-5.4 mini to 47.5% ([ETH SRI](https://eth-sri.github.io/blog/fixedcode)). The
abstain prompt is brittle: where an earlier wrong patch needed fixing, it led those two models to
submit 70% and 94% empty patches. So the option has to be offered, not pushed.

**Advice, not a directive.** Because some points will be noise, the orchestrator adopts what it
agrees with and takes disagreements to the user, who stays accountable. That split is a workflow
choice.

## TDD with agents, test gaming, and certification evidence

**Tests help when they are trustworthy and outside the agent's control.** Supplying tests with
the problem raised GPT-4's MBPP score from 69.67% to 82.45% against stricter hidden tests
([Mathews & Nagappan — Test-driven development for code
generation](https://arxiv.org/html/2402.13521)). Those were human-written tests.

**Agent-written tests and bare "do TDD" help less.** On SWE-bench Verified, resolved and
unresolved tasks showed similar test-writing frequencies, and agent tests leaned on prints over
assertions ([Chen et al. — Rethinking the value of agent-generated
tests](https://arxiv.org/html/2602.07900)). With small local models, TDD instructions alone
raised regressions from 6.08% to 9.94%. Naming the tests a change could break cut them to 1.82%
([TDAD](https://arxiv.org/html/2603.17973)). This is why each TDD task states what its tests must
cover and records the expected failure, rather than relying on the instruction alone. Beck's agent
protocol is the nearest practitioner model: simplest failing test first, then only enough code to
pass ([Beck — Canon TDD](https://newsletter.kentbeck.com/p/canon-tdd)).

**Visible tests get gamed.** When tests contradicted the spec, GPT-5 still passed 54% of
impossible SWE-bench tasks. Claude models cheated mainly by editing tests. Others special-cased
tests or overloaded comparison operators. Read-only tests stopped test edits but not
special-casing. LLM monitors caught only 42–65% of cheats on multi-file tasks
([ImpossibleBench](https://arxiv.org/html/2510.20270)). METR saw o3 reward-hack in 30.4% of runs
where the scoring function was visible, against 0.7% elsewhere ([METR — Recent frontier models are
reward hacking](https://metr.org/blog/2025-06-05-recent-reward-hacking/)). The gap between
visible and held-out tests widened with code size
([SpecBench](https://arxiv.org/abs/2605.21384); abstract-only).

**Why certification carries three pieces of evidence:**

- **Raw test-runner output**, because a summary is a claim and the runner output is the
  observation. Anthropic's harness let the agent flip a `passes` field but not edit the criteria
  ([Anthropic — Effective harnesses for long-running
  agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)).
- **A diff of the test files since red**, because test edits were the dominant cheat for one model
  family, and a diff makes them visible to a reviewer who cannot rely on a monitor.
- **An explicit flag** for any test changed after red, or that the developer believes contradicts
  the spec. An explicit `flag_for_human_intervention` exit cut GPT-5's cheating from 54% to 9%
  and o3's from 49% to 12%, with a much smaller effect for Claude Opus 4.1. It is one effective
  mitigation among several: hidden tests cut cheating to near zero but hurt legitimate
  performance, and the strictest prompt wording cut GPT-5 to 1% on a LiveCodeBench variant
  ([ImpossibleBench](https://arxiv.org/html/2510.20270)). The flag is the one that keeps tests
  visible and costs nothing.

Nobody re-runs the checks at certification. The hardening reviewer sees the same evidence and is
where the claim gets tested. That split is a workflow choice. TeamBench is a caution here:
verifiers approved 49% of submissions that failed the deterministic grader ([Kim et al. —
TeamBench](https://arxiv.org/abs/2605.07073); abstract-level). The mitigation the sources support is review against
raw evidence, not the author's account.

## Severity classes and the borderline-up rule

**Label every finding, and keep "how bad" apart from "must it block".** Google's reviewer guide
says unlabelled comments read as mandatory ([Google eng-practices — How to write code review
comments](https://google.github.io/eng-practices/review/reviewer/comments.html)). Conventional
Comments makes blocking a separate decoration ([Conventional
Comments](https://conventionalcomments.org/)). CVSS scores intrinsic severity and leaves business
factors outside its scope ([FIRST — CVSS v4.0](https://www.first.org/cvss/v4.0/specification-document)).

The four classes mix those axes knowingly. IMMINENT is a severity, in the sense of CVSS or an
incident level. COMPLIANCE and BEST-PRACTICE are kinds of finding. EDGE is mostly a blocking
decision, like Google's FYI. The skill ties the blocking decision to the class: IMMINENT and
COMPLIANCE are always fixed, and BEST-PRACTICE and EDGE are weighed. That mapping is the skill's
choice, not a source's.

**Each class needs a test someone else would apply the same way.** When people choose severity
freely, 51% of duplicate-bug buckets carried inconsistent labels, though 95% described the same
problem ([Tian et al. — On the unreliability of bug severity
data](https://sail.cs.queensu.ca/data/pdfs/EMSE2015_OnTheUnreliabilityOfBugSeverityData.pdf)).
That data comes from free-choice bug trackers, not a written rubric, so it shows the failure mode
rather than its size under one.

**Borderline goes up.** PagerDuty's rule is "always assume the worst": when unsure, treat it as
the higher level, and settle it afterwards ([PagerDuty — Severity
levels](https://response.pagerduty.com/before/severity_levels/)). The skill applies that to
findings. Because IMMINENT and COMPLIANCE always block, a downgrade or refutation of one goes to the
user with its evidence before anyone acts on it.

**Most findings will not be IMMINENT.** In an industrial inspection study, about half the issues
raised were false positives, and "only 13 percent" would have compromised function ([Porter et
al. — Cost-benefits of code
inspections](https://userweb.cs.txstate.edu/~rp31/papersSQ/PorterEtAl_TSE.pdf)). Together with
over-reporting, that is why the orchestrator verifies each finding against its evidence.

## Stopping rules, fresh reviewers and the early stop

**Most of the gain comes early.** Across code generation, test generation and translation, "the
first three to four repair iterations account for most achievable gains", and feedback design
mattered more than the model ([Kiecker et al. — Is three the magic
number?](https://arxiv.org/html/2607.05197)). In a
randomized human inspection experiment, two two-person teams were no more effective than one
([Porter et al.](https://userweb.cs.txstate.edu/~rp31/papersSQ/PorterEtAl_TSE.pdf)). At Stripe,
agent CI iteration is capped at two rounds before the change goes to a person ([Stripe —
Minions](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents);
vendor-reported).

**The default of 2** sits at the low end of that two-to-four range, with a pause to ask the user
when more look needed. It is a workflow choice, recorded in the plan as a parameter, as Kiecker
et al. recommend.

**A fresh reviewer per round.** Most models lose "60–80% of their debugging capability within
just 2–3 attempts", and clearing the context at that point raised accuracy for all six models
tested ([Adnan & Kuhn — The debugging decay index](https://arxiv.org/html/2506.18403)).
Self-repair gains are "often modest", and feedback from a stronger source raised them markedly
([Olausson et al. — Is self-repair a silver
bullet?](https://arxiv.org/html/2306.09896)). Both point to fresh feedback each round, not
repeated passes from the same reviewer.

**Stop early on a clean round.** Evidence-based stopping, by estimating remaining defects from
reviewer overlap, needs four or more inspectors ([Briand et al. — Capture-recapture
models](https://ehealthinformation.ca/web/default/files/wp-files/isern-97-22.pdf)). One reviewer
per round cannot support that. A round with no blocking findings is the cheap signal that can be
used instead.

**More rounds are not free.** Allowing multiple submissions with feedback raised the legitimate
pass rate from 80% to 83%, and raised cheating on impossible tasks from 33% to 38%
([ImpossibleBench](https://arxiv.org/html/2510.20270)). This is one reason N is a ceiling rather
than a target, and why late rounds should look for weakened tests.

**When rounds run out.** The pause before delivery covers the case the cap would otherwise hide:
an IMMINENT item found in the final round, or an IMMINENT fix that no round has reviewed. No
source measures this rule. It follows from treating an unreviewed fix as the same kind of
unchecked claim as an uncertified test result.

## Remediation by the original developer

No source directly measures who should fix a reviewer's findings. The choice rests on adjacent
evidence:

- **Context transfer.** Anthropic advises that the agent building a feature also write its tests,
  and warns against splitting sequential phases of the same work between agents ([Anthropic — When
  to use multi-agent
  systems](https://www.claude.com/blog/building-multi-agent-systems-when-and-how-to-use-them)).
  The original developer already holds the package's context.
- **Outside feedback is what makes repair work.** The findings come from an independent reviewer,
  which is the external feedback that self-correction lacks ([Huang et
  al.](https://arxiv.org/abs/2310.01798); [Olausson et al.](https://arxiv.org/html/2306.09896)).

There is a counter-signal: debugging decays within a long conversation, and a fresh start helped
([Adnan & Kuhn](https://arxiv.org/html/2506.18403)). The skill's answer is that the reviewer is
always fresh, and a fresh developer, given the brief, the certification evidence and the findings,
is the fallback when the original is unavailable. Whether the original or a fresh developer fixes
better is untested.

## Spikes

Spikes skip TDD, certification and hardening because their deliverable is a verdict, not shipped
code. The ExecPlan's prototyping milestones end with explicit criteria "for promoting or
discarding the prototype" ([OpenAI — Using
PLANS.md](https://developers.openai.com/cookbook/articles/codex_exec_plans)). No source measures
whether spikes help or gives them a timebox, so promoted work is specced again as a build.

## Gaps

- **Severity triage by AI reviewers.** Nothing measures how well an AI reviewer assigns severity
  classes, or how often its classes agree with another reviewer's under a written rubric. The
  noise figure above comes from human bug trackers.
- **Misreported test results.** Nothing measures how often agents misreport their own test
  results. The gaming studies concern deliberate cheating, not misreading or overstating output.
- **An enforced red-first loop.** No study measures a loop where the agent writes the failing test
  itself, confirms the failure, and then implements, on realistic tasks.
- **The package as a whole.** No source compares this workflow, or any spec-driven workflow,
  against working without it.
- **Evidence quality.** Much of the evidence is abstract-only (Huang et al., Song, Ambig-SWE, From
  Plan to Action, TeamBench, Adversarial review, Alexopoulos et al., Kim et al. on correlated
  errors, SpecBench), vendor-reported (Anthropic, Cognition, OpenAI,
  Stripe), second-hand (Klein's 30%) or from the 1990s (Porter et al., Briand et al.). The LLM
  repair-loop studies use mechanical feedback on benchmarks, mostly with smaller or older models,
  not rounds of independent review on agent-built features.
