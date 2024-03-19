from utils.utils import get_table_key
from typing import Any



class BigTable(object):
    
    def __init__(self, 
            vertical_length: int, 
            horizontal_length: int, 
            null_offset:int = 1, 
            default_value=None
            ):
        
        self.x_axis = range(null_offset, horizontal_length+null_offset)
        self.y_axis = range(null_offset, vertical_length+null_offset)
        self.null_offset = null_offset
        self.cells: dict[int, Any] = {}
        self.default_value = default_value
        
    def __repr__(self) -> str:
        return str(self.get_all())
        
    def x_is_on_axis(self, x):
        return x in self.x_axis
    
    def y_is_on_axis(self, y):
        return y in self.y_axis
        
    def get(self, x: int, y: int) -> Any:
        key = get_table_key(x, y)
        if not self.cells.get(key):
            return self.default_value
        return self.cells[key]
    
    def get_all_x(self, x: int):
        resp = {}
        if not self.x_is_on_axis(x):
            raise ValueError(f"{x} is not on y axis.")
        for y in self.y_axis:
            resp[get_table_key(x, y)] = self.get(x, y)
        return resp
    
    def get_all_y(self, y: int):
        resp = {}
        if not self.y_is_on_axis(y):
            raise ValueError(f"{x} is not on x axis.")
        for x in self.x_axis:
            resp[get_table_key(x, y)] = self.get(x, y)
        return resp
    
    def get_all(self):
        #! may be very slow if table contains a lot of cells
        return self.cells
    
    def update_v(self, x: int, y: int, new_v: Any) -> None:
        self.cells[get_table_key(x, y)] = new_v
        
    def clear(self):
        self.cells = {}
        
    def full_fill(self, v):
        self.clear()
        self.default_value = v
        
    def partial(self, x_start: int, x_end: int, y_start: int, y_end: int):
        # if any arg is -1 it will be loaded fully
        if x_start == -1:
            x_start = self.x_axis[0]
        if x_end == -1:
            x_start = self.x_axis[-1]
        if y_start == -1:
            y_start = self.y_axis[0]
        if y_end == -1:
            y_end = self.y_axis[-1]
        resp = {}
        for x in range(x_start, x_end):
            for y in range(y_start, y_end):
                resp[get_table_key(x, y)] = self.get(x, y)
        return resp
    
    def dump(self):
        return {
            "range": {
                "null_offset": self.null_offset,
                "x": {
                    "start": self.x_axis[0],
                    "end": self.x_axis[-1]
                },
                "y": {
                    "start": self.y_axis[0],
                    "end": self.y_axis[-1]
                }
            },
            "default": self.default_value,
            "cells": self.cells
        }
    
    def load(self, data: dict):
        self.null_offset = data["range"]["null_offset"]
        self.default_value = data["default"]
        self.cells = data["cells"]
        self.x_axis = range(data["range"]["x"]["start"], data["range"]["x"]["end"])
        self.y_axis = range(data["range"]["y"]["start"], data["range"]["y"]["end"])
        
     
table = BigTable(36000, 500)
 
import time
x_ = 360
y_ = 100

start = time.perf_counter()   
table.full_fill(1000_000)  
end = time.perf_counter()
print(end-start)
t_ = table.dump()
print(t_)
new_t = BigTable(1, 1)
new_t.load(t_)
print(new_t.get(25, 25))
print(new_t.partial(1, 17, 20, 90))