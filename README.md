# Loom V2

A GenLayer creative synthesis court.

This repo packages the public casework UI and the GenLayer contract behind it: filings, evidence, review windows, challenge paths and final resolution.

## Loom Brief

- Project folder: `projects/24-loom`
- Frontend: static browser app
- Contract package: `contracts/` plus `deployment.json`
- Build status: Schema-valid (38187 bytes, 17 write + 18 view); deployed + 18 write smoke txs finalized incl 3 GenLayer reasoning calls; 37/37 read tests passed; legacy frontend shape verified; app.js repointed.
- QA notes: Upgraded from a compact collaborative story MVP into Loom V2. Smoke: set_loom_standard / start_strand / four weave calls / two add_evidence calls / open_synthesis / seal_with_genlayer / open_challenge_window / submit_challenge / resolve_challenge_with_genla...

## Loom Chain Links

- Network: studionet (61999)
- Contract: [0xCA03806cdA08C45c29919Bca57cC420477f8ef5d](https://explorer-studio.genlayer.com/contracts/0xCA03806cdA08C45c29919Bca57cC420477f8ef5d)
- Deploy tx: [0x8b99a1c1...ae622b](https://explorer-studio.genlayer.com/tx/0x8b99a1c1393cc09a9fc94ff2d6b928bedc272e1a114b2e7af2499d4d00ae622b)
- Deployed at: 2026-06-23T18:56:51.852Z
- Smoke writes recorded: 18

## Adjudication Mechanics

- Primary source: `contracts/loom_v2.py` (38,187 bytes)
- Public write/action methods: 17
- Read methods: 20
- GenLayer features: live web rendering, LLM adjudication, validator-comparative consensus, append-only collections

Typical flow: `open_strand` -> `submit_challenge` -> `resolve_challenge_with_genlayer` -> `open_challenge_window` -> `submit_appeal` -> `archive_strand` -> `set_loom_standard`

Useful reads: `get_strand_count`, `get_line_count`, `get_strand`, `get_line`, `get_strand_record`, `get_recent_strands`, `get_strands_by_status`, `get_author_strands`

The contract is deliberately larger than a one-method demo. It keeps lifecycle state, evidence records and read endpoints so the UI can show real project state instead of static copy.

## Run Loom Locally

```powershell
cd <private-workspace-root>
npm run preview:start
npm run preview:project -- 24-loom
```

Open http://localhost:8080/24-loom/.

## Smoke Transactions

- set_loom_standard: [0x86e9d09e...3dc796](https://explorer-studio.genlayer.com/tx/0x86e9d09ea05630f9750c1f3ed95119901486ec77b6629a7e8eae4671c43dc796)
- start_strand: [0x647b0db1...ea6c3e](https://explorer-studio.genlayer.com/tx/0x647b0db16fb9f93dd47f216f562642e82a012e094d460df7cf6f3a1d66ea6c3e)
- weave_1: [0x4cb80cf5...5301be](https://explorer-studio.genlayer.com/tx/0x4cb80cf560ab1eaad0794da7d00dfd56f518280cb4d23b5811a9729ea55301be)
- weave_2: [0x18fe63b1...12eafd](https://explorer-studio.genlayer.com/tx/0x18fe63b17f8612a74fceb060b7c37453229847bb65e4f81f3fc933470112eafd)
- weave_3: [0xf2ff17bb...30bfaf](https://explorer-studio.genlayer.com/tx/0xf2ff17bb2e68ba11ebd4d47c547cacd7a378a40f5382654995977213e630bfaf)
- weave_4: [0x17faf139...a02fe4](https://explorer-studio.genlayer.com/tx/0x17faf13940321431c0c75c7da39867f5695dd670f81ddf5e55d399bc2ca02fe4)
- add_evidence_collab: [0xbe03246c...60e835](https://explorer-studio.genlayer.com/tx/0xbe03246c2bef94cb170728132c36779ccbd5986535e7df79904b2cfa3d60e835)
- add_evidence_exquisite: [0x311eaf2c...bb0a70](https://explorer-studio.genlayer.com/tx/0x311eaf2c9157327332a33990fdf6f1818470043f778a6aa0f610ff7300bb0a70)

## Publish Loom

```powershell
cd <private-workspace-root>
npm run publish:project -- -Project 24-loom -Repo https://github.com/aspro45/<repo-name>.git
```

Replace `<repo-name>` with the GitHub repository name before publishing.

## Keys And Boundaries

- Private keys and local vault files are not part of this repository.
- Public addresses, contract source, deployment metadata and frontend code are safe to publish.
- Vercel should receive only this project folder, never the workspace dashboard or vault data.
