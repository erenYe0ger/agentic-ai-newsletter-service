import sys
import os

# add project root to python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.services.model_discovery_service import ModelDiscoveryService

ModelDiscoveryService().save_models()