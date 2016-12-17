from unittest import TestCase
from tests.assertions import CustomAssertions
import floq.optimization.fidelity as fid
from floq.systems.spins import SpinEnsemble
import numpy as np
from mock import MagicMock


class TestFidelityComputerBaseIterations(TestCase):
    def setUp(self):
        self.computer = fid.FidelityComputerBase(None)
        self.computer._f = MagicMock()
        self.computer._df = MagicMock()

    def test_increase_iterations(self):
        self.computer.f(np.ones(3))
        self.computer.f(2*np.ones(3))
        self.computer.df(2*np.ones(3))
        self.computer.f(2*np.ones(3))
        self.assertEqual(self.computer.iterations, 2)

    def test_reset(self):
        self.computer.reset_iterations()
        self.assertEqual(self.computer.iterations, 0)

    def test_iterate_gets_called(self):
        iterate = MagicMock()
        self.computer._iterate = iterate
        self.computer.f(np.ones(3))
        self.computer.f(2*np.ones(3))
        self.computer.df(2*np.ones(3))
        self.computer.f(2*np.ones(3))
        self.computer.f(3*np.ones(3))
        self.assertEqual(iterate.call_count, self.computer.iterations)



class TestEnsembleFidelity(TestCase, CustomAssertions):
    def setUp(self):
        self.ensemble = SpinEnsemble(2, 2, 1.5, np.array([1.1, 1.1]), np.array([1, 1]))


    def test_correct_in_one_case(self):
        target = np.array([[0.105818 - 0.324164j, -0.601164 - 0.722718j],
                           [0.601164 - 0.722718j, 0.105818 + 0.324164j]])

        f = fid.EnsembleFidelity(self.ensemble, fid.OperatorDistance, t=1.0, target=target)
        print f.f(np.array([1.5, 1.5, 1.5, 1.5]))
        self.assertTrue(np.isclose(f.f(np.array([1.5, 1.5, 1.5, 1.5])), 0.0, atol=1e-5))
