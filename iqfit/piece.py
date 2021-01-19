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
        rep1,rep2, ch = "","", self.name[0]
        for y in range(self.height):
            rep1 += "\n"
            for x in range(self.width):
                if (x, y, 0) in self.coordinates:
                    rep1 += ch
                else:
                    rep1 += " "
        self_rot = self.from_array(name=self.name,array=self.from_array_rotate_3D(self.to_array()))
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

    @classmethod
    def from_array(cls, name, array):
        return cls(name=name, coordinates=set([(y, x, z) for x in range(array.shape[0]) for y in range(array.shape[1]) for z in range(array.shape[2]) if array[x, y, z]]))

    def get_transformations(self):
        piece = self.to_array()
        return
    
    @classmethod
    def from_array_rotate_3D(cls, array):
        n_rot = 1 + 2 * array.sum(axis=1).argmax(axis=0)[0]
        return np.rot90(array, k=n_rot, axes=(0, 2))
