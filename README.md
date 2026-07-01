# Loom

Collaborative strands with synthesis and dispute review.

Loom stores narrative strands, evidence and synthesis runs. The point is not just to publish text, but to preserve how a shared conclusion was woven from sources.

## Review Links

| Surface | Link |
| --- | --- |
| Live app | https://assmore22-loom.vercel.app |
| GitHub | https://github.com/assmore22/loom |
| Contract | https://explorer-studio.genlayer.com/contracts/0xCA03806cdA08C45c29919Bca57cC420477f8ef5d |

## Chain Record

- Network: GenLayer Studionet
- Chain ID: 61999
- Contract: `0xCA03806cdA08C45c29919Bca57cC420477f8ef5d`
- Deploy transaction: [0x8b99a1c1...ae622b](https://explorer-studio.genlayer.com/tx/0x8b99a1c1393cc09a9fc94ff2d6b928bedc272e1a114b2e7af2499d4d00ae622b)
- Deployed: `2026-06-23T18:56:51.852Z`
- Source: `contracts/loom_v2.py` (38,187 bytes)

## Protocol Path

1. Start a strand.
2. Add weave entries.
3. Attach evidence.
4. Open synthesis.
5. Seal the synthesis with GenLayer.

The frontend reads strand entries, evidence, synthesis summaries and challenge state. Contract state is public; write actions still require a connected wallet on GenLayer Studionet.

## Finalized Smoke

| Action | Transaction |
| --- | --- |
| `set_loom_standard` | [0x86e9d09e...3dc796](https://explorer-studio.genlayer.com/tx/0x86e9d09ea05630f9750c1f3ed95119901486ec77b6629a7e8eae4671c43dc796) |
| `start_strand` | [0x647b0db1...ea6c3e](https://explorer-studio.genlayer.com/tx/0x647b0db16fb9f93dd47f216f562642e82a012e094d460df7cf6f3a1d66ea6c3e) |
| `weave_1` | [0x4cb80cf5...5301be](https://explorer-studio.genlayer.com/tx/0x4cb80cf560ab1eaad0794da7d00dfd56f518280cb4d23b5811a9729ea55301be) |
| `weave_2` | [0x18fe63b1...12eafd](https://explorer-studio.genlayer.com/tx/0x18fe63b17f8612a74fceb060b7c37453229847bb65e4f81f3fc933470112eafd) |
| `weave_3` | [0xf2ff17bb...30bfaf](https://explorer-studio.genlayer.com/tx/0xf2ff17bb2e68ba11ebd4d47c547cacd7a378a40f5382654995977213e630bfaf) |
| `weave_4` | [0x17faf139...a02fe4](https://explorer-studio.genlayer.com/tx/0x17faf13940321431c0c75c7da39867f5695dd670f81ddf5e55d399bc2ca02fe4) |

## Local Run

```bash
python -m http.server 8080
```

Open `http://localhost:8080`.

## Release Hygiene

The public package is static and has no install step. Vercel receives only frontend, contract source and public deployment metadata.

Keep wallet private keys, vault exports, `.env` files, Vercel project state and dashboard data out of Git. This repository is for public source, UI, tests and deployment receipts only.
