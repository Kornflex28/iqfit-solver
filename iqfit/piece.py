import numpy as np


class Piece:
    def __init__(self, name="square", coordinates={(0, 0, 0), (0, 1, 0), (1, 0, 0), (1, 1, 0)}):
        self.name = name
        self.coordinates = coordinates
        self.width = max(coordinates, key=lambda x: x[0])[0]+1
        self.height = max(coordinates, key=lambda x: x[1])[1]+1
        self.depth = max(coordinates, key=lambda x: x[2])[2]+1

    def __repr__(self):
        return f"Piece(name={self.name},coordinates={self.coordinates})"

    def __str__(self):
        rep1, rep2, ch = "", "", self.name[0]
        for y in range(self.height):
            rep1 += "\n"
            for x in range(self.width):
                if (x, y, 0) in self.coordinates:
                    rep1 += ch
                else:
                    rep1 += " "
        self_rot = self.from_array(
            name=self.name, array=self.from_array_rotate_3D(self.to_array()))
        for y in range(self_rot.height):
            rep2 += "\n"
            for x in range(self_rot.width):
                if (x, y, 0) in self_rot.coordinates:
                    rep2 += ch
                else:
                    rep2 += " "

        return f"Piece: {self.name}{rep1}\n{self.width*'-'}{rep2}"

    def to_array(self):
        piece = np.zeros((self.height, self.width, self.depth))
        for x, y, z in self.coordinates:
            piece[y, x, z] = 1
        return piece

    def translate_piece(self,dx=0,dy=0):
        return Piece(self.name,{(x+dx,y+dy,z) for x,y,z in self.coordinates})

    def get_transformations(self):
        piece = self.to_array()
        piece_rot3D = self.from_array_rotate_3D(piece)
        return [self.from_array_to_coordinates(array) for array in self.from_array_get_2D_rotations(piece)+self.from_array_get_2D_rotations(piece_rot3D)]

    def get_2D_coordinates(self):
        return {(x,y) for x,y,z in self.coordinates if z==0}

    @classmethod
    def from_array_to_coordinates(cls,array):
        return set([(y, x, z) for x in range(array.shape[0]) for y in range(array.shape[1]) for z in range(array.shape[2]) if array[x, y, z]])

    @classmethod
    def from_array(cls, name, array):
        return cls(name=name, coordinates=cls.from_array_to_coordinates(array))  

    @classmethod
    def from_array_rotate_3D(cls, array):
        ax = np.argmax(array.shape[:2])
        n_rot = 1 + 2 * array.sum(axis=ax).argmax(axis=0)[0]
        rot_axs= tuple(i for i in range(3) if i !=ax)
        # print(ax,rot_axs)
        return np.rot90(array, k=n_rot, axes=rot_axs)

    @classmethod
    def from_array_get_2D_rotations(cls, array):
        return [np.rot90(array, k=k, axes=(0,1)) for k in range(4)]

    @classmethod
    def iqfit_pieces(cls):
        return {"Blue": cls("Blue", {(0, 0, 0), (0, 0, 1), (1, 0, 0), (2, 0, 0), (2, 0, 1), (1, 1, 0)}),
                "Yellow": cls("Yellow", {(0, 0, 0), (0, 0, 1), (1, 0, 0),
                                         (2, 0, 0), (3, 0, 0), (2, 1, 0), (3, 1, 0)}),
                "Red": cls("Red", {(0, 0, 0), (0, 0, 1), (1, 0, 0),
                                   (2, 0, 0), (3, 0, 0), (3, 0, 1), (0, 1, 0)}),
                "Sky": cls("Sky", {(0, 0, 0), (0, 0, 1), (1, 0, 0),
                                   (2, 0, 0), (2, 0, 1), (3, 0, 0), (0, 1, 0)}),
                "Magenta": cls("Magenta", {(0, 0, 0), (1, 0, 0), (1, 0, 1),
                                           (2, 0, 0), (3, 0, 0), (0, 1, 0), (1, 1, 0)}),
                "Orange": cls("Orange", {(0, 0, 0), (1, 0, 0), (1, 0, 1),
                                         (2, 0, 0), (3, 0, 0), (3, 0, 1), (1, 1, 0)}),
                "Green": cls("Green", {(0, 0, 0), (0, 0, 1), (1, 0, 0),
                                       (2, 0, 0), (2, 0, 1), (0, 1, 0)}),
                "Forest": cls("Forest", {(0, 0, 0), (1, 0, 0),
                                         (1, 0, 1), (2, 0, 0), (2, 0, 1), (1, 1, 0)}),
                "Cyan": cls("Cyan", {(0, 0, 0), (1, 0, 0), (1, 0, 1),
                                     (2, 0, 0), (2, 0, 1), (3, 0, 0), (1, 1, 0)}),
                "Purple": cls("Purple", {(0, 0, 0), (0, 0, 1),
                                         (1, 0, 0), (1, 0, 1), (2, 0, 0), (2, 1, 0)})
                }
