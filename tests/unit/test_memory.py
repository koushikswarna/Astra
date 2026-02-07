"""Tests for the memory subsystem."""

import json
import pytest
from pathlib import Path

from astra.memory.short_term import ShortTermMemory
from astra.storage.json_store import JSONStore
from astra.types import Personality


class TestShortTermMemory:
    def test_add_and_retrieve(self):
        mem = ShortTermMemory(max_turns=4)
        mem.add("User", "hello")
        mem.add("Astra", "hi there")

        assert len(mem.history) == 2
        assert mem.history[0] == ("User", "hello")

    def test_trimming(self):
        mem = ShortTermMemory(max_turns=2)
        # add 3 full exchanges (6 entries, limit is 4)
        for i in range(3):
            mem.add("User", f"msg {i}")
            mem.add("Astra", f"reply {i}")

        # should keep last 4 entries (2 exchanges)
        assert len(mem.history) == 4
        assert mem.history[0] == ("User", "msg 1")

    def test_retrieve_recent(self):
        mem = ShortTermMemory()
        mem.add("User", "first")
        mem.add("Astra", "second")
        mem.add("User", "third")

        recent = mem.retrieve("anything", n=2)
        assert len(recent) == 2
        assert recent[-1] == "third"

    def test_format_prompt(self):
        mem = ShortTermMemory()
        mem.add("User", "hello")

        personality = Personality(tone="friendly", mood="cheerful")
        prompt = mem.format_prompt(personality)

        assert "friendly and cheerful" in prompt
        assert "User: hello" in prompt
        assert prompt.endswith("Astra:")

    def test_format_prompt_no_double_user(self):
        """Regression test: the user message should appear exactly once."""
        mem = ShortTermMemory()
        mem.add("User", "test message")

        personality = Personality(tone="calm", mood="analytic")
        prompt = mem.format_prompt(personality)

        count = prompt.count("test message")
        assert count == 1, f"User message appeared {count} times in prompt"

    def test_clear(self):
        mem = ShortTermMemory()
        mem.add("User", "hello")
        mem.clear()
        assert mem.size() == 0

    def test_persistence(self, tmp_path):
        store = JSONStore(tmp_path / "test_mem.json")

        # save
        mem1 = ShortTermMemory()
        mem1.attach_store(store)
        mem1.add("User", "remember this")
        mem1.add("Astra", "I will")
        mem1.save()

        # load into fresh instance
        mem2 = ShortTermMemory()
        mem2.attach_store(store)
        mem2.load()

        assert len(mem2.history) == 2
        assert mem2.history[0] == ("User", "remember this")


class TestJSONStore:
    def test_save_and_load(self, tmp_path):
        path = tmp_path / "data.json"
        store = JSONStore(path)

        store.save({"key": "value"})
        loaded = store.load()
        assert loaded == {"key": "value"}

    def test_load_nonexistent(self, tmp_path):
        store = JSONStore(tmp_path / "nope.json")
        assert store.load() is None

    def test_exists(self, tmp_path):
        path = tmp_path / "data.json"
        store = JSONStore(path)

        assert not store.exists()
        store.save([1, 2, 3])
        assert store.exists()

    def test_clear(self, tmp_path):
        path = tmp_path / "data.json"
        store = JSONStore(path)
        store.save("test")
        store.clear()
        assert not store.exists()
