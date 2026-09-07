# Rubber duck: should hartye-skills add a pre-commit SKILL.md validation hook?

- **Date:** 2026-09-07
- **Model consulted:** `gpt-6-astra` via Codex CLI, `model_reasoning_effort=high`, sandbox `read-only`
- **Question asked:** I am leaning toward adding a git pre-commit hook to `hartye-skills` that
  mechanically validates every `skills/*/SKILL.md` — (a) `description` length bounds, (b)
  frontmatter `name` matches the containing directory, (c) reference-file nesting depth. My
  instinct says it is a good idea but something feels off and I cannot articulate what. The brief
  asked six specific questions: (1) is the hook consistent with CLAUDE.md's own admission criteria
  and graduation rule; (2) rank checks (a)/(b)/(c) on mechanical checkability, correlation with
  skill quality, and false-positive/negative profile; (3) what breaks in six months; (4) is there a
  category error in validating prose with a hook, given yoda's premise that inspection cannot
  distinguish a well-written skill from a helpful one; (5) where is the check better placed
  (yoda itself, manual script, release-time, nowhere); (6) what am I not asking that I should be.
  Explicit license to disagree and to say "don't build this at all" was given.

Response recorded verbatim and unedited below.

---

**I would not build the proposed commit hook.** Keep name/directory agreement, retain description limits only against an explicit compatibility contract, and drop nesting depth as a blocking check. Put the narrow validation at release time.

I read all four skills, yoda’s evidence file, the manifests, authoring rules, README, and relevant history. The four skills total 772 lines. One correction: commit `49c7052` removed CI-checking language from `ship-it`; it did not remove a CI workflow. That does not change your constraint against adding CI.

**1. Is the hook consistent with the admission criteria and graduation rule?**

**Yes, a repository-development Git hook is consistent with their literal scope.** Using the graduation rule to reject it would misread the rule.

[CLAUDE.md](C:/Users/ehart/repos/hartye-skills/CLAUDE.md:8) introduces the criteria with:

> Before adding a skill, it must clear all three:

It then requires:

> **Cross-application** - useful in 2+ unrelated projects.

> **Self-contained** - no shared state or load-order dependency on other skills in this plugin.

> **Small** - a `SKILL.md` plus, at most, a script or a reference file.

The [graduation rule](C:/Users/ehart/repos/hartye-skills/CLAUDE.md:15) says:

> the moment a skill needs hooks, an MCP server, persistent storage, or a UI, it has outgrown this repo.

The subject is **a skill**. A maintainer’s pre-commit hook does not make an installed skill depend on hooks. Shipping plugin hooks that a skill needs would cross that boundary.

There is a proportionality question—whether development machinery earns its place around four prose files—but no literal prohibition. “This violates graduation” is the first argument against the hook I tried, and it fails.

**2. How defensible are the three checks?**

**(a) Description length: mechanically checkable, provided you define the contract.**

“Within some bound” is not a requirement yet. Two different constraints currently exist:

