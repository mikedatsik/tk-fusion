import os
import sgtk
import tank

logger = sgtk.LogManager.get_logger(__name__)

logger.debug("Launching toolkit in classic mode.")
env_engine = os.environ.get("SGTK_ENGINE")
env_context = os.environ.get("SGTK_CONTEXT")
context = sgtk.context.deserialize(env_context)

engine = sgtk.platform.start_engine(env_engine, context.sgtk, context)

out = ""
for item in engine.commands.items():
    if 'File Save...' in item[0]:
        out = item[1].get('callback')
# out.__call__()
