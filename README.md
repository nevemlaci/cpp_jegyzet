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

#### Példák:

Buildeli a könyvet, ezután a "foo bar" üzenettel új commitot hoz létre. Az `origin` remotera pusholja a forráskódot, a `book` branchre pusholja a könyv tartalmát.
```
./publish.bat "foo bar"
```

Ugyanaz, mint az előző, csak nem pushol remote repoba
```
./publish.bat "foo bar" --no_push
```

Nem csinál commitot, az eddigi nem pusholt commitokat pusholja repoba
```
./publish.bat --only_push
```

Linuxról alternatívaként közvetlen invokeolható a `python.py` script, az argumentumok ugyanazok, például:
```
python publish.py "foo bar" --no_push
```