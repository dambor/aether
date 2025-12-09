
# This file patches potential issues with Langflow's custom types when running in standalone mode.
import uuid
import sys
import inspect
from typing import Any

# 1. Patch UUIDstr for SQLModel compatibility
try:
    import langflow.services.database.models.base
    langflow.services.database.models.base.UUIDstr = uuid.UUID
except ImportError:
    pass
except Exception as e:
    print(f"Warning: Failed to patch UUIDstr: {e}")

# 2. Force LFX to use standalone stubs (bypass langflow memory)
# This prevents "ValueError: The messages must be instances of Message" caused by type mismatch
try:
    # We patch lfx.utils.langflow_utils.has_langflow_memory to return False
    # This ensures LFX uses its internal stubs and Message types instead of trying to use Langflow's
    import lfx.utils.langflow_utils
    lfx.utils.langflow_utils.has_langflow_memory = lambda: False
    
    # Also force has_running_db_service to False just in case
    lfx.utils.langflow_utils.has_running_db_service = lambda: False
    
    print("Patched LFX to force standalone memory mode.")
except ImportError:
    pass
except Exception as e:
    print(f"Warning: Failed to patch LFX standalone mode: {e}")

# 3. Patch lfx.memory.aget_messages for compatibility (Backup fix)
try:
    import lfx.memory
    original_aget_messages = lfx.memory.aget_messages
    
    sig = inspect.signature(original_aget_messages)
    if "context_id" not in sig.parameters:
        print("Patching lfx.memory.aget_messages to support context_id")
        async def patched_aget_messages(*args, **kwargs):
            kwargs.pop("context_id", None)
            return await original_aget_messages(*args, **kwargs)
        lfx.memory.aget_messages = patched_aget_messages
        # Also patch sys.modules in case it was already imported
        if "lfx.memory.stubs" in sys.modules:
             sys.modules["lfx.memory.stubs"].aget_messages = patched_aget_messages
except ImportError:
    pass
except Exception as e:
    print(f"Warning: Failed to patch lfx.memory: {e}")

# 4. Patch ChatOutputResponse for UUID session_id compatibility
try:
    from lfx.utils import schemas
    from pydantic import field_validator
    from uuid import UUID

    # Create a patched class that accepts UUID for session_id
    BaseChatOutputResponse = schemas.ChatOutputResponse
    
    class PatchedChatOutputResponse(BaseChatOutputResponse):
        # We allow session_id to be UUID and coerce to string
        @field_validator("session_id", mode="before", check_fields=False)
        @classmethod
        def validate_session_id(cls, v):
            if isinstance(v, UUID):
                return str(v)
            return v

    # Replace the class in the module
    schemas.ChatOutputResponse = PatchedChatOutputResponse
    print("Patched ChatOutputResponse to accept UUID session_id.")
    
except ImportError:
    pass
except Exception as e:
    print(f"Warning: Failed to patch ChatOutputResponse: {e}")

# 5. Patch base_component deepcopy to handle unpickleable objects (e.g. gRPC clients)
try:
    import lfx.custom.custom_component.base_component
    import copy

    # We replace the 'copy' module in base_component with a wrapper
    original_copy = lfx.custom.custom_component.base_component.copy
    
    class SafeCopyWrapper:
        def __getattr__(self, name):
            attr = getattr(original_copy, name)
            if name == "deepcopy":
                return self.safe_deepcopy
            return attr
            
        def safe_deepcopy(self, obj, memo=None, _nil=[]):
            try:
                # We try deepcopy
                return original_copy.deepcopy(obj, memo)
            except TypeError:
                 # If deepcopy fails (e.g. "no default __reduce__"), return original
                 return obj
            except Exception:
                 return obj

    lfx.custom.custom_component.base_component.copy = SafeCopyWrapper()
    print("Patched base_component.copy to handle uncopyable objects.")
except ImportError:
    pass
except Exception as e:
    print(f"Warning: Failed to patch base_component copy: {e}")
