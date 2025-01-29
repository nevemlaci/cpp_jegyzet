# Dinamikus memóriakezelés

## C dinamikus memóriakezelés

A C dinamikus memóriakezelése a kőkorszakban jár. Megkérdezi hány bájtnyi memóriára van szükségünk, majd visszadob rá egy pointert.

## C++ memóriakezelés

A C++ `malloc` függvényét a `new` operátor(igen, ezek operátorok), a `free` függvényt pedig a `delete` és `delete[]` operátor váltotta fel.

A `new` egy intelligens eszköz. Nem memóriamennyiséget, hanem egy típust és opcionálisan egy tömbméretet kap. 
Pl.
```cpp

int* x = new int; //egy darab dinamikusan foglalt int

int* tomb = new int[5]; //egy dinamikusan foglalt 5 méretű tömb

std::size_t tombMeret; //std::size_t : általában memóriafoglalások méretét vagy indexeket tároló előjel nélküli egész

std::cin >> tombMeret;

int* dinTomb = new int[tombMeret];
```

A `delete` operátor a `new` operátorral lefoglalt memóriát szabadítja fel. Ha tömböt szabadítunk fel, akkor a `delete[]` operátort kell használni.

Az előbbi példa foglalások felszabadítása:
```cpp
delete x;
delete[] tomb;
delete[] dinTomb;
```

## Variable Length Array

Az alábbi kódrészlet az ISO C++ Standard szerint nem szabványos C++, a GCC és Clang fordítók compiler extensionként engedélyezik. VLA-t ne használjunk, hiszen így a stacken szükséges memória mérete ismeretlen lesz.

<https://godbolt.org/z/93xxj5WPM>
```cpp
int x;
std::cin >> x;
int a[x];
```

*A non-standard extension-ök kikapcsolása:*
* GCC/Clang: `-pedantic-errors` flag
* MSVC: `/fpermissive-` flag