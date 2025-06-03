from setuptools import setup
from pybind11.setup_helpers import Pybind11Extension, build_ext

cppSources = ["./ChessFramework/chessState.cpp", 
              "./ChessFramework/bindings.cpp",
              "./ChessFramework/transpositionTable.cpp"]

ext_modules = [
  Pybind11Extension(
    "chessEngine",
    sorted(cppSources),
    cxx_std=17
    
  ),
]

setup(
  name="chessEngineWrapper",
  version="0.1.0",
  author="James",
  description="Python bindings for c++ chess engine",
  ext_modules=ext_modules,
  cmdclass={"build_ext":build_ext},
  install_requires=["pybind11>=2.6"]
)