# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
"""
LOOM - Collaborative AI-Judged Story Strands
============================================
A strand begins with a premise. Anyone weaves the next line. When the strand is
sealed, a validator set reads the whole thread under the Equivalence Principle
and crowns the single best continuation - the line that is most imaginative and
most coherent with what came before - and records a short critique. Authorship
of the winning line is permanent on-chain.

Strand status: OPEN(0) -> SEALED(1)
"""

from genlayer import *
from dataclasses import dataclass
import json
import typing


OPEN = 0
SEALED = 1


@allow_storage
@dataclass
class Line:
    strand_id: u256
    author: Address
    text: str


@allow_storage
@dataclass
class Strand:
    author: Address
    premise: str
    status: u8
    won: u8
    winner_line: u256
    critique: str


class Loom(gl.Contract):
    strands: DynArray[Strand]
    lines: DynArray[Line]

    def __init__(self) -> None:
        pass

    @gl.public.write
    def start_strand(self, premise: str) -> int:
        if len(premise.strip()) == 0:
            raise gl.vm.UserError("a premise is required")
        s = self.strands.append_new_get()
        s.author = gl.message.sender_address
        s.premise = premise
        s.status = u8(OPEN)
        s.won = u8(0)
        s.winner_line = u256(0)
        s.critique = ""
        return len(self.strands) - 1

    @gl.public.write
    def weave(self, strand_id: int, text: str) -> int:
        s = self._get(strand_id)
        if s.status != OPEN:
            raise gl.vm.UserError("this strand is sealed")
        if len(text.strip()) == 0:
            raise gl.vm.UserError("a line is required")
        if len(text) > 280:
            raise gl.vm.UserError("a line must be 280 characters or fewer")
        ln = self.lines.append_new_get()
        ln.strand_id = u256(strand_id)
        ln.author = gl.message.sender_address
        ln.text = text
        return len(self.lines) - 1

    @gl.public.write
    def seal(self, strand_id: int) -> None:
        s = self._get(strand_id)
        if s.status != OPEN:
            raise gl.vm.UserError("this strand is already sealed")

        globals_idx = []
        texts = []
        for gi in range(len(self.lines)):
            if int(self.lines[gi].strand_id) == strand_id:
                globals_idx.append(gi)
                texts.append(self.lines[gi].text)
        if len(texts) < 2:
            raise gl.vm.UserError("need at least two woven lines to seal")

        premise = s.premise
        numbered = "\n".join(str(i + 1) + ". " + t for i, t in enumerate(texts))
        n = len(texts)

        def leader_fn() -> str:
            prompt = (
                f"A collaborative micro-story.\nPREMISE: {premise}\n\n"
                f"Candidate continuation lines:\n{numbered}\n\n"
                f"Pick the SINGLE best continuation - the most imaginative line that "
                f"is also coherent with the premise. Choose a number from 1 to {n}. "
                'Reply with ONLY JSON: {"best": <number>, "critique": "<one sentence>"}.'
            )
            return gl.nondet.exec_prompt(prompt)

        def validator_fn(leader_res) -> bool:
            if not isinstance(leader_res, gl.vm.Return):
                return False
            return self._best_of(leader_res.calldata, n)[0] == self._best_of(leader_fn(), n)[0]

        result = gl.vm.run_nondet_unsafe(leader_fn, validator_fn)
        best_local, critique = self._best_of(result, n)
        s.winner_line = u256(globals_idx[best_local - 1])
        s.won = u8(1)
        s.critique = critique[:300]
        s.status = u8(SEALED)

    # ------------------------------------------------------------------ views
    @gl.public.view
    def get_strand_count(self) -> int:
        return len(self.strands)

    @gl.public.view
    def get_strand(self, strand_id: int) -> dict:
        s = self._get(strand_id)
        nlines = 0
        authors = []
        for ln in self.lines:
            if int(ln.strand_id) == strand_id:
                nlines += 1
                a = ln.author.as_hex
                if a not in authors:
                    authors.append(a)
        return {
            "author": s.author.as_hex,
            "premise": s.premise,
            "status": int(s.status),
            "won": int(s.won),
            "winner_line": int(s.winner_line),
            "critique": s.critique,
            "line_count": nlines,
            "weaver_count": len(authors),
        }

    @gl.public.view
    def get_line_count(self) -> int:
        return len(self.lines)

    @gl.public.view
    def get_line(self, idx: int) -> dict:
        if idx < 0 or idx >= len(self.lines):
            raise gl.vm.UserError("no such line")
        ln = self.lines[idx]
        return {
            "idx": idx,
            "strand_id": int(ln.strand_id),
            "author": ln.author.as_hex,
            "text": ln.text,
        }

    # -------------------------------------------------------------- internals
    def _get(self, strand_id: int) -> Strand:
        if strand_id < 0 or strand_id >= len(self.strands):
            raise gl.vm.UserError("no such strand")
        return self.strands[strand_id]

    def _best_of(self, result: typing.Any, n: int) -> tuple:
        data = result
        if isinstance(data, str):
            data = self._extract_json(data)
        best = 1
        critique = ""
        if isinstance(data, dict):
            critique = str(data.get("critique", ""))
            raw = data.get("best", 1)
            try:
                best = int(raw)
            except (ValueError, TypeError):
                best = 1
        if best < 1 or best > n:
            best = 1
        return (best, critique)

    def _extract_json(self, text: str) -> typing.Any:
        try:
            return json.loads(text)
        except (ValueError, TypeError):
            pass
        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1 and end > start:
            try:
                return json.loads(text[start:end + 1])
            except (ValueError, TypeError):
                return None
        return None
