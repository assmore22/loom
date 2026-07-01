"""Tests for LOOM (direct runner). AI seal() validated live on studionet."""
from pathlib import Path

CONTRACT = str(Path(__file__).resolve().parents[1] / "contracts" / "loom.py")
OPEN = 0; SEALED = 1


def test_start_strand(deploy, direct_vm, direct_alice):
    lm = deploy(CONTRACT)
    direct_vm.sender = direct_alice
    sid = lm.start_strand("The last library on Earth powered down - except one terminal.")
    assert sid == 0
    s = lm.get_strand(0)
    assert s["status"] == OPEN
    assert s["line_count"] == 0


def test_start_requires_premise(deploy, direct_vm, direct_alice):
    lm = deploy(CONTRACT)
    direct_vm.sender = direct_alice
    with direct_vm.expect_revert("a premise is required"):
        lm.start_strand("   ")


def test_weave(deploy, direct_vm, direct_alice, direct_bob):
    lm = deploy(CONTRACT)
    direct_vm.sender = direct_alice
    lm.start_strand("A premise.")
    direct_vm.sender = direct_alice
    lm.weave(0, "It blinked once, then asked a question.")
    direct_vm.sender = direct_bob
    lm.weave(0, "Nobody had typed in a thousand years.")
    s = lm.get_strand(0)
    assert s["line_count"] == 2
    assert s["weaver_count"] == 2
    assert lm.get_line(0)["text"].startswith("It blinked")


def test_weave_requires_text(deploy, direct_vm, direct_alice):
    lm = deploy(CONTRACT)
    direct_vm.sender = direct_alice
    lm.start_strand("A premise.")
    with direct_vm.expect_revert("a line is required"):
        lm.weave(0, "  ")


def test_weave_too_long(deploy, direct_vm, direct_alice):
    lm = deploy(CONTRACT)
    direct_vm.sender = direct_alice
    lm.start_strand("A premise.")
    with direct_vm.expect_revert("280 characters"):
        lm.weave(0, "x" * 281)


def test_seal_needs_two_lines(deploy, direct_vm, direct_alice):
    lm = deploy(CONTRACT)
    direct_vm.sender = direct_alice
    lm.start_strand("A premise.")
    lm.weave(0, "Only one line.")
    with direct_vm.expect_revert("at least two"):
        lm.seal(0)


def test_no_such_strand(deploy, direct_vm, direct_alice):
    lm = deploy(CONTRACT)
    direct_vm.sender = direct_alice
    with direct_vm.expect_revert("no such strand"):
        lm.weave(5, "hi")


def test_multiple(deploy, direct_vm, direct_alice):
    lm = deploy(CONTRACT)
    direct_vm.sender = direct_alice
    lm.start_strand("Strand A")
    lm.start_strand("Strand B")
    assert lm.get_strand_count() == 2
    assert lm.get_strand(1)["premise"] == "Strand B"
