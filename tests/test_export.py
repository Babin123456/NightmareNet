import os
import tempfile
import unittest
from unittest.mock import MagicMock, patch

import torch
import torch.nn as nn

from nightmarenet.export.onnx_export import export_to_onnx
from nightmarenet.export.torchscript_export import export_to_torchscript


class DummyModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.linear = nn.Linear(10, 2)

    def forward(self, input_ids, attention_mask=None):
        # Dummy computation using the input_ids directly
        x = input_ids.float()
        return self.linear(x)


class DummyHFModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.linear = nn.Linear(10, 2)

    def forward(self, input_ids, attention_mask=None):
        class Output:
            def __init__(self, logits):
                self.logits = logits

        x = input_ids.float()
        return Output(self.linear(x))


class TestModelExport(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.output_dir = self.temp_dir.name
        self.model = DummyModel()
        self.hf_model = DummyHFModel()
        self.dummy_input = {
            "input_ids": torch.randint(0, 100, (2, 10)),
            "attention_mask": torch.ones(2, 10, dtype=torch.long),
        }

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_export_to_onnx(self):
        from importlib.util import find_spec

        if find_spec("onnx") is None or find_spec("onnxruntime") is None:
            self.skipTest("ONNX optional dependencies not installed.")

        output_path = os.path.join(self.output_dir, "model.onnx")
        export_to_onnx(self.model, output_path, self.dummy_input)
        self.assertTrue(os.path.exists(output_path))

    def test_export_to_onnx_hf(self):
        from importlib.util import find_spec

        if find_spec("onnx") is None or find_spec("onnxruntime") is None:
            self.skipTest("ONNX optional dependencies not installed.")

        output_path = os.path.join(self.output_dir, "model_hf.onnx")
        export_to_onnx(self.hf_model, output_path, self.dummy_input)
        self.assertTrue(os.path.exists(output_path))

    def test_export_to_torchscript(self):
        output_path = os.path.join(self.output_dir, "model.pt")
        export_to_torchscript(self.model, output_path, self.dummy_input)
        self.assertTrue(os.path.exists(output_path))

    def test_export_to_torchscript_hf(self):
        output_path = os.path.join(self.output_dir, "model_hf.pt")
        export_to_torchscript(self.hf_model, output_path, self.dummy_input)
        self.assertTrue(os.path.exists(output_path))

    @patch("nightmarenet.export.export_to_onnx")
    @patch("nightmarenet.distributed.checkpoint.load_model_weights")
    @patch("transformers.AutoModelForSequenceClassification.from_config")
    @patch("transformers.AutoTokenizer.from_pretrained")
    @patch("transformers.AutoConfig.from_pretrained")
    def test_cli_export_onnx(self, mock_config, mock_tokenizer, mock_model, mock_load, mock_export):
        import argparse

        from nightmarenet.cli import cmd_export

        args = argparse.Namespace(
            command="export",
            format="onnx",
            checkpoint="/tmp/dummy_checkpoint",
            output="/tmp/dummy_output.onnx",
            model="distilbert-base-uncased",
            task="seq_classification",
        )

        # We need os.path.exists to return True for checkpoint_dir
        with patch("os.path.exists") as mock_exists:

            def side_effect(path):
                if path == "/tmp/dummy_checkpoint":
                    return True
                return False

            mock_exists.side_effect = side_effect

            mock_tokenizer_instance = MagicMock()
            mock_tokenizer_instance.return_value = {"input_ids": torch.tensor([[1]])}
            mock_tokenizer.return_value = mock_tokenizer_instance

            ret = cmd_export(args)
            self.assertEqual(ret, 0)
            mock_export.assert_called_once()
            mock_load.assert_called_once()
