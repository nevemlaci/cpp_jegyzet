# Osztályok, objektumok

**Ez egy viszonylag hosszú fejezet, azonban a nyelv megértéséhez gyakorlatilag esszenciális!**

## Osztály, objektum

A C nyelvben már megismerhettük a `struct` kulcsszót, ami azonos dologhoz tartozó adatokat tárolt. Valószínűleg sok olyan függvényt írtunk ekkor, hogy

```c
struct foo {};

void foo_szamol(struct foo f) {}
```
és társai.

Az osztályok ezt a problémát oldják meg, valamint néhány nagyon hasznos utility-t adnak a programozó kezébe.

Egy osztályt a `class` vagy a `struct` kulcsszóval(különbség később) tudunk definiálni, `typedef` használatára egyáltalán nincs szükség.

Egy osztályból "példányokat" hozhatunk létre, ez gyakorlatilag azt jelenti, hogy az adott osztály típusú változót hozunk létre a C struktúrákhoz hasonlóan.

```cpp
class Foo {};

int main(){
    Foo f;
}
```

## Publikus és privát elérés

Egy osztály tartalmazhat "member"-eket(tagokat), amelyeknek különböző láthatóságai lehetnek. 
Ezt a `public`, `private` és `protected` (később) szavakkal állíthatjuk be. Ezeket a kulcsszavakat *access specifier*-nek hívjuk.
A privát tagokat csak az osztályon belülről, a public-okat kívülről is elérhetjük. Egy osztályban alapból minden private, amíg ezt meg nem változtatjuk.

```cpp
class Foo {
public: //ez után a következő access-specifier -ig minden public.
    int x;
private: //ez után a következő access-specifier -ig minden private.
    double y;
};

int main(){
    Foo f;
    f.x = 5;
    f.y = 2.3; //nem ok, y private
```

## Tagfüggvények (member functions)

Az osztályok egyik "breaktrough" feature-je, hogy függvényeket tartalmazhatnak, amelyek az osztály által tárolt állapoton(state) operálnak.

Egy tagváltozó lehet `const`, ami azt jelenti, hogy nem változtatja meg az objektum állapotát, így `const` objektumon is működik.

A `this` pointer egy osztályon belül az adott példányra vonatkozik, viszont kiírni csak akkor kell, ha egy tagfüggvény paramétere miatt egy név nem egyértelmű.

A szintaxis a következő:

```cpp
class Square{
private:
    double side_length; //privát, írunk rá publikus set és get függvényt.

public:
    //"Setter" függvény, nagyon hasznos ha nem triviális egy érték beállítása(pl. itt side_length > 0 check miatt)
    void set_side_length(double side_length){
        if(side_length <= 0) { 
            throw std::runtime_error("side length <= 0 is not allowed");
        }

    //this->side_length: az adott példány oldalhossza,
    //side_length: a tagfüggvény paramétere
        this->side_length = side_length; 
    }

    double get_side_length() const { //const, mivel nem változtatja a példányt.
        return side_length; //nem kell this-> mivel nincs név konfliktus.
    }

    double calculate_area() const { //const, mivel csak számol, ez sem változtat semmit
        return side_length * side_length;
    }
};
```
## Konstruktor, destruktor és RAII

Most jön talán a C++ legfontosabb része. A RAII(Resource Acquisition Is Initialization) módszer szerint egy objektum élettartama kezdetén(construction) átveszi és lefoglalja a számára szükséges erőforrásokat(memória, adatbázishoz csatlakozás, stb.) és élettartama végén(destruction) felszabadítja, bezárja ezeket az erőforrásokat.

A C++ nyelvben a "konstruktor"(constructor, ctor) speciális tagfüggvény fut az objektum élettartamának kezdetekor, és a destruktor fut az élettartam legvégén. Erre nézzünk egy egyszerű példát.

A konstruktornak és destruktornak nincs visszatérési értéke. A konstruktor függvény neve mindig megegyezik az osztály nevével, a destruktor neve pedig `~osztaly_neve`.

