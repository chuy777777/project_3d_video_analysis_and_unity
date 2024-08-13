class TemplateFrame():
    def __init__(self, father, name, grid_frame, grid_information):
        self.father=father
        self.name=name
        self.grid_frame=grid_frame
        self.grid_information=grid_information
        self.elements={}
        self.is_visible=True
    
    # Este metodo se debe sobreescribir
    def create_specific_grid_frame(self, grid_frame):
        pass

    # Este metodo se debe sobreescribir
    def hide_frame(self):
        pass

    # Este metodo se debe sobreescribir
    def show_frame(self):
        pass
    
    # Este metodo se debe sobreescribir
    def enable_fixed_size(self):
        pass

    # Este metodo se debe sobreescribir
    def desable_fixed_size(self):
        pass

    def element_exists(self, cad_pos):
        return self.key_exists(cad_pos=cad_pos) and self.elements[cad_pos]["element"].winfo_exists()
    
    def key_exists(self, cad_pos):
        return cad_pos in list(self.elements.keys())
    
    def insert_element(self, cad_pos, element, **kwargs):
        if element is not None:
            i,j=[int(val) for val in cad_pos.split(",")]
            columnspan=self.grid_frame.dict[cad_pos]["columnspan"]
            rowspan=self.grid_frame.dict[cad_pos]["rowspan"]
            element.grid(row=i, column=j, rowspan=rowspan, columnspan=columnspan, **kwargs)
            self.elements[cad_pos]={"element": element}
            return element
        return None

    def get_element(self, cad_pos):
        if self.key_exists(cad_pos=cad_pos) and self.element_exists(cad_pos=cad_pos):
            return self.elements[cad_pos]["element"]
        return None
    
    def destroy_element(self, cad_pos):
        if self.key_exists(cad_pos=cad_pos) and self.element_exists(cad_pos=cad_pos):
            self.elements[cad_pos]["element"].destroy()
            del self.elements[cad_pos]

    def destroy_all(self):
        keys=list(self.elements.keys())
        for cad_pos in keys:
            self.destroy_element(cad_pos=cad_pos)

    # Obtiene un frame en el arbol (la busqueda es de abajo hacia arriba)
    def get_frame(self, frame_name, frame=None):
        if frame is None:
            frame=self

        if hasattr(frame, 'father'):
            if frame.name == frame_name:
                return frame
            else:
                return self.get_frame(frame_name=frame_name, frame=frame.father)
        else:
            return None
