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
Unit tests for the molecule object.
"""
# pylint: disable=no-self-use
import pytest
from pennylane import numpy as np
from pennylane.hf.molecule import Molecule
from pennylane.hf.basis_set import BasisFunction
from pennylane.hf.hartree_fock import generate_scf


class TestMolecule:
    """Tests for generating a molecule object."""

    @pytest.mark.parametrize(
        ("symbols", "geometry"),
        [
            (["H", "F"], np.array([[0.0, 0.0, 0.0], [0.0, 0.0, 1.0]])),
        ],
    )
    def test_build_molecule(self, symbols, geometry):
        r"""Test that the generated molecule object has the correct type."""
        mol = Molecule(symbols, geometry)
        assert isinstance(mol, Molecule)

    @pytest.mark.parametrize(
        ("symbols", "geometry"),
        [
            (["H", "F"], np.array([[0.0, 0.0, 0.0], [0.0, 0.0, 1.0]])),
        ],
    )
    def test_basis_error(self, symbols, geometry):
        r"""Test that an error is raised if a wrong basis set name is entered."""
        with pytest.raises(ValueError, match="Currently, the only supported basis set is"):
            Molecule(symbols, geometry, basis_name="6-31g")

    @pytest.mark.parametrize(
        ("symbols", "geometry"),
        [
            (["H", "Og"], np.array([[0.0, 0.0, 0.0], [0.0, 0.0, 1.0]])),
        ],
    )
    def test_symbol_error(self, symbols, geometry):
        r"""Test that an error is raised if a wrong/not-supported atomic symbol is entered."""
        with pytest.raises(ValueError, match="are not supported"):
            Molecule(symbols, geometry)

    @pytest.mark.parametrize(
        ("symbols", "geometry", "charge", "mult", "basis_name"),
        [
            (["H", "F"], np.array([[0.0, 0.0, 0.0], [0.0, 0.0, 1.0]]), 0, 1, "sto-3g"),
        ],
    )
    def test_default_inputs(self, symbols, geometry, charge, mult, basis_name):
        r"""Test that the molecule object contains correct default molecular input data."""
        mol = Molecule(symbols, geometry)

        assert mol.symbols == symbols
        assert np.allclose(mol.coordinates, geometry)
        assert mol.charge == charge
        assert mol.mult == mult
        assert mol.basis_name == basis_name

    @pytest.mark.parametrize(
        ("symbols", "geometry", "n_electrons", "n_orbitals", "nuclear_charges"),
        [
            (
                ["H", "F"],
                np.array([[0.0, 0.0, 0.0], [0.0, 0.0, 1.0]]),
                10,
                6,
                [1, 9],
            ),
        ],
    )
    def test_molecule_data(self, symbols, geometry, n_electrons, n_orbitals, nuclear_charges):
        r"""Test that the molecule object contains correct molecular data."""
        mol = Molecule(symbols, geometry)

        assert mol.n_electrons == n_electrons
        assert mol.n_orbitals == n_orbitals
        assert mol.nuclear_charges == nuclear_charges

    @pytest.mark.parametrize(
        ("symbols", "geometry", "n_basis", "basis_data"),
        [
            (
                ["H", "H"],
                np.array([[0.0, 0.0, 0.0], [0.0, 0.0, 1.0]]),
                [1, 1],
                (
                    (
                        (0, 0, 0),
                        [3.42525091, 0.62391373, 0.1688554],
                        [0.15432897, 0.53532814, 0.44463454],
                    ),
                    (
                        (0, 0, 0),
                        [3.42525091, 0.62391373, 0.1688554],
                        [0.15432897, 0.53532814, 0.44463454],
                    ),
                ),
            ),
        ],
    )
    def test_default_basisdata(self, symbols, geometry, n_basis, basis_data):
        r"""Test that the molecule object contains correct default basis data for a given molecule."""
        mol = Molecule(symbols, geometry)

        assert mol.n_basis == n_basis
        assert np.allclose(mol.basis_data, basis_data)

    @pytest.mark.parametrize(
        ("symbols", "geometry", "l", "alpha", "coeff", "r"),
        [
            (
                ["H", "H"],
                np.array([[0.0, 0.0, 0.0], [0.0, 0.0, 1.0]]),
                [(0, 0, 0), (0, 0, 0)],
                [[3.42525091, 0.62391373, 0.1688554], [3.42525091, 0.62391373, 0.1688554]],
                [[0.15432897, 0.53532814, 0.44463454], [0.15432897, 0.53532814, 0.44463454]],
                np.array([[0.0, 0.0, 0.0], [0.0, 0.0, 1.0]]),
            ),
            (
                ["H", "F"],
                np.array([[0.0, 0.0, 0.0], [0.0, 0.0, 1.0]]),
                [(0, 0, 0), (0, 0, 0), (0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1)],
                [
                    [0.3425250914e01, 0.6239137298e00, 0.1688554040e00],
                    [0.1666791340e03, 0.3036081233e02, 0.8216820672e01],
                    [0.6464803249e01, 0.1502281245e01, 0.4885884864e00],
                    [0.6464803249e01, 0.1502281245e01, 0.4885884864e00],
                    [0.6464803249e01, 0.1502281245e01, 0.4885884864e00],
                    [0.6464803249e01, 0.1502281245e01, 0.4885884864e00],
                ],
                [
                    [0.1543289673e00, 0.5353281423e00, 0.4446345422e00],
                    [0.1543289673e00, 0.5353281423e00, 0.4446345422e00],
                    [-0.9996722919e-01, 0.3995128261e00, 0.7001154689e00],
                    [0.1559162750e00, 0.6076837186e00, 0.3919573931e00],
                    [0.1559162750e00, 0.6076837186e00, 0.3919573931e00],
                    [0.1559162750e00, 0.6076837186e00, 0.3919573931e00],
                ],
                np.array(
                    [
                        [0.0, 0.0, 0.0],
                        [0.0, 0.0, 1.0],
                        [0.0, 0.0, 1.0],
                        [0.0, 0.0, 1.0],
                        [0.0, 0.0, 1.0],
                        [0.0, 0.0, 1.0],
                    ]
                ),
            ),
        ],
    )
    def test_basisset(self, symbols, geometry, l, alpha, coeff, r):
        r"""Test that the molecule object contains the correct basis set and non-default basis data
        for a given molecule.
        """
        mol = Molecule(symbols, geometry)

        assert set(map(type, mol.basis_set)) == {BasisFunction}
        assert mol.l == l
        assert np.allclose(mol.alpha, alpha)
        assert np.allclose(mol.coeff, coeff)
        assert np.allclose(mol.r, r)

    @pytest.mark.parametrize(
        ("symbols", "geometry", "index", "position", "ref_value"),
        [
            (
                ["H", "H"],
                np.array([[0.0, 0.0, 0.0], [0.0, 0.0, 1.0]]),
                0,
                (0.0, 0.0, 0.0),
                0.62824688,
            ),
        ],
    )
    def test_atomic_orbital(self, symbols, geometry, index, position, ref_value):
        r"""Test that the computed atomic orbital value is correct."""
        mol = Molecule(symbols, geometry)

        x, y, z = position
        ao = mol.get_atomic_orbital(index)
        ao_value = ao(x, y, z)

        assert np.allclose(ao_value, ref_value)

    @pytest.mark.parametrize(
        ("symbols", "geometry", "index", "position", "ref_value"),
        [
            (
                ["H", "H"],
                np.array([[0.0, 0.0, 0.0], [0.0, 0.0, 1.0]], requires_grad=False),
                1,
                (0.0, 0.0, 0.0),
                0.01825128,
            ),
        ],
    )
    def test_molecular_orbital(self, symbols, geometry, index, position, ref_value):
        r"""Test that the computed atomic orbital value is correct."""
        mol = Molecule(symbols, geometry)

        x, y, z = position
        _ = generate_scf(mol)()
        mo = mol.get_molecular_orbital(index)
        mo_value = mo(x, y, z)

        assert np.allclose(mo_value, ref_value)
