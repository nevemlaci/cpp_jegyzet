# Osztályok, objektumok
*most ugrik a majom a vízbe*

**Ez egy viszonylag hosszú fejezet, azonban a nyelv megértéséhez esszenciális!**

## Osztály, objektum

A C nyelvben már megismerhettük a `struct` kulcsszót, ami azonos dologhoz tartozó adatokat tárolt. Valószínűleg sok olyan függvényt írtunk ekkor, hogy

```c
struct foo {};

void foo_szamol(struct foo f) {}
```
és társai. Jó lenne, ha a `foo_szamol` függvényt valahogyan a `foo` struktúrához köthetnénk.

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

<https://godbolt.org/z/vYb75s41a>
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

Egy tagváltozó lehet `const`, ami azt jelenti, hogy nem változtatja meg az objektum állapotát, így `const` objektumon is működik.<br>
***FONTOS*** egy tagfüggvény túltölthető az alapján, hogy `const` -e, vagy nem, így a `const` qualifier része a függvény fejlécének! (signature)

A `this` pointer egy osztályon belül az adott példányra vonatkozik, viszont kiírni csak akkor kell, ha egy tagfüggvény paramétere miatt egy név nem egyértelmű.
A tagfüggvények gyakorlatilag speciális függvények, amelyek első paramétere a rejtett `this` pointer. 

A szintaxis a következő:

<https://godbolt.org/z/E3YP9scPq>
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
Tagfüggvényeket a `.` operátorral érhetünk el:
```cpp
int main(){
    Square square;
    square.set_side_length(2.5);
    std::cout << square.calculate_area();
}
```

Felfedezhetjük azonban azt a problémát, hogy egy `const` négyzet objektummal sok mindent nem tudunk kezdeni, ugyanis annak nem változtathatjuk meg az oldalhosszát, mután az objektum "elkészült". Ezt a problémát később, a konstruktorral oldjuk meg.

## Konstruktor, destruktor és RAII

Most jön talán a C++ legfontosabb része. A RAII(Resource Acquisition Is Initialization), de hívhatjuk *"Scope Based Resource Management*-nek is, módszer szerint egy objektum élettartama kezdetén(construction) átveszi és lefoglalja a számára szükséges erőforrásokat(memória, adatbázishoz csatlakozás, stb.) és élettartama végén(destruction) felszabadítja, bezárja ezeket az erőforrásokat.

A C++ nyelvben a "konstruktor"(constructor, ctor) speciális tagfüggvény fut az objektum élettartamának kezdetekor, és a destruktor fut az élettartam legvégén. Erre nézzünk egy egyszerű példát.

A konstruktornak és destruktornak nincs visszatérési értéke. A konstruktor függvény neve mindig megegyezik az osztály nevével, a destruktor neve pedig `~osztaly_neve`.
Objektum létrehozása alatt azt értjük, amikor egy lokális változót definiálunk az adott osztálytípussal, vagy a `new` operátorral dinamikus élettartamú objektumot hozunk létre.
Lokális változó élettartama a definiálásától a scope végéig, dinamikus élettartamú objektum élettartama a lefoglalásától(`new`) a felszabadításáig(`delete`) tart.

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

Egy osztályból csak akkor hozható létre (C értelemben vett) tömb, ha annak van default konstruktora.

A konstruktor arra való, hogy egy példány alap értékeit beállítsuk, viszont a konstruktorba írt kód valójában az objektum létrejötte után fut, így pl. konstans tagváltozókat, vagy konstans objektum tagváltozóit nem tudunk beállítani itt, ezért a tagváltozók inicializálását általában a "member initialization list" -en tesszük meg. Ennek kicsit furcsa szintaxisa van: `classname() : member1(value1), member2(value2)`<br>
Vegyük újra példának a `Square` osztályt.

<https://godbolt.org/z/hK479jPbY>
```cpp
class Square{
private:
    double side_length; //privát, írunk rá publikus set és get függvényt.
    std::string name; //std::string : egy dinamikusan növő karakter tömb, modern nyelvektől elvárt string típus
public:
    // : side_length(side_length) -> a side_length nevű tagváltozót inicializáljuk a side_length nevű paraméterrel
    // vesszővel választjuk el a tagokat
    Square(double side_length, const std::string& name) : side_length(side_length), name(name) {
    } //így már lehet const Square is használható objektum

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
Mint ahogyan a függvényekhez, az osztályokhoz is lehet sablonokat készítnei. 
pl.
```cpp
template <typename T>
class Foo{
public:
    T x;
};
```
Nagyon hasonlóan működik a függvényparaméterekhez, szimpla kódgenerálásról van szó.

## Gyakori félreértések, static tagfüggvények

*adatbázisok referencia következik*
Amikor egy osztályt hozunk létre, azzal még nem jön létre objektum. Az osztály egy tervrajz, egy *valami* leírása. Ez az objektumorientált programozás alapelve. A való világ(vagy esetleg kitalált világ) dolgairól készült tervrajzokból hozunk létre *példányokat*. Egy osztály egy példányát nevezzük általában objektumnak.

Pl.

```cpp
class foo{};

