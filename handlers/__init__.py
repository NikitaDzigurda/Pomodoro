import importlib

routers = []
modules = ["tasks", "ping"]

for module_name in modules:
    module = importlib.import_module(f"handlers.{module_name}")
    if hasattr(module, "router"):
        routers.append(module.router)

