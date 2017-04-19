import unittest
from corneal.body import Body, naca_airfoil, flat_plate
from corneal.panel import *
import numpy as np

class TestPanel(unittest.TestCase):
    def test_single_panel_aligned(self):
        x = [1, 0]
        y = [0, 0]
        points = np.vstack([x, y])
        body = Body(points)
        body_panels = BoundVortices(body)
        body_panels.update_strengths()
        gam = body_panels.vortices.strengths
        self.assertEqual(gam, 0)

    def test_single_panel_normal(self):
        x = [0, 0]
        y = [0, 1]
        points = np.vstack([x, y])
        body = Body(points)
        body_panels = BoundVortices(body)
        body_panels.update_strengths()
        gam = body_panels.vortices.strengths
        self.assertEqual(gam, -np.pi)

    def check_shed_vortex(self, body, wake_fac):
        panels = BoundVortices(body)
        Uinfty = (1,0)
        dt = 1
        panels.update_strengths_unsteady(dt, Uinfty, None, wake_fac=wake_fac)
        gam = panels.vortices.strengths
        x_shed, gam_shed = panels.get_newly_shed()
        gam_sum = np.sum(gam)
        self.assertAlmostEqual(gam_shed, -gam_sum)
        np.testing.assert_array_almost_equal(x_shed, (1 + wake_fac, 0))

    def test_shed_vortex_thick(self):
        body = naca_airfoil("0012", 8)
        self.check_shed_vortex(body, 0.2)
        self.check_shed_vortex(body, 0.3)

    def test_shed_vortex_thin(self):
        body = flat_plate(8)
        self.check_shed_vortex(body, 0.2)
        self.check_shed_vortex(body, 0.3)

    def test_regularization(self):
        pass

if __name__ == "__main__":
    unittest.main()
