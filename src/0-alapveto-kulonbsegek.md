# Alapvető különbségek a C nyelvtől

## A `bool`, mint nyelvi elem

A `bool` típus, habár a C nyelv újabb verzióiban nyelvi elemként szerepel, a Prog1 még nem tanítja. A C++ nyelvnek szerencsére része a `bool` típus, nem kell ehhez a legújabb verziókat használni.

```cpp
bool x = true; //nem kell semmilyen include
```

## Struktúra és typedef

A C nyelvben a struktúrák önmagukban nem, csak a `struct` előtaggal voltak egyéni típusnevek. Ez C++ -ban másképp van, itt a struktúra neve `typedef` nélkül is egyéni típusnév.

```cpp
struct foo{
    int a;
};

int main(){
    foo f;
    f.a = 5;
}
```

## C Standard Library headerek

A C standard library header-jei a C++ nyelvben is léteznek, viszont a `.h` kiterjesztést elvesztették, és egy `c` előtagot kaptak. Pl.
```
#include <stdio.h> -> #include <cstdio>
```

## Névterek(namespace)

C-ben gyakori az, hogy egy név már használva van például egy header file-ban ezért bárhol, ahol ez a header include-olva van, ez a név "foglalt" lesz. Ezt sok könyvtár a név prefixelésével oldja meg, pl. `SDL_Texture`.

Erre a C++ -nak beépített nyelvi eleme van, ezek pedig a névterek.

```cpp
#include <cstdio>

namespace foo{
    void f(){
        std::printf("foo");
    }

    namespace bar{
        void f(){
            std::printf("bar");
        }
    }
}

int main(){
    foo::f();
    foo::bar::f();
}
```

A névtereken belüli neveket a `::` operátorral érhetjük el. A `printf` előtti `std` névtér a standard library névtere, ez tartalmazza az összes standard library által tartalmazott szimbólumot(függvények, struktúrák, stb.), éppen azért, hogy az stdlib által használt gyakori nevek(pl. vector) ne ütközzenek más kóddal.



## Function overloading

C++ -ban ugyanazon nevű függvény többféle paramétereket vehet át.

```cpp
#include <cstdio>

void foo(double x){
    std::printf("%lf double", x);
}

void foo(int x){
    std::printf("%d int", x);
}

int main(){
    foo(5); // 5 int
    foo(3.2); // 3.2 double
}
```

## Referenciák

C-ből ismert a pointerek fogalma. Ezt sokszor arra használjuk, hogy egy függvényben a paraméterként kapott eredeti objektumot módosítsuk, vagy hogy egy másolást elkerüljünk.
Erre valók C++ban a *referenciák*

```cpp
//swap függvény C-ben

void c_swap(int* x, int* y){
    int tmp = *x;
    *x = *y;
    *y = tmp;
}

//swap C++ -ban
void cpp_swap(int& x, int& y){
    int tmp = x;
    x = y;
    y = tmp;
}
```

A referenciák konstansok, azaz egy referencia az élettartama alatt nem tud hirtelen másik objektumra mutatni.
```cpp
int x = 5;
int y = 1;
int& xr = x;
xr = y; //ugyan az, mint x = y;
```
Gondolhatunk a referenciára úgy, mint egy 'alias' -ra (alternatív név). Megmondjuk, minek az alias-a, majd utána az eredeti változó helyett használjuk.

Fontos megjegyezni, hogy ugyan úgy mint a pointereknél, lokális változóra mutató referenciával *tilos* visszatérni.

## A const kulcsszó

A `const` kulcsszó a C nyelvnek is része, viszont C++ban egy sokkal fontosabb szerepe van, amivel később találkozunk még.

Jelentése nevéből adódik, egy `const` objektumot "nem lehet megváltoztatni". A kulcsszó mindig a tőle azonnal balra található dologra vonatkozik, kivéve ha a `const` az első, akkor a tőle azonnal jobbra található elemre vonatkozik. 
Fontos azt megemlíteni, hogy a `const` nem fordításidejű konstans értéket jelöl, inkább a programozó felé jelzés. Régebben a fordítók optimalizálásra is használták, viszont ennek a jelentősége ma már elenyésző, viszont a kulcsszó használata ettől még esszenciális marad.

Pélák:
```cpp
int x; // sima, változtatható egész
int const pi = 3.14; //konstans egész
const int pi = 3.14; //ugyanaz, mint az előző

const int* p = &pi; // pointer egy konstans egészre
int const * p = &pi; //ugyanaz, mint az előző

const int& p = pi; //referencia konstans egészre
int const& p = pi; //ugyanaz, mint az előző

//most jön a lényeg

const int* const c = &pi; //konstans pointer konstans egészre
int const * const c = &pi; //ugyanaz, mint az előző

int* const c = &x; // konstans pointer változtatható egészre

/*!!!---!!!*/
//az alábbi kódrészletek pedig nem működnek, mivel konstans objektumra csak pointer-to-const és reference-to-const mutathat

//mivel pi const, ezért csak pointer-to-const mutathat rá
int* const c = &pi; 

//mivel pi const, ezért csak reference-to-const referálhat rá
int& r = pi; 
```

## Null pointer

A régebbi(prog1en oktatott) C verziókban a `NULL` valójában a konstans 0 void* -é kasztolása. C++ban a `void*` -> `T*` konverzió nem implicit, így C++ban a null pointernek saját `std::nullptr_t` típusa van, és `nullptr` -ként hivatkozunk rá a kódban. Az `std::nullptr_t` típust a saját kódunkban nem fogjuk használni, viszont annyit kell tudni róla, hogy bármilyen pointer típussá és `bool`-ra is képes implicit konvertálódni, azaz működnek a
```cpp
int* a = nullptr;

if(a) {

}
```
kódrészletek.