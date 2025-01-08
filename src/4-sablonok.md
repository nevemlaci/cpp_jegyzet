# Sablonok (template)

## Sablon alapok
A C++ egyik legnagyobb előnye a C-vel szemben a generikus programozási lehetőségekben rejlik. A jegyzetben már szerepelt az alábbi függvény:

```cpp
//swap C++ -ban
void cpp_swap(int& x, int& y){
    int tmp = x;
    x = y;
    y = tmp;
}
```

Ezt a függvényt szeretnénk megírni, hogy működjön mindenféle típusra. Természetesen ez lehetetlen küldetésnek tűnhet, azonban a C++ templatek fő felhasználási módja éppen ez.

```cpp
template <typename T> //sablondeklaráció, sablonparaméterek(itt T) felsorolása
void cpp_swap(T& x, T&y){ //cpp_swap<T> függvénysablon
    T tmp = x;
    x = y;
    y = tmp;
}
```

A fent látható `cpp_swap` -ot *függvénysablon*nak hívjuk. Önmagában nem függvény, ahhoz "példányosítani" kell. Ez a gyakorlatban annyit jelent, hogy használjuk.

pl.

```cpp
int x = 5;
int y = 2;
// cpp_swap<T> függvénysablon példányosítása T=int sablonparaméterekkel
cpp_swap<int>(x, y); //<int> <- sablonparaméter megadása

double a = 5.2;
double b = 1.2;
cpp_swap<double>(a, b);
```

Amikor egy sablont példányosítunk adott sablonparaméterekkel, olyankor valójában fordításidőben kód generálódik az adott sablonparaméterek behelyettesítésével.
Pl.
```cpp
cpp_swap<int>(x, y); //cpp_swap<T> függvénysablon példányosítása T=int sablonparaméterekkel
```
esetén a
```cpp
void cpp_swap(int& x, int& y){ 
    int tmp = x;
    x = y;
    y = tmp;
}
```
kód generálódik. A `T` helyére mindenhol `int` kerül. Ezt a generált kódot nekük természetesen nem kell látnunk, vagy foglalkoznunk vele.

A sablonparamétereket a fordító néha ki tudja találni a kapott függvényparaméterekből(template parameter deduction).
Például:
```cpp
double a = 5.2;
double b = 1.2;
cpp_swap(a, b); //nem kell megadni, hogy double típus, mivel a és b double típusúak

cpp_swap<double>(a, x); //meg kell adni, hogy double típus, mivel a és x különböző típusúak, így a fordító nem tud dönteni
```

A sablonok(template) használata nagyon elterjedt a C++ programozásban, ezért néhány standard library implementáció gyakran Standard Template Library(STL) -nek nevezi magát(pl. MSVC STL).

## Duck typing

A sablonokkal felmerül egy újabb kérdés: milyen típusokat fogadunk el? A válasz erre egyszerű: mindent, amivel a függvény kódja lefordul.

Ezt "duck typing" -nak hívjuk: *"If it walks like a duck and it quacks like a duck, then it must be a duck"*

Például nézzünk meg egy függvényt, ami megmondja két *valamiről*, hogy az első *valami* nagyobb-e, mint a második *valami*.

```cpp
template<typename T>
bool nagyobbe(T elso, T masodik){
    return elso > masodik;
}
```

Milyen típusokra működik ez a függvény?
Hát azokra, amelyek ezeket a feltételeket teljesítik:
* lemásolhatók (hiszen másolatként vesszük át őket)
* összehasonlíthatók a `>` operátorral

A sablonok korlátozására léteznek további technikák(SFINAE, concept), azonban ezek messze túlmutatnak a tárgy anyagán.

## Nem-típus sablonparaméterek, nem-függvény sablonok

Sablonparaméterként átadható nem csak típus, hanem gyakorlatilag bármilyen más objektum is. Pl. a standard library egy típusa az `std::array`, amely első függvényparamétere a tömbben tárolt típus, második függvényparamétere egy pozitív egész szám, a tömb mérete.

```cpp
std::array<int, 5> tomb; //5 méretű int-eket tároló tömb
```

Ezt kódban a következőként "replikálhatjuk":
```cpp
template<typename T, std::size_t siz>
struct array{ // array<T, siz> "osztálysablon"(osztályok később)
    T belso_tomb[siz];
    //array implementáció...
};

template <int N>
void print_template_int(){
    std::cout << N << '\n';
}
```
Fontos azt megjegyezni, hogy a sablonok fordításidőben példanyosodnak, szóval minden függvényparaméternek fordításidőben konstansnak kell lennie.
pl.
```cpp
print_template_int<5>(); //ok
int x = 5;
print_template_int<x>(); //hiba, x nem fordításidejű konstans(const sem oldaná meg)
```
## Részleges specializáció

Tegyük fel, hogy szeretnénk ha egy adott sablon egy speciális módon működjön, ha egy adott típust kap. 
Például ha a swap függvényünk int-et kap, akkor írja ki, hogy "int", különben működjön normális módon.

```cpp
template <typename T> 
void cpp_swap(T& x, T&y){ 
    T tmp = x;
    x = y;
    y = tmp;
}

template <> 
void cpp_swap<int>(int& x, int&y){ //specializáció a T=int esetre
    std::cout << "int";
    T tmp = x;
    x = y;
    y = tmp;
}
```