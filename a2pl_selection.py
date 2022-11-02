

# num_objet, num_face courant
class Selection:
    """
    Class to simulate false selection of two faces as input of a2+ without GUI.
    """
    def __init__(self, document, id_obj, id_face):

        self.solids_objects = []
        for k, obj in enumerate(document.getObject('SolidObjects').Group):
            if obj.TypeId[:4] == 'Part':
                self.solids_objects.append(obj)

        self.Object = self.solids_objects[id_obj]
        self.ObjectName = self.Object.Name
        self.SubElementNames = ["Face"+str(id_face+1)]
        self.Face = self.Object.Shape.Faces[id_face]
        self.id_obj = id_obj
        self.id_face = id_face


