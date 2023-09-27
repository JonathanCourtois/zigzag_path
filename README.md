# zigzag_path
Python library that give waypoint coordinate when drawing a zigzag in a rectangular area.

this library was build for this paper :
- [paper_name](https:404)

## How to use it
### import 
```python
import drawings_zigzag as dzz

# define draw area
h, w = 40, 30
da = dzz.area(h,w)

# call the path builder with your parameters
path_builder = dzz.path_builder(da, nb_brin=3, base_brin_length=5, start_pos_top=True)

# to get path list use :
path = path_builder.path_list

# Draw your path
# path_builder.debug_lines_factors(show=False)
path_builder.draw_path()
```
<p align="center">
  <img src="https://github.com/JonathanCourtois/zigzag_path/blob/main/example.png" title="example">
</p>

## Publications and Citation

If you use zigzag_path in your work, please cite it as follows:

```
@misc{x,
	title = {x},
	author = {x,x,x,x},
	year = {x},
	howpublished = {x}},
	note = {Accessed: YYYY-MM-DD},
}
```
