"""Memory management for lfx with dynamic loading.

This module automatically chooses between the full langflow implementation
(when available) and the lfx implementation (when standalone).
"""

from lfx.utils.langflow_utils import has_langflow_memory, has_running_db_service

# Import the appropriate implementation
try:
    # Import the appropriate implementation
    if has_langflow_memory() and has_running_db_service():
        try:
            # Import full langflow implementation
            from langflow.memory import (
                aadd_messages,
                aadd_messagetables,
                add_messages,
                adelete_messages,
                aget_messages,
                astore_message,
                aupdate_messages,
                delete_message,
                delete_messages,
                get_messages,
                store_message,
            )
            
            # Verify compatibility
            import inspect
            sig = inspect.signature(aget_messages)
            if "context_id" not in sig.parameters:
                from lfx.log.logger import logger
                logger.warning("Installed langflow version is incompatible (missing context_id in aget_messages). Falling back to lfx stubs.")
                raise ImportError("Incompatible langflow version")
                
        except ImportError:
            # Fallback to lfx implementation if langflow import fails or is incompatible
            from lfx.memory.stubs import (
                aadd_messages,
                aadd_messagetables,
                add_messages,
                adelete_messages,
                aget_messages,
                astore_message,
                aupdate_messages,
                delete_message,
                delete_messages,
                get_messages,
                store_message,
            )
    else:
        # Use lfx implementation
        from lfx.memory.stubs import (
            aadd_messages,
            aadd_messagetables,
            add_messages,
            adelete_messages,
            aget_messages,
            astore_message,
            aupdate_messages,
            delete_message,
            delete_messages,
            get_messages,
            store_message,
        )
except Exception as e:
    from lfx.log.logger import logger
    logger.debug(f"Error initializing langflow memory, falling back to stubs: {e}")
    from lfx.memory.stubs import (
        aadd_messages,
        aadd_messagetables,
        add_messages,
        adelete_messages,
        aget_messages,
        astore_message,
        aupdate_messages,
        delete_message,
        delete_messages,
        get_messages,
        store_message,
    )
else:
    # Use lfx implementation
    from lfx.memory.stubs import (
        aadd_messages,
        aadd_messagetables,
        add_messages,
        adelete_messages,
        aget_messages,
        astore_message,
        aupdate_messages,
        delete_message,
        delete_messages,
        get_messages,
        store_message,
    )

# Export the available functions
__all__ = [
    "aadd_messages",
    "aadd_messagetables",
    "add_messages",
    "adelete_messages",
    "aget_messages",
    "astore_message",
    "aupdate_messages",
    "delete_message",
    "delete_messages",
    "get_messages",
    "store_message",
]
