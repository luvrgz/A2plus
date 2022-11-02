import freecad
import FreeCAD
import Part
import time
import math
import numpy as np


class Force:
    def __init__(self, pt: FreeCAD.Vector, direction: FreeCAD.Vector, amp: float()):
        self.application_point = pt
        self.direction = direction.normalize()
        self.amplitude = amp


class Collider:
    def __init__(self, object1, object2):
        self.names = [object1.Name, object2.Name]
        self.tol_inside = 0.05  # tolerance for common volume
        self.coeff_amplitude = 2  # Multplied by common volume
        self.shape = [object1.Shape, object2.Shape]
        self.collide = False
        self.forces_on_1 = list()
        self.forces_on_2 = list()

    # Check if two shapes collides
    def calculate(self):
        # Vérification BoundBox
        if not self.shape[0].BoundBox.intersect(self.shape[1].BoundBox):
            self.collide = False
            return

        # Same location/geometry verification
        if self.shape[0].hashCode() == self.shape[1].hashCode():
            self.collide = True
            return

        # common occ function
        common_shape = self.shape[0].common(self.shape[1])
        # obj = FreeCAD.ActiveDocument.addObject("Part::Feature", "common")
        # obj.Shape = common_shape
        # FreeCAD.ActiveDocument.save()

        if common_shape.Volume <= self.tol_inside:
            self.collide = False
            return

        for solid in common_shape.Solids:
            pt_application = solid.CenterOfMass
            amplitude = solid.Volume * self.coeff_amplitude

            # Calcul de direction
            bb = solid.BoundBox
            # bb.enlarge(1.0)  # in millimeter, not necessary for now
            bb_shape = Part.makeBox(bb.XLength, bb.YLength, bb.ZLength)
            bb_shape.Placement.Base = FreeCAD.Vector(bb.XMin, bb.YMin, bb.ZMin)

            s1_reduced = bb_shape.common(self.shape[0])
            s2_reduced = bb_shape.common(self.shape[1])

            # obj = FreeCAD.ActiveDocument.addObject("Part::Feature", "s2_reduced")
            # obj.Shape = s2_reduced
            # FreeCAD.ActiveDocument.save()

            dir_on_1 = s1_reduced.Solids[0].CenterOfMass - s2_reduced.Solids[0].CenterOfMass

            self.forces_on_1.append(Force(pt_application, dir_on_1, amplitude))
            self.forces_on_2.append(Force(pt_application, - dir_on_1, amplitude))

        self.collide = True
        return


if __name__ == "__main__":
    from tabulate import tabulate
    import Ressources.config as C

    doc = FreeCAD.openDocument(C.TMP_PATH + "\\first_11.FCStd")

    s1 = doc.Objects[1]
    s2 = doc.Objects[5]
    col = Collider(s1, s2)
    col.calculate()
    print(col.collide)