- The Agent Skills specification requires a nonempty description of at most **1,024 characters**. [Specification](https://agentskills.io/specification)
- Claude Code’s listing normally caps the **combined `description` and `when_to_use`** at **1,536 characters**; that cap is configurable. [Claude skills documentation](https://code.claude.com/docs/en/skills#skill-descriptions-are-cut-short)

A correct checker parses the actual YAML frontmatter and measures the resulting string. Counting physical lines or bytes is different. Yoda itself contains example `description:` and `when_to_use:` fields inside its body, so a whole-file grep already encounters misleading matches in this repository.

This check protects format compatibility or visibility of metadata. It does **not** establish a useful description.

- **False positives:** an arbitrary short cap rejects useful trigger distinctions; a substantial minimum rewards padding. A byte counter rejects some descriptions that satisfy a character limit.
- **False negatives:** a short, vague description passes. So does a procedural synopsis that competes with the body. Checking only `description` misses overflow caused by `when_to_use` and says nothing about competition across installed skills.

**Keep a documented compatibility limit. Drop an invented brevity threshold.**

**(b) Name matches directory: the strongest check.**

This is precisely checkable after parsing YAML. It enforces an explicit repository and specification contract.

Its value is identity consistency, portability, and predictable command naming—not helpful instructions. Yoda correctly distinguishes a mismatch from an automatic Claude load failure: plugin naming can produce a different command name. [Yoda’s contract comparison](C:/Users/ehart/repos/hartye-skills/skills/yoda/SKILL.md:200)

- **False positives:** essentially none against the repository’s explicit equality rule, with a correct implementation. An intentional Claude alias can work while violating this repository rule.
- **False negatives:** every ineffective skill whose name matches passes; renaming the directory and field together can also leave README examples or external references stale.

**Keep it.** Its narrowness is a virtue because its result means something definite.

**(c) Reference nesting: drop it as a blocking check.**

Your wording suggests filesystem depth. Yoda’s rationale concerns **reference chains**. Those are different measurements. Its evidence file explicitly calls the rule “Reference chains exactly one level deep.” [Evidence](C:/Users/ehart/repos/hartye-skills/skills/yoda/references/evidence.md:213)

For example:

```text
SKILL.md → references/vendor/v2/details.md
```

That is one navigation hop despite nested directories.

```text
SKILL.md → a.md → b.md
```

That is two hops despite flat directories.

Filesystem depth is easy to calculate and poorly matched to the claimed failure mechanism. A link graph is more relevant, but still cannot reliably distinguish required reading from citations, optional background, examples, or instructions expressed without Markdown links.

- **False positives:** direct links into well-organized folders; harmless citations inside a reference; deliberate conditional reading.
- **False negatives:** flat-file reading chains; required material mentioned only in prose; a directly linked file that the agent never opens.

Yoda also explicitly permits justified exceptions to these structural rules. [Yoda](C:/Users/ehart/repos/hartye-skills/skills/yoda/SKILL.md:163) Turning that guidance into an unconditional blocker changes the policy.

**Ranking: (b), then a contract-specific (a), then a distant (c).**

Existing-tool coverage is a substantive finding:

| Tool | What I verified |
|---|---|
| Agent Skills `skills-ref` | Its source implements the 1–1,024-character description check and name/directory agreement. It does not inspect reference chains. |
| `claude plugin validate` | The installed version, **2.1.263**, validates frontmatter parsing and field types. Its frontmatter-validation implementation does not implement these three proposed checks. |
| `/skill-doctor` | Reports listing cost and usage, including never-invoked skills. It is not a structural linter. |
| `claude plugin eval` | Installed CLI supports behavioral cases and a with/without-plugin baseline. It needs a meaningful eval suite; it does not infer one from these three properties. |

The reference validator also rejects unknown fields, including **`when_to_use`**, which your current `rubber-duck` uses. Adopting it wholesale would immediately reject a supported Claude extension. That would be a portability-policy finding, not proof the Claude skill is broken. [Validator source](https://raw.githubusercontent.com/agentskills/agentskills/main/skills-ref/src/skills_ref/validator.py), [skill-doctor documentation](https://code.claude.com/docs/en/skills#see-what-your-skills-cost-and-how-often-they-run)

**3. What breaks in six months?**

These are plausible failure scenarios, not predictions that all will occur:

- **The hook checks different content from the commit.** You stage bad metadata, repair it without staging, and the hook scans the repaired working tree. Green hook, bad commit. Conversely, an unfinished untracked skill blocks an unrelated commit. Your checkout currently contains an untracked `rubber-duck` directory, so this workflow distinction already matters.
- **A new checkout quietly lacks enforcement.** Tracking a hook script does not alone activate it. Installation and `core.hooksPath` become another convention to maintain. Pre-commit is also explicitly bypassable with `--no-verify`; it supplies automatic feedback, not an inviolable repository guarantee. [Git documentation](https://git-scm.com/docs/githooks)
- **The checker freezes the wrong limit.** An old threshold blocks useful descriptions, or a description-only check misses the combined listing constraint. Someone cuts valuable exclusions until the gate turns green, making skill collisions more likely.
- **The depth rule induces a cosmetic fix.** Files get flattened while reading chains remain, or reference material gets pasted into the body to avoid the rule. The metric improves while the intended architecture deteriorates.
- **Another rendered-instruction defect ships green.** This already has a close precedent: commit `9d7575d` fixed yoda’s length-check command because Claude substituted invocation arguments into an awk expression, producing `length(new)`. The command remained executable but wrong. All three proposed checks would have passed it.

Correct index handling and robust parsing are solvable. The objection is that “three cheap checks” omits the machinery needed to make their verdict accurately describe a commit.

**4. Is validating prose with a hook a category error?**

**No. Treating its result as evidence of usefulness is.**

Frontmatter is structured data embedded in prose. Mechanically checking it is entirely appropriate. You do not need a paired agent experiment to prove that a required field is absent.

Yoda’s premise is sound when read as a claim about **effectiveness**: inspection cannot establish the benefit the skill causes. It is too broad if interpreted as saying inspection establishes nothing useful.

The strongest argument **for** your hook therefore survives: deterministic checks catch objective mistakes cheaply and promptly, freeing review attention for behavior.

What does not follow is that these checks establish “skill quality.” A matching name, a 200-character description, and shallow references can accompany:

- a description that provides an attractive shortcut around the body;
- a skill that never activates;
- competing skills that both claim the same prompt;
- instructions that make the result worse.

The appearance-of-quality risk is real **if the green result substitutes for behavioral evidence**. It is not inevitable merely because a linter exists. The honest claim is “these metadata constraints passed.” Nothing stronger.

**5. Where should the check live?**

**Choose release time, tied to the existing version-bump ritual.**

[CLAUDE.md](C:/Users/ehart/repos/hartye-skills/CLAUDE.md:78) already identifies a useful boundary: agree the two manifest versions, update README, then tag. Validate the exact release candidate there, using an existing validator where its contract fits.

There is already more support than your proposal assumes: the installed `claude plugin tag` checks manifest/marketplace version agreement. I ran its **dry-run** mode; it refused the current uncommitted release changes and created no tag.

Against the alternatives:

- **Inside yoda:** little setup, but execution depends on the skill being invoked and its instructions followed. It also entangles reusable authoring advice with this repository’s release policy. Yoda can interpret findings; it should not be the only mechanism for deterministic enforcement.
- **A standalone manual script:** low complexity and useful during editing, but “remember to run it sometime” has no clear checkpoint. A manual command and release-time placement are compatible—the command is the mechanism, release is the occasion.
- **Pre-commit:** fastest feedback, and that is its strongest advantage. It adds installation and staged-content concerns and interrupts intermediate work. For four files and low commit volume, I would accept later feedback to avoid that coupling.
- **Nowhere:** zero setup or upkeep, but gives up objective compatibility checks that are useful independently of skill efficacy.

Release-time checking is still a ritual unless the release operation invokes it. I am not claiming it is impossible to skip. Its advantage is fitting the existing workflow and the artifact users receive, with fewer moving parts.

**6. What are you not asking?**

**“Are these settled requirements, and which demonstrated failure would enforcing them prevent?”**

The most important finding is that **your authoring contract already disagrees with itself**:

- [CLAUDE.md](C:/Users/ehart/repos/hartye-skills/CLAUDE.md:45): description says **“WHEN, never WHAT.”**
- [Yoda](C:/Users/ehart/repos/hartye-skills/skills/yoda/SKILL.md:74): capability in `description`, triggers in `when_to_use`; it later explicitly rejects the universal trigger-only interpretation.
- [Rubber-duck](C:/Users/ehart/repos/hartye-skills/skills/rubber-duck/SKILL.md:3) follows yoda’s approach.

This is an unresolved policy conflict, not merely a convention awaiting enforcement. All three proposed checks can pass while it remains unresolved.

Two further questions matter:

**“Are we checking what the agent actually receives?”** Your recent escaped defect occurred during rendering, after source-file inspection. Static metadata checks cannot reach that transformation.

**“Does the skill activate correctly, as well as help when activated?”** A forced with-skill/without-skill comparison measures benefit conditional on use. It does not, by itself, establish correct autonomous selection among competing installed skills. Realistic trigger prompts and near misses test a different property. Even a paired result is evidence for the sampled tasks and model, not permanent certification.

What feels off is this: **ease of measurement is being used to choose what deserves enforcement.** The proposed gate bundles a genuine identity invariant, an unspecified size policy, and a questionable structural proxy into one reassuring result.

Resolve the authoring-contract conflict first. Keep narrow compatibility validation at release. Spend the next unit of behavioral testing effort on failures like the one this repository has actually experienced.
