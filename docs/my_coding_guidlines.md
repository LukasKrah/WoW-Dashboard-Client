```python
class Example(Parent):
    """
    This is a example class
    """
    master: any
    must_pos_param1: str
    must_pos_param2: str
    
    optional_kw_param1: str
    optional_kw_param2: str

    othervar: int

    def __init__(self, 
                 master: any, 
                 must_pos_param1: str, 
                 must_pos_param2: str, 
                 *args: any,
                 optional_kw_param1: str, 
                 optional_kw_param2: str,
                 **kwargs: any) -> None:
        """
        Create example class
        """
        # Params
        self.master = master
        self.must_pos_param1 = must_pos_param1
        self.must_pos_param2 = must_pos_param2
        
        self.optional_kw_param1 = optional_kw_param1
        self.optional_kw_param2 = optional_kw_param2
        
        # Parent init
        super().__init__(master, *args, **kwargs)
        
        # Other vars
        othervar = 0
        
        self._create_widgets()
        self.grid_widgets()
        
    def _create_widgets(self) -> None:
        """
        This function should create all grapical elems
        and should only get called from the __init__ once
        """
        ...
        
    def grid_widgets(self) -> None:
        ...
        
    def reload(self) -> None:
        ...
        
    def __resize(self, event: Event) -> None:
        ...


```