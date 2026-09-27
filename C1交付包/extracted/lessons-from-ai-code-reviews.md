# AI-Powered Entomology: Lessons from Millions of AI Code Reviews

# AI-Powered Entomology: Lessons from Millions of AI Code Reviews

## 1. The "Entomology" Metaphor: Bugs in the AI Era

Software bugs are no longer solely written by human hands. As AI agents write an increasingly large portion of production code, the velocity of code authoring has outpaced traditional human review bandwidth. Tomas Reimers presents "AI-Powered Entomology"—treating code review defects as biological specimens that need systematic classification, taxonomy, and targeted eradication.

## 2. The Two Axes of Effective AI Feedback: Reliability vs. Reception

Graphite's engineering team discovered that high model accuracy alone does not make an AI code review tool successful. Feedback must be evaluated across two critical dimensions:

- Reliability: Can the AI model deterministically and accurately spot the issue without hallucinations?
- Reception: Do developers actually want and appreciate this feedback from an AI reviewer, or does it trigger cognitive fatigue?

## 3. What AI Code Review Is Excellent At

- Logic & Boundary Bugs: Off-by-one errors, missing nil/null checks, and concurrency race conditions.
- Accidentally Committed Code: Hardcoded test secrets, leftover debug logs, and unfinished placeholder logic.
- Security & Performance Red Flags: SQL injection patterns, unindexed database queries, and redundant network roundtrips.

## 4. What Human Developers Hate from AI

> "Nothing kills developer trust faster than an AI nitpicking style while missing a critical production regression."

Subjective feedback on "code cleanliness", such as requesting function extractions, renaming local variables to suit stylistic preferences, or demanding additional comments, consistently receives high downvote rates. Developers perceive this as pedantic noise that blocks merge velocity.

## 5. The Final Frontier: Tribal Knowledge

The hardest challenge for AI code review agents is Tribal Knowledge (团队内隐经验). This refers to unwritten institutional context: why a certain bespoke pattern was chosen five years ago, architectural trade-offs specific to the organization's legacy systems, or undocumented external service idiosyncrasies. Until agents can effectively index organizational history, human reviewers remain indispensable for architectural sign-offs.

## 6. Key Metrics for AI Review Agents

Graphite gauges review quality not through token volume or comment count, but through:

- Action Rate: Percentage of AI comments that directly result in code edits before merge.
- Downvote / Dismissal Rate: Kept strictly below 5% to maintain long-term developer trust.
- Time to Merge: AI review should compress, rather than elongate, PR cycle time.