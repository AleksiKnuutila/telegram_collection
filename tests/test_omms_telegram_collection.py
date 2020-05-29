import pytest
import hypothesis

import omms_telegram_collection

def test_omms_telegram_collection_version():
    """Test that the package exists and has a version"""
    assert omms_telegram_collection.__version__

