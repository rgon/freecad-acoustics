
# FreeCAD parametric FeaturePython object for a "Paraline" profile
# Usage: Run inside FreeCAD's Python console or as a macro

import FreeCAD as App
import FreeCADGui as Gui
import Part
import math

def get_a(H:float, resolution:float = 0.05) -> list[float]:
    # Generalized generation of points to calculate the Paraline Points
    A = []
    # Range does not support floats, so we cannot use range(-1.0, 1.0, resolution):
    num_steps = int(2 / resolution) + 1
    for i in range(num_steps):
        A.append(H * (i / (num_steps - 1) * 2 - 1))
    return A

class ParalineFeature(object):
    def __init__(self, obj):
        obj.Proxy = self
        self.Type = "ParalineFeature"
        obj.addProperty("App::PropertyLength", "H", "Paraline", "Height parameter").H = 30.0
        obj.addProperty("App::PropertyLength", "ExtrudeHeight", "Paraline", "Extrusion height").ExtrudeHeight = 10.0
        # Add resolution property (unit-aware)
        obj.addProperty("App::PropertyFloat", "Resolution", "Paraline", "Resolution parameter").Resolution = 0.05

    def execute(self, obj):
        H = obj.H
        extrude_height = obj.ExtrudeHeight
        resolution = obj.Resolution

        # Step 3: Solve triangle for each Ai (right side)
        right_points = []
        for Ai in get_a(H, resolution):
            B = (H**2 - Ai**2) / (2 * H)
            right_points.append(App.Vector(B, -Ai, 0))
        # Add the starting point
        # right_points.insert(0, App.Vector(0, 0, 0))

        # Mirror over Y axis (left side)
        left_points = [App.Vector(-pt.x, pt.y, pt.z) for pt in reversed(right_points)]

        # Combine points, remove duplicate at (0,0,0) in the middle
        all_points = right_points + left_points[1:]
        # Close the shape
        all_points.append(all_points[0])

        # Create a wire from the points
        wire = Part.makePolygon(all_points)
        face = None
        if wire.isClosed():
            try:
                face = Part.Face(wire)
            except Exception:
                face = None

        # Extrude the face
        if face:
            solid = face.extrude(App.Vector(0, 0, extrude_height))
            obj.Shape = solid
        else:
            obj.Shape = wire


# Optional: ViewProvider for custom icon/appearance
class ViewProviderParaline(object):
    def __init__(self, obj):
        obj.Proxy = self
    def attach(self, obj):
        pass
    def updateData(self, fp, prop):
        pass
    def getDisplayModes(self, obj):
        return []
    def getDefaultDisplayMode(self):
        return "Shaded"
    def setDisplayMode(self, mode):
        return mode
    def onChanged(self, vp, prop):
        pass
    def getIcon(self):
        return ""
    def __getstate__(self):
        return None
    def __setstate__(self, state):
        return None

# --- Add the parametric object to the document ---
doc = App.ActiveDocument if App.ActiveDocument else App.newDocument("ParalineDoc")
paraline = doc.addObject("Part::FeaturePython", "Paraline")
ParalineFeature(paraline)
ViewProviderParaline(paraline.ViewObject)
doc.recompute()

# --- Optionally fit view if running in GUI ---
try:
    Gui.activeDocument().activeView().viewAxometric()
    Gui.SendMsgToActiveView('ViewFit')
except Exception:
    pass