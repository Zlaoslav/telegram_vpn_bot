import pkgutil
import importlib
from services.hlpr_logging import logger

def register_handlers(dp):
    loaded_handlers_count = 0
    error_handlers_count = 0

    for importer, modname, ispkg in pkgutil.iter_modules(__path__):
        if modname == '__init__':
            continue
        if not modname.startswith("hndl_"):
            continue

        try:
            module = importlib.import_module(f"{__name__}.{modname}")
            if hasattr(module, 'router'):
                dp.include_router(module.router)
                logger.info(f"HANDLER loaded: {modname}")
                loaded_handlers_count += 1
        except Exception as e:
            logger.error(f"Failed to load handler: {modname}, Error: {e}")
            error_handlers_count += 1
    
    if error_handlers_count == 0:
        logger.info(f"All handlers loaded successfully ({loaded_handlers_count})")
    else:
        logger.critical(f"Only {loaded_handlers_count}/{loaded_handlers_count + error_handlers_count} handlers have been loaded.")