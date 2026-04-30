# MIT License
#
# Copyright (c) 2026 jmfrohs
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import json
import os
import sys
from unittest.mock import patch

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from config import load_config

class TestLoadConfig:
    def test_returns_defaults_when_no_file(self, tmp_path):
        fake_config = tmp_path / ".scaffoldrc"
        with patch("config.CONFIG_FILE", fake_config):
            config = load_config()
        assert config["lang"] == "javascript"
        assert config["author"] == "jmfrohs"

    def test_merges_user_config(self, tmp_path):
        fake_config = tmp_path / ".scaffoldrc"
        fake_config.write_text(
            json.dumps({"author": "TestUser", "lang": "python"}), encoding="utf-8"
        )
        with patch("config.CONFIG_FILE", fake_config):
            config = load_config()
        assert config["author"] == "TestUser"
        assert config["lang"] == "python"

    def test_invalid_json_returns_defaults(self, tmp_path):
        fake_config = tmp_path / ".scaffoldrc"
        fake_config.write_text("not valid json", encoding="utf-8")
        with patch("config.CONFIG_FILE", fake_config):
            config = load_config()
        assert "author" in config
