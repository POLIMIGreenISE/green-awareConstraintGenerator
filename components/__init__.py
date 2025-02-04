import os
import glob

# Get all Python files in the current directory (excluding __init__.py)
module_files = glob.glob(os.path.join(os.path.dirname(__file__), "*.py"))
module_names = [
    os.path.basename(f)[:-3] for f in module_files if f.endswith(".py") and f != "__init__.py"
]

# Import all modules dynamically
__all__ = []
for module in module_names:
    mod = __import__(f"components.{module}", fromlist=["*"])
    globals().update({name: getattr(mod, name) for name in dir(mod) if not name.startswith("_")})
    __all__.extend([name for name in dir(mod) if not name.startswith("_")])
