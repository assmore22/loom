# Loom

Collaborative strands with synthesis and dispute review.

Loom stores narrative strands, evidence and synthesis runs. The point is not just to publish text, but to preserve how a shared conclusion was woven from sources.

## Review Links

| Surface | Link |
| --- | --- |
| Live app | https://assmore22-loom.vercel.app |
| GitHub | https://github.com/assmore22/loom |
| Contract | https://explorer-bradbury.genlayer.com/address/0x5fcB086587Ac6741Dd0dec5AEeDfcda1460c6Da5 |

## Chain Record

- Network: GenLayer Bradbury
- Chain ID: 4221
- Contract: `0x5fcB086587Ac6741Dd0dec5AEeDfcda1460c6Da5`
- Deploy transaction: [0x55a7e51c...5bd6d0](https://explorer-bradbury.genlayer.com/tx/0x55a7e51c3091640ee6316df17cbb29839731582949884601c11cb2c22e5bd6d0)
- Deployed: `2026-07-01T15:53:12.275Z`
- Source: `contracts/loom_v2.py` (38,187 bytes)

## Protocol Path

1. Start a strand.
2. Add weave entries.
3. Attach evidence.
4. Open synthesis.
5. Seal the synthesis with GenLayer.

The frontend reads strand entries, evidence, synthesis summaries and challenge state. Contract state is public; write actions still require a connected wallet on GenLayer Bradbury.

## Bradbury Smoke

| Action | Transaction |
| --- | --- |
| `open_strand` | [0x2737f842...93a4f1](https://explorer-bradbury.genlayer.com/tx/0x2737f8426d89e70365dec46ab3bdfa2a0b08ae100c04f4160ef8741ced93a4f1) |

Read verification passed on Bradbury after deploy. The public app points at this contract address and reads accepted state.

## Local Run

```bash
python -m http.server 8080
```

Open `http://localhost:8080`.

## Release Hygiene

The public package is static and has no install step. Vercel receives only frontend, contract source and public deployment metadata.

Keep wallet private keys, vault exports, `.env` files, Vercel project state and dashboard data out of Git. This repository is for public source, UI, tests and deployment receipts only.