```cpp
class Foo{
    Foo() {
        std::cout << "Foo ctor\n";
    }

    ~Foo() {
        std::cout << "Foo dtor\n";
    }
};

int main(){
    Foo f; //foo ctor lefut
    /*
    ...
    */

    return 0; //foo dtor lefut
}
```

Azt a konstruktort, amely paraméter nélkül hívható, *defualt konstruktor*nak nevezzük. Ha egy osztályban minden tagváltozónak van default konstruktora, és mi nem írtunk külön konstruktort, akkor az osztálynak generálódik default konstruktor.

A konstruktor arra való, hogy egy példány alap értékeit beállítsuk, viszont a konstruktorba írt kód valójában az objektum létrejötte után fut, így pl. konstans tagváltozókat nem tudunk beállítani itt, ezért a tagváltozók inicializálását általában a "member initialization list" -en tesszük meg. Ennek kicsit furcsa szintaxisa van.
Vegyük újra példának a `Square` osztályt.

```cpp
class Square{
private:
    double side_length; //privát, írunk rá publikus set és get függvényt.
    std::string name; //std::string : egy dinamikusan növő karakter tömb, modern nyelvektől elvárt string típus
public:
    // : side_length(side_length) -> a side_length nevű tagváltozót inicializáljuk a side_length nevű paraméterrel
    // vesszővel választjuk el a tagokat
    Square(double side_length, const std::string& name) : side_length(side_length), name(name) {
    } 

    //"Setter" függvény, nagyon hasznos ha nem triviális egy érték beállítása(pl. itt side_length > 0 check miatt)
    void set_side_length(double side_length){
        if(side_length <= 0) { 
            throw std::runtime_error("side length <= 0 is not allowed");
        }

        this->side_length = side_length; //this->side_length: az adott példány oldalhossza, side_length: a tagfüggvény paramétere
    }

    double get_side_length() const { //const, mivel nem változtatja a példányt.
        return side_length; //nem kell this-> mivel nincs név konfliktus.
    }
};

int main(){
    Square square(5.3, "foo"); //konstruktor hívás
    Square square; //ez most nem működik, mert Square-nek nincs default konstruktora. 
}
```

## Osztálysablonok
Mint ahogyan a függvények, az osztályokhoz is lehet sablonokat készítnei. 
pl.
```cpp
template <typename T>
class Foo{
public:
    T x;
};
```
Nagyon hasonlóan működik a függvényparaméterekhez, szimpla kódgenerálásról van szó.

## Komolyabb RAII példa

Most pedig nézzünk egy komolyabb RAII példát. 
A tervünk egy dinamikusan növő tömb osztálysablon létrehozása ami bármilyen lemásolható típust képes tárolni.
Ezt a példát sokáig fogjuk használni.

Szóval szükségünk lesz egy `typename` sablonparaméterre, egy pointerre, ami a tömbre mutat, valamint tárolni kell a tömb méretét
```cpp
#include <cstdint>

template <typename T>
class DinTomb{
    std::size_t meret; //dinamikus tömb méretét tárolja
    T* tomb; //T* -> T-re mutató pointer, ez fog mutatni a tömbre.

public:
    DinTomb() : meret(0), tomb(nullptr) {} //default ctor, 0-ra inicializalunk mindent

    //ez fog beilleszteni, gyakorlatilag ugyanaz, mint C-ben, csak new és delete van malloc&free helyett
    void push_back(const T& elem) { 
        T* uj_tomb = new T[meret + 1];
        for(std::size_t i = 0; i < meret; ++i){
            uj_tomb[i] = tomb[i];
        }
        uj_tomb[meret] = elem;
        delete[] tomb; // delete[], mert tömböt szabadítunk fel.
        tomb = uj_tomb;
        ++meret;
    }

    std::size_t size() const { return meret; }

    //visszaad egy referenciát az adott tömbindexre
    T& at(std::size_t idx) {
        return tomb[idx];
    }

    ~DinTomb() {
        delete[] tomb; // a destruktor felszabadítja az objektum által használt erőforrást az élettartam végén
    }
};

int main(){
    DinTomb<double> tomb; //valos szamokat tartalmazo dinamikus tomb

    tomb.push_back(4.3);
    tomb.push_back(3.2);
    tomb.at(0) = 5.8; //függvény az egyenlőség bal oldalán, mivel referenciát ad vissza!
    return 0; // nem kell semmi manuális memóriakezelés, mert a destruktor automatikusan felszabadítja amit kell, mert egyszer megírtuk
}
```

