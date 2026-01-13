#!/usr/bin/env python3
"""
Test script to verify all imports work correctly in the backend directory.
This addresses the naming conflict with the 'logging' directory.
"""

import sys
import os

# Add the parent directory to the path to avoid conflicts with local 'logging' directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_backend_imports():
    """Test importing all major backend components."""
    print("Testing backend imports...")

    try:
        # Test main import
        import main
        print("✓ Successfully imported main")

        # Test config import
        from config import BackendConfig
        print("✓ Successfully imported BackendConfig")

        # Test models import
        from models import Task, Conversation, Message
        print("✓ Successfully imported models")

        # Test routers import
        from routers.chat_router import router as chat_router
        from routers.auth_router import router as auth_router
        print("✓ Successfully imported routers")

        # Test database import
        from database.connection import get_session_context
        print("✓ Successfully imported database connection")

        # Test logging import (the tricky one due to naming conflict)
        # We need to temporarily remove the local logging from sys.modules if it was imported
        if 'logging' in sys.modules:
            # Save the stdlib logging module
            import logging as std_logging
            # Clear the local logging module if it was mistakenly imported
            if 'logging' in sys.modules:
                del sys.modules['logging']
            # Re-import the standard library logging
            import logging
            print("✓ Successfully handled logging module conflict")
        else:
            import logging
            print("✓ Successfully imported logging")

        # Test the local logging config
        from logging.config import log_with_context
        print("✓ Successfully imported local logging config")

        # Test middleware imports
        from middleware.correlation_id_middleware import CorrelationIDMiddleware
        from middleware.timeout_middleware import TimeoutMiddleware
        from middleware.validation_middleware import ValidationMiddleware
        from middleware.rate_limiting_middleware import RateLimitMiddleware
        print("✓ Successfully imported middleware")

        # Test auth imports
        from auth.middleware import auth_middleware
        from auth.session_manager import session_manager
        print("✓ Successfully imported auth components")

        print("\n🎉 All imports successful!")
        return True

    except Exception as e:
        print(f"❌ Import failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_backend_imports()
    sys.exit(0 if success else 1)