int main(){
    foo f; // f a foo osztály egy példánya
}
```

Amikor egy osztályban egy tagváltozót érünk el, az az adott példány tagváltozójára vonatkozik. Emlékezzünk vissza, a tagváltozók elérése (még ha implicit módon is) a `this` pointeren keresztül történik, azaz a példányunkra mutató pointeren keresztül.

Vannak azonban esetek amikor valamilyen állapotot nem egy példányhoz, hanem az osztályhoz szeretnénk kötni. Nos erre való a `static` kulcsszó. Egy statikus tagváltozó nem a példányokhoz, hanem az osztályhoz tartozik, a statikus tagfüggvény ugyanígy az osztályhoz tartozik. Természetesen ez azt is jelenti, hogy statikus tagváltozót/tagfüggvényt nem érhetünk el példányon keresztül, valamint `non static` tagváltozókat és tagfüggvényeket nem érhetünk el statikus tagfüggvényekből.

Statikus tagváltozókat a `::` operátorral érhetünk el: 
`foo::bar();`

```cpp
class foo{
    public:
        static void s_bar() {}
        void m_bar() {}
        int s_x;
        int m_x;
};

int main(){
    foo f;
    f.m_bar(); //ok
    f.m_x = 4; //ok
    f.s_bar; //nem ok
    foo::s_bar(); //ok
}
```

## Egyetlen felelősség elve

*"A module should be responsible to one, and only one, actor."* <br>
Nos ez egy kicsit furcsa lehet, szóval vegyünk egy érthetőbb megfogalmazást:
Egy osztálynak egyetlen felelősséget kell lefednie, viszont azt teljes mértékben. 

Pl. A `string` osztályunk kezeli a dinamikus karaktertömböt, viszont azzal nem foglalkozik, hogy a karaktereit egyesével hogy írjuk ki.

## Komolyabb RAII példa

Most pedig nézzünk egy komolyabb RAII példát. 
A tervünk egy dinamikusan növő tömb osztálysablon létrehozása ami bármilyen lemásolható típust képes tárolni.
Ezt a példát sokáig fogjuk használni.

Szóval szükségünk lesz egy `typename T` sablonparaméterre, egy pointerre, ami a tömbre mutat, valamint tárolni kell a tömb méretét
```cpp
#include <cstdint>

template <typename T>
class DinTomb{
    T* tomb; //pointer a dinamikus tömbre
    std::size_t meret; //a dinamikus tömb mérete

public:
    /**
     * @brief Default konstruktor, mindent 0-ra inicializál
     */
    DinTomb() : tomb(nullptr), meret(0) {}

    /**
     * @brief hozzáad egy új elemet a tömb végéhez. Nagyon hasonlít a C-ben megismert algoritmushoz, csak malloc-free helyett new-delete[] van
     * @param elem az elem amit hozzáadunk(lemásolható kell, hogy legyen)
     */
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

    /**
     * @brief indexelő függvény
     * @param idx
     * @return referencia az adott indexen lévő elemre
     * @throw std::out_of_range, ha túlindexelés történik
     */
    T& at(std::size_t idx) {
        if(idx >= meret) {
            throw std::out_of_range("Tomb tulindexelve!");
        }
        return tomb[idx];
    }

    //ua. mint az előbb, csak konstans verzió
    const T& at(std::size_t idx) const { 
        if(idx >= meret) {
            throw std::out_of_range("Tomb tulindexelve!");
        }
        return tomb[idx];
    }