Nos igen, ez a RAII lényege. Nem kell manuálisan sehol `delete` és `new` -t írnunk, ha szépen becsomagoltuk a memóriakezelést egy osztályba. Ezt teszi a C++ Standard Library nagyrésze, pl. `std::vector`, a Standard Library dinamikus tömb típusa.

## class vs struct

A `struct` keyword C++ -ban gyakorlatilag egy alternatíva osztályok definiálására. A `class` -tól annyiban különbözik, hogy `private` helyett alapértelmezetten minden `public` benne(C kompatibilitás miatt). Az, hogy valaki `class`-t vagy `struct`-ot használ, preferencia.

## Operátorok túltöltése

Az operátorok valójában csak speciális függvények. Ez azt jelenti, hogy ugyanúgy bánhatunk velük, habár van némi megkötés, azonban legtöbbször ezek nem fognak az utunkban állni. 

Ha egy operátor az adott osztály típust veszi át baloldali paraméterként, akkor az operátort az osztályon belül tagfüggvényként kezelhetjük. Ekkor valójában egy paramétert adunk neki, ami a jobb oldali operandus. A bal oldali operandusa implicit a `this` pointer lesz.

Szeretnénk, hogy a tömbünkhöz a += operátorral is lehessen új elemet hozzáadni. Ehhez túl kell töltenünk += operátort.
A += operátorra "függvényként" az `operator+=` kifejezéssel hivatkozhatunk.

Nézzünk egy példát:

```cpp
class DinTomb{
    /* 
        ...
    */

    void operator+=(const T& elem){
        push_back(elem); //delegáljuk a beillesztést a push_back függvénynek, nem duplikálunk kódot.
    }
};

int main(){
    DinTomb tomb;
    tomb += 5.2; // értelmezzük: tomb.operator+=(5.2) -> operator+=(&tomb, 5.2)

    return 0;
}
```

Most szeretnénk, ha a tömbünket ki is lehetne írni. Viszont ezzel van egy kis gond. Azt, hogy hova írjuk ki a tömböt(stdout, file, stb.) balértékként veszi át az `operator<<` (stream insertion operator), ezért ezt az osztályon kívük kell túltölteni. 
A `friend` kulcsszó használatával az osztályon belül deklaráljuk a függvényt, ezzel "megengedjuk" neki, hogy a privát tagokat is lássa. Eztunán az osztályon kívül definiáljuk.

```cpp
#include <iostream>

class DinTomb{
    /* 
        ...
    */

    friend std::ostream& operator<<(std::ostream& out, const DinTomb& dtomb);
};

std::ostream& operator<<(std::ostream& out, const DinTomb& dtomb){
    for(std::size_t i = 0; i < dtomb.meret; ++i){
        out << dtomb.tomb[i] << ' ';
    }

    return out;
}

int main(){
    DinTomb tomb;
    tomb += 5.2; // értelmezzük: tomb.operator+=(5.2) -> operator+=(&tomb, 5.2)
    tomb += 2.3;
    tomb.push_back(8.7);

    std::cout << tomb;
    return 0;
}
```
Ha az `operator<<`-t streamre való kiírásra használjuk, akkor mindig `std::ostream&` -et ad vissza és vesz át bal operandusként, valamint visszaadja a bal operandusát, így láncolhatóvá teszi az operátort. (`std::cout << a << b << c;`)

Természetesen ezt a példát `friend` nélkül is meg lehet oldani, azonban ez nem mindig van így.
