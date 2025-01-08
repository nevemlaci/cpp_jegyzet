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

