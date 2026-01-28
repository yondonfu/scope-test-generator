"""Test generator pipeline that creates simple animated frames."""

import torch
from typing import ClassVar

from scope.core.pipelines.interface import Pipeline
from scope.core.pipelines.schema import BasePipelineConfig


class TestGeneratorConfig(BasePipelineConfig):
    """Configuration for test generator pipeline."""

    pipeline_id: ClassVar[str] = "test-generator"
    pipeline_name: ClassVar[str] = "Test Generator"
    pipeline_description: ClassVar[str] = "Generates simple animated test patterns"
    pipeline_version: ClassVar[str] = "0.1.0"

    supports_prompts: ClassVar[bool] = False

    supported_modes: ClassVar[list[str]] = ["text"]
    default_mode: ClassVar[str] = "text"
    height: int = 512
    width: int = 512


class TestGeneratorPipeline(Pipeline):
    """Simple pipeline that generates animated color frames."""

    @classmethod
    def get_config_class(cls):
        return TestGeneratorConfig

    def __init__(self, height=512, width=512, device=None, **kwargs):
        self.height = height
        self.width = width
        self.device = device or torch.device(
            "cuda" if torch.cuda.is_available() else "cpu"
        )
        self.frame_count = 0

    def __call__(self, **kwargs):
        """Generate a frame that changes color over time.

        Returns:
            torch.Tensor: Frame in THWC format (1, H, W, 3) in [0, 1] range
        """
        # Cycle through RGB colors based on frame count
        t = torch.tensor(self.frame_count / 60.0)  # Smooth transition every 60 frames

        r = (torch.sin(t) + 1) / 2
        g = (torch.sin(t + 2.0) + 1) / 2
        b = (torch.sin(t + 4.0) + 1) / 2

        # Create frame with solid color
        frame = torch.ones(1, self.height, self.width, 3, device=self.device)
        frame[0, :, :, 0] = r
        frame[0, :, :, 1] = g
        frame[0, :, :, 2] = b

        self.frame_count += 1

        return {"video": frame}
