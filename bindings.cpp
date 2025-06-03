#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "chessState.h"

namespace py = pybind11;
using namespace pybind11::literals;

PYBIND11_MODULE(chessEngine, m){
  m.doc() = "Python bindings for C++ engine";

  py::class_<chessState>(m, "chessStatePy")
    .def(py::init<std::string>())
    .def("playerMove", &chessState::playerMove)
    .def("pieceAt", &chessState::sPieceAt)
    .def("searchMove", &chessState::searchMove);
}