    ~DinTomb() {
        delete[] tomb; //destruktor felszabadítja a lefoglalt memóriát
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

Nos igen, ez a RAII lényege. Nem kell manuálisan sehol `delete` és `new` -t írnunk, ha szépen becsomagoltuk a memóriakezelést egy osztályba. Az erőforráskezelést elabsztraktáltuk a felsőbb szintű kód elől, így ezt a tömb osztályt használva már nem kell a memóriakezeléssel foglalkoznunk.

Jó RAII példák a már megismert filestream osztályok. A konstruktorukban megnyitják a filet(elkérik a file handle-t az OS-től), majd a destruktorukban automatikusan bezárják a file-t.

## Objektumok másolása

Tegyük fel, hogy a tömbünkből másolatot szeretnénk csinálni. Ez valójában nem más, mint egy tömbből egy új tömböt csinálunk. Azt a konstruktort, amely egy `T` típusú objektumból `T` típusú objektumot készít *másoló konstruktor*(copy constructor)-nak nevezzük.

A copy constructor valójában azt mondja meg, hogyan is kéne lemásolni egy objektumot. Ez sok esetben triviális, pl.
```cpp
class foo{
    public:
        int x;
        float y;
        double t;
};
```
Ha egy osztálynak minden tagváltozója lemásolható(van copy constructora, vagy pl. primitív típus), akkor lesz automatikusan generált copy constructora is. 

A copy constructor paramétereként `const T&` -et vesz át. Persze, hiszen a másolandó objektumot nem változtatjuk és a nem referenciaként átvételhet(lemásolásához) copy constructorra lenne szükség.
Ha például az osztályunk egy dinamikusan növő tömböt kezel, nem másolhatjuk le egyszerűen a tömbre mutató pointert, hanem a tömböt elemenként le kell másolni(deep copy).
Ennek oka az, hogy a pointer lemásolásával(shallow copy, ez a default) az egyik tömb destruktora felszabadítja mindkét tömböt. <https://en.wikipedia.org/wiki/Object_copying>

***FONTOS!*** Néhány olvasó esetleg ismerheti a `memcpy` függvényt. C++ objektumokat `memcpy`-vel(és `std::memcpy`-vel) másolni óriási hiba, mivel ilyenkor nem hívódnak meg az objektumok másoló konstruktorai!

```cpp
template <typename T>
class DinTomb{
    T* tomb; //pointer a dinamikus tömbre
    std::size_t meret; //a dinamikus tömb mérete

public:
    /**
     * @brief Default konstruktor, mindent 0-ra inicializál
     */
    DinTomb() : tomb(nullptr), meret(0) {}

    /**
     * @brief Másoló konstruktor
     * @param other a másik tömb amit másolunk
     */
    DinTomb(const DinTomb& other) : tomb(other.tomb != nullptr ? new T[other.meret] : nullptr), meret(other.meret) {
        //                                          ^ ha nullptr a másik tömb(vagy 0 a mérete), akkor nem foglalunk 0 méretű tömböt(nem is lehetne...)
        for(std::size_t i = 0; i < other.meret; ++i){
            tomb[i] = other.tomb[i];
        }
    }

    ~DinTomb() {
        delete[] tomb; //destruktor felszabadítja a lefoglalt memóriát
    }
};
```
## class vs struct

A `struct` keyword C++ -ban gyakorlatilag egy alternatíva osztályok definiálására. A `class` -tól annyiban különbözik, hogy `private` helyett alapértelmezetten minden `public` benne(C kompatibilitás miatt). Az, hogy valaki `class`-t vagy `struct`-ot használ, preferencia.

## Osztályok tagfüggvényei többmodulos programokban

Ha egy osztálynak saját header és cpp file-t dezignálunk, akkor azt a következő szintaxissal tehetjük meg:

`foo.hpp` (a .hpp kiterjesztés gyakori c++ header fileokhoz, de természetesen a .h ugyanígy gyakori)
```cpp
class foo{
    int x;
    static int y;
    public:
    foo(int x);
    void set_x(int x);
    int get_x() const;

    static void something();


    template <typename T>
    void print_with_x(T thing) const {
        std::cout << x << ' ' << thing;
    }
};
```

***FONTOS!*** A template definíciókat (explicit specializációkat kivéve) header fileokban kell megírni!

A .cpp fileban a `returntype classname::functionname(params...)` szintaktikát használjuk.<br>
Statikus tagváltozókat itt kell definiálni, itt a `type classname::variablename = somevalue;` szintaktikát használjuk. Osztálydefiníción kívül a `static` mást jelent, így kiírni nagy hiba.
`foo.cpp`
```cpp

int foo::y = 1; //statikus tagváltozó definíciója

foo::foo(int x) : x(x) {} //konstruktor definíciója

void foo::set_x(int x){
    this->x = x;
}

int foo::get_x() const { //fontos! a const része a függvény fejécének(signature), itt is ki kell írni.
    return x;
}

void foo::something(){
    y*=2;
}
```

#### *std::initializer_list*
<https://en.cppreference.com/w/cpp/utility/initializer_list>

`<initializer_list>` header

Ha szeretnénk a tömbünknek egy egyszerű inicializálási módszert adni, akkor átvehetünk egy `std::initializer_list` típusú objektumot konstruktor paraméterként.

Az `std::initializer_list` egy read-only "view", azaz módosítani nem tudjuk, viszont másolni tudunk belőle. Nincs sem `at()` tagfüggvénye, sem indexelő operátora, csak range-for ciklussal tudunk végigiterálni rajta.

```cpp
template <typename T>
class DinTomb{
    T* tomb; //pointer a dinamikus tömbre
    std::size_t meret; //a dinamikus tömb mérete

public:
    /**
     * @brief Default konstruktor, mindent 0-ra inicializál
     */
    DinTomb() : tomb(nullptr), meret(0) {}

    /**
     * @brief initializer list konstruktor
     * @param init
     */
    DinTomb(std::initializer_list<T> init) : tomb(new T[init.size()]), meret(init.size()) {
        std::size_t i = 0;
        for(const T& elem : init) {
            tomb[i] = elem;
            ++i;
        }
    }
};

int main(){
    DinTomb<int> tomb = {1, 2, 3, 4};
}
```