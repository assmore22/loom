"""Seed LOOM with real strands on studionet (multi-author lines + AI seal)."""
from pathlib import Path

from gltest_cli.config.general import get_general_config
from gltest_cli.config.user import load_user_config
from gltest import get_contract_factory, get_default_account, get_gl_client, create_account

ROOT = Path(__file__).resolve().parents[1]
ADDR = "0xE355A2452D135F7133367d8C7D23b47315b34DaB"
GEN = 10 ** 18

cfg = load_user_config(str(ROOT / "gltest.config.yaml"))
get_general_config().user_config = cfg
factory = get_contract_factory(contract_file_path=str(ROOT / "contracts" / "loom.py"))
host = get_default_account()
c = factory.build_contract(ADDR, account=host)


def weaver():
    acc = create_account()
    try:
        get_gl_client().fund_account(acc.address, 5 * GEN)
    except Exception as e:
        print("fund:", e)
    return factory.build_contract(ADDR, account=acc)


S0 = "The last library on Earth finally powered down -- except for one terminal, still blinking in the dark."
S0_LINES = [
    "A child's hand reached up and pressed a single key, and the whole room exhaled.",
    "On the screen, three words appeared: ASK ME ANYTHING.",
    "Outside, the rain stopped, as if the sky itself were leaning in to listen.",
    "It had been waiting nine hundred years to be asked the one question it could not answer.",
]
S1 = "A lighthouse keeper receives a message in a bottle addressed to her -- postmarked next year."
S1_LINES = [
    "The handwriting was unmistakably her own, though she had never written it.",
    "Tomorrow's tide, it warned, would bring something that did not float.",
]


def main():
    if c.get_strand_count().call() == 0:
        c.start_strand(args=[S0]).transact()
        c.start_strand(args=[S1]).transact()
        print("started 2 strands")

        weavers = [weaver() for _ in range(2)]
        for i, ln in enumerate(S0_LINES):
            (c if i % 3 == 0 else weavers[i % 2]).weave(args=[0, ln]).transact()
            print("woven s0:", ln[:40])
        for i, ln in enumerate(S1_LINES):
            (c if i == 0 else weavers[0]).weave(args=[1, ln]).transact()
            print("woven s1:", ln[:40])

    s0 = c.get_strand(args=[0]).call()
    if int(s0["status"]) == 0 and int(s0["line_count"]) >= 2:
        print("sealing strand 0 (AI)...")
        try:
            c.seal(args=[0]).transact()
        except Exception as e:
            print("seal ->", e)

    for sid in range(c.get_strand_count().call()):
        s = c.get_strand(args=[sid]).call()
        st = ["OPEN", "SEALED"][int(s["status"])]
        print(sid, st, "lines=%d" % int(s["line_count"]), "winner_line=%s" % s["winner_line"], "|", (s["critique"] or "")[:50])


if __name__ == "__main__":
    main()
