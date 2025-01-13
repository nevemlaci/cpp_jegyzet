## Build

Build using [mdbook](https://github.com/rust-lang/mdBook), an awesome project for writing digital content.

```
git clone https://github.com/nevemlaci/cpp_jegyzet
cd cpp_jegyzet
mdbook serve
```

`mdbook serve` will deploy the book on `http://localhost:3000` and will listen for any changes to the book and update the site on any change.

`mdbook build` will build the book and output it as HTML into the `book` directory