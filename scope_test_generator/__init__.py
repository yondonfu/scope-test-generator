"""Test generator plugin for Scope."""

import scope.core

from .pipeline import TestGeneratorPipeline


@scope.core.hookimpl
def register_pipelines(register):
    """Register the test generator pipeline."""
    register(TestGeneratorPipeline)


__all__ = ["TestGeneratorPipeline"]
