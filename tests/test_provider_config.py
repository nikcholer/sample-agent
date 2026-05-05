from __future__ import annotations

import os
import unittest
from unittest.mock import patch

from implementations.openai_agents_sdk.provider_config import (
    TOGETHER_DEFAULT_MODEL,
    selected_model,
    selected_provider,
)


class ProviderConfigTests(unittest.TestCase):
    def test_defaults_to_openai_provider(self) -> None:
        with patch.dict(os.environ, {}, clear=True):
            self.assertEqual(selected_provider(), "openai")
            self.assertIsNone(selected_model())

    def test_together_provider_defaults_to_supported_model(self) -> None:
        with patch.dict(os.environ, {"OPENAI_AGENT_PROVIDER": "together"}, clear=True):
            self.assertEqual(selected_provider(), "together")
            self.assertEqual(selected_model(), TOGETHER_DEFAULT_MODEL)

    def test_explicit_model_wins(self) -> None:
        with patch.dict(
            os.environ,
            {
                "OPENAI_AGENT_PROVIDER": "together",
                "OPENAI_AGENT_MODEL": "moonshotai/Kimi-K2.5",
            },
            clear=True,
        ):
            self.assertEqual(selected_model("manual/model"), "manual/model")
            self.assertEqual(selected_model(), "moonshotai/Kimi-K2.5")


if __name__ == "__main__":
    unittest.main()
