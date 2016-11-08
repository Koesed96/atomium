from unittest import TestCase
import unittest.mock
from molecupy.structures import GhostAtom

class GhostAtomCreationTests(TestCase):

    def test_can_create_ghost_atom(self):
        atom = GhostAtom("C", 100, "CA")
        self.assertEqual(atom._element, "C")
        self.assertEqual(atom._atom_id, 100)
        self.assertEqual(atom._atom_name, "CA")
        self.assertEqual(atom._molecule, None)


    def test_repr(self):
        atom = GhostAtom("C", 100, "CA")
        self.assertEqual(str(atom), "<GhostAtom 100 (CA)>")


    def test_element_must_be_str(self):
        with self.assertRaises(TypeError):
            atom = GhostAtom(9, 100, "CA")


    def test_element_must_be_correct_length(self):
        with self.assertRaises(ValueError):
            atom = GhostAtom("", 100, "CA")
        with self.assertRaises(ValueError):
            atom = GhostAtom("CAC", 100, "CA")
        atom = GhostAtom("MG", 100, "CA")
        atom = GhostAtom("M", 100, "CA")


    def test_atom_id_must_be_int(self):
        with self.assertRaises(TypeError):
            atom = GhostAtom("C", "100", "CA")


    def test_atom_name_must_be_str(self):
        with self.assertRaises(TypeError):
            atom = GhostAtom("C", 100, 1.5)



class GhostAtomPropertyTests(TestCase):

    def setUp(self):
        self.atom = GhostAtom("C", 100, "CA")


    def test_basic_properties(self):
        self.assertEqual(self.atom.element(), "C")
        self.assertEqual(self.atom.atom_id(), 100)
        self.assertEqual(self.atom.atom_name(), "CA")
        self.assertEqual(self.atom.molecule(), None)


    def test_basic_property_update(self):
        self.atom.element("H")
        self.assertEqual(self.atom.element(), "H")
        self.atom.atom_name("C")
        self.assertEqual(self.atom.atom_name(), "C")


    def test_element_must_be_str(self):
        with self.assertRaises(TypeError):
            self.atom.element(100)


    def test_element_must_be_correct_length(self):
        with self.assertRaises(ValueError):
            self.atom.element("")
        with self.assertRaises(ValueError):
            self.atom.element("CAC")
        self.atom.element("MG")
        self.atom.element("M")


    def test_atom_name_must_be_str(self):
        with self.assertRaises(TypeError):
            self.atom.atom_name(100)




class GhostAtomMassTests(TestCase):

    def test_can_get_atom_mass(self):
        lithium = GhostAtom("Li", 1, "Li")
        sodium = GhostAtom("Na", 1, "Na")
        iron = GhostAtom("Fe", 1, "Fe")
        uranium = GhostAtom("U", 1, "U")
        self.assertAlmostEqual(lithium.mass(), 7, delta=0.5)
        self.assertAlmostEqual(sodium.mass(), 23, delta=0.5)
        self.assertAlmostEqual(iron.mass(), 56, delta=0.5)
        self.assertAlmostEqual(uranium.mass(), 238, delta=0.5)


    def test_strange_elements_have_zero_mass(self):
        mysterium = GhostAtom("My", 1, "My")
        self.assertEqual(mysterium.mass(), 0)



class GhostAtomModelTests(TestCase):

    def test_can_get_model_through_small_molecule(self):
        atom = GhostAtom("C", 100, "CA")
        small_molecule = unittest.mock.Mock()
        atom._molecule = small_molecule
        small_molecule.model.return_value = "model"
        self.assertEqual(atom.model(), "model")


    def test_can_get_model_through_chain(self):
        atom = GhostAtom("C", 100, "CA")
        residue = unittest.mock.Mock()
        residue.model.side_effect = AttributeError()
        atom._molecule = residue
        chain = unittest.mock.Mock()
        residue.chain.return_value = chain
        chain.model.return_value = "model"
        self.assertEqual(atom.model(), "model")