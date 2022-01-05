# data_parser

C++ program for fast preprocessing of the `combined_data_*.txt` files (< 1min on a 2020 MacBook Pro).

The format of these files is roughly like this:

```csv
movie_id:
reviewer_id,rating,date
reviewer_id,rating,date
...
```

Since this format is hard to use in the python program, we want to add the `movie_id` to all rows to get a plain CSV format.

## compiling

1. `mkdir build`
2. `cd build`
3. `cmake ..`
4. `make`

By default, the program is compiled in "binary" mode, meaning that the output is binary. If the define `BINARY` is undefined, the output will be plain CSV.

## usage

```bash
./data_parser combined_data_*.txt > preprocessed_reviews_all.bin
```

**Output (binary)**

Each review will produce 7 bytes:

* 2 Bytes Movie Id (Big Endian)
* 4 Bytes Customer Id (Big Endian)
* 1 Byte Rating

It can be loaded with `numpy` using this `dtype`

```python
np.dtype([('movie_id', '>u2'),
          ('customer_id', '>u4'),
          ('rating', '>u1')])
```

**Output (plain CSV)**

```text
movie_id,customer_id,rating
movie_id,customer_id,rating
...
```