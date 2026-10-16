# Optional context and output-style lab

Complete the [Module 2 walkthrough](README.md) first. Output styles change how
Claude explains work; they do not change application requirements or verify facts.

**Guided:** inspect `examples/output-styles/issue-tracker-tutor.md`. Copy it to
`.claude/output-styles/issue-tracker-tutor.md` only if that destination is absent
(create the directory first). Restart Claude and select it with `/output-style`
if supported by the installed CLI. Ask it to explain the existing login request
flow. Compare the explanation with the source map and turn the style off afterward.

**Independent:** create a terse reviewer style with headings “Evidence,” “Unknowns,”
and “Next check.” Explain one issue PATCH request. Verify that the style changes
presentation without inventing paths or claiming unrun tests.

Scoped rules are exercised in Module 2. Keep rules short; avoid placing the whole
specification in always-loaded context. Use `/context` to inspect context usage
and preserve facts in the map before `/compact`.
