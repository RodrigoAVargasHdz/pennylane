# Copyright 2018-2021 Xanadu Quantum Technologies Inc.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Unit tests for for Hartree-Fock functions.
"""
import pytest
from pennylane import numpy as np
from pennylane.hf.hartree_fock import generate_hartree_fock, hf_energy, nuclear_energy
from pennylane.hf.molecule import Molecule


@pytest.mark.parametrize(
    ("symbols", "geometry", "v_fock", "coeffs", "fock_matrix", "h_core"),
    [
        (
            ["H", "H"],
            np.array([[0.0, 0.0, 0.0], [0.0, 0.0, 1.0]], requires_grad=False),
            np.array([-0.67578019,  0.94181155]),
            np.array([[-0.52754647, -1.56782303], [-0.52754647,  1.56782303]]),
            np.array([[-0.51126165, -0.70283714], [-0.70283714, -0.51126165]]),
            np.array([[-1.27848869, -1.21916299], [-1.21916299, -1.27848869]])
        )
    ],
)
def test_hartree_fock(symbols, geometry, v_fock, coeffs, fock_matrix, h_core):
    r"""Test that generate_hartree_fock returns the correct values."""
    mol = Molecule(symbols, geometry)
    v, c, f, h = generate_hartree_fock(mol)()

    assert np.allclose(v, v_fock)
    assert np.allclose(c, coeffs)
    assert np.allclose(f, fock_matrix)
    assert np.allclose(h, h_core)


@pytest.mark.parametrize(
    ("symbols", "geometry", "e_ref"),
    [
        (
            ["H", "H"],
            np.array([[0.0, 0.0, 0.0], [0.0, 0.0, 1.0]], requires_grad=False),
            # HF energy computed with pyscf using scf.hf.SCF(mol).kernel(numpy.eye(mol.nao_nr()))
            np.array([-1.06599931664376]),
        ),
        (
            ["H", "F"],
            np.array([[0.0, 0.0, 0.0], [0.0, 0.0, 1.0]], requires_grad=False),
            # HF energy computed with pyscf using scf.hf.SCF(mol).kernel(numpy.eye(mol.nao_nr()))
            np.array([-97.8884541671664]),
        )
    ],
)
def test_hf_energy(symbols, geometry, e_ref):
    r"""Test that hf_energy returns the correct energy."""
    mol = Molecule(symbols, geometry)
    e = hf_energy(mol)()
    assert np.allclose(e, e_ref)


@pytest.mark.parametrize(
    ("symbols", "geometry", "e_ref"),
    [
        # e_repulsion = sum(q_i * q_j / r_ij)
        (
            ["H", "H"],
            np.array([[0.0, 0.0, 0.0], [0.0, 0.0, 1.0]], requires_grad=False),
            np.array([1.0]),
        ),
        (
            ["H", "F"],
            np.array([[0.0, 0.0, 0.0], [0.0, 0.0, 2.0]], requires_grad=True),
            np.array([4.5]),
        ),
            (
            ["H", "O", "H"],
            np.array([[0.0, 1.2, 0.0], [0.0, 0.0, 0.0], [1.0, -0.2, 0.0]], requires_grad=True),
            np.array([15.09255]),
        )
    ],
)
def test_nuclear_energy(symbols, geometry, e_ref):
    r"""Test that nuclear_energy returns the correct energy."""
    mol = Molecule(symbols, geometry)
    args = [mol.coordinates]
    e = nuclear_energy(mol.nuclear_charges, mol.coordinates)(*args)
    print(e)
    assert np.allclose(e, e_ref)