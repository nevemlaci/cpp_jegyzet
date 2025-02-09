## Build

[Mdbook](https://github.com/rust-lang/mdBook)-al buildelhető.

```
git clone https://github.com/nevemlaci/cpp_jegyzet
cd cpp_jegyzet
mdbook serve
```

`mdbook serve` egy interaktív előnézeted ad a `http://localhost:3000` címen, minden változtatásra frissíteni fogja ezt az előnézetet.

`mdbook build` elkészíti a HTML leképzést a `book` könyvtárba.

A `publish.bat` file segítségével automatikusan remote repoba pusholható a könyv forráskódja és a `book` almappa is.
