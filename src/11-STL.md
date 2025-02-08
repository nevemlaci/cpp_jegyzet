# A C++ Standard Library

A C++ Standard Library(gyakran STL, stdlib, stb.) alatt általában a C++ standard által meghatározott, C++ nyelvhez tartozó szabványos könyvtár egy implementációját értjük (pl libc++, libstdc++, MSVC STL).

## STL Tárolók

A standard tárolók fontosabb közös tulajdonságai: 
* mind osztálysablonok(Standard **Template** Library)
* begin és end iterátort visszaadó tagfüggvények foreach ciklushoz
* at tagfüggvény (ahol értelmes)
* indexelő operátor (ahol értelmes)

#### std::string

Egy egyszerű karakterlánc implementáció.

```cpp
std::string str = "foo";

str.push_back("bar");
str[0] = 'l';

std::cout << str;
```

#### std::vector
`<vector>` header
Egy általános dinamikus tömb típus. Nem mindig akkora helyet foglal, amennyire szüksége van, hanem kapacitás hiányában geometrikusan növeli a lefoglalt memória méretét(pl kétszerezi, vagy másfélszerezi)

```cpp
std::vector<int> x = {1, 2, 3};

x.push_back(-5);

std::cout << *x.begin() << '\n';

for(int elem : x){
    std::cout << elem << ' ';
}
```

Az `at()` tagfüggvény kivételt dob, ha túlindexeljük a tárolót, az indexelő operátor viszont nem.

Van egy konstruktora, amely egyetlen pozitív egészet vesz át, ezzel előre foglalható valamennyi elem. Az előre foglalt elemek előre default-constructolva lesznek.
```cpp
#include <iostream>
#include <vector>

int main(){
    std::vector<int> v(10);
    std::cout << v.size();
}
```


#### std::map és std::unordered_map
`<map>` és `<unordered_map>` headerek

A `map` és `unordered_map` kulcs-érték párok tárolására való tárolók. A `map` garantált olvasási sorrendet kínál, míg az `unordered_map` nem, cserébe viszont gyorsabb.

Mindkét típus indexelő operátora beilleszti az adott kulcs-érték párt, ha az adott kulcs még nincs a tárolóban, ha pedig bent van, akkor megváltoztatja a hozzá tartozó értéket.

```cpp
std::map<std::string, int> m;

m["foo"] = 5;
m["foo"] = 1;
std::cout << m["foo"];
```

Az `at()` tagfüggvény nem így viselkedik, hanem kivételt dob, ha a kulcs nincs a tárolóban.

Azt, hogy egy kulcs a tárolóban van -e, a `contains(key)` tagfüggvénnyel ellenőrizhetjük.

## STL algoritmusok
`<algorithm>` header

#### std::find, std::find_if

Az `std::find` függvény két iterátort(a keresés doménjét), valamint egy értéket vesz át. A doménjében az `==` operátor segítségével keresi a kapott értéket, és ha megtalálja, akkor visszaad rá egy iterátort. Ha nem találja meg, akkor a domén végére mutató iterátort adja vissza.
Az ilyen iterátor párokat gyakran *range*-nek nevezzük.

```cpp
    std::vector<foo> fs = {foo(1), foo(3), foo(-2)};

    auto find_iterator = std::find(fs.begin(), fs.end(), foo(3));
    if(find_iterator != fs.end()) {
        std::cout << "foo(3) pozicio: " << find_iterator - fs.begin() << '\n';
    }else {
        std::cout << "foo(3) -ra nincs talalat\n";
    }
```

Az `std::find_if` 3. paraméterként egy érték helyett egy predikátumfüggvényt(vagy más függvényhívó operátorral rendelkező objektumot) vesz át, amely `bool` -t ad vissza és egyetlen paramétereként átveszi egy a doménben tárolt objektumok típusával megegyező típusú objektumot(*értsd: átveszi az éppen vizsgált elemet*).

```cpp
    auto elter_2_iterator = std::find_if(fs.begin(), fs.end(), isDivisibleBy2);
    if(elter_2_iterator != fs.end()) {
        std::cout << "foo(%2) pozicio: " << elter_2_iterator - fs.begin() << '\n';
    }else {
        std::cout << "foo(%2) -re nincs talalat\n";
    }
```

#### std::count és std::count_if

Ugyan az, mint a `find` és `find_if`, csak összeszámolja a feltételt kielégítő elemeket.

<https://godbolt.org/z/E17se46PG>
```cpp
#include <iostream>
#include <vector>
#include <algorithm>

bool divisibleBy2(int x){
    return x % 2 == 0;
}

int main(){
    std::vector<int> v = {3, 2, 1, 5, 3, 2, 8, 3, 12};
    std::cout << "3-asok szama: " << std::count(v.begin(), v.end(), 3);
    std::cout << "\n2-vel oszthatoak szama: " << std::count_if(v.begin(), v.end(), divisibleBy2);
}
```

#### std::fill, std::generate

Az `std::fill` feltölti a kapott range-t egy értékkel.
<https://godbolt.org/z/7qbYq17v3>
```cpp
#include <iostream>
#include <vector>
#include <algorithm>

int main(){
    std::vector<int> v(10); //előre foglalunk 10 objektumot, különben a range 0 elemű lenne
    std::fill(v.begin(), v.end(), 9); 
    for(auto& elem : v){
        std::cout << elem << ' ';
    }
}
```

Az std::generate feltölti a kapott range-t értékekkel. 
Ezt egy generátor segítségével teszi, amely a harmadik paramétere. A generátor paraméter nélkül hívható objektum, amely visszaadja a beillesztendő értéket.

Pl.
<https://godbolt.org/z/Mz78oP4Wb>
```cpp
#include <iostream>
#include <vector>
#include <algorithm>

struct generator{
    int x;
    generator() : x(0) {}

    int operator()(){
        return x++; //emlékezzünk vissza mit csinál a posztinkremens operátor(növeli, de régi értéket returnöl)
    }
};

int main(){
    std::vector<int> v(10); //előre foglalunk 10 objektumot, különben a range 0 elemű lenne
    generator g; //készítünk egy generátor példányt
    std::generate(v.begin(), v.end(), g); //átadjuk a generátort
    for(auto& elem : v){
        std::cout << elem << ' ';
    }
}
```

A generálás gyakorlatilag a következőből áll:
```cpp
for(auto it = v.begin(), it != v.end(), ++it){
    *it = g();
}
```

#### std::equal, std::mismatch

Az `std::equal` megmondja, hogy két range minden eleme egyenlő -e.

<https://godbolt.org/z/qsv57sPK5>
```cpp
#include <iostream>
#include <vector>
#include <algorithm>

int main(){
    std::vector<int> v = {3, 2, 1, 5, 3, 2, 8, 3, 12};
    std::vector<int> w = {1, 4, 3, 2, 1, 7, 8, 9, 14};
    std::cout << std::boolalpha << std::equal(v.begin(), v.end(), w.begin(), w.end()) << '\n';
    std::cout << std::boolalpha << std::equal(v.begin(), v.end(), v.begin(), v.end());
}
```

Az `std::mismatch` megkeresi az első olyan pontot két range-ben, ahol eltérnek.

#### std::transform

Az `std::transform` végrehajt egy függvényt az adott range minden elemén és átmásolja egy másik rangebe. A függvény a range mindig aktuálisan változtatandó elemét veszi át.<br>
Első két paramétere a domén range eleje és vége, a hardmadik paramétere a másolás céljának eleje, a negyedik paraméter pedig a végrehajtandó művelet(függvény vagy funktor).

<https://godbolt.org/z/WKE977c8P>
```cpp
#include <iostream>
#include <vector>
#include <algorithm>

template<typename T> //template hogy mindenféle vektorhoz jó legyen
struct transformer{
    T elozo;
    
    transformer() : elozo(0) {}

    T operator()(const T& elem){
        int eredmeny = elem + elozo;
        elozo = elem;
        return eredmeny;
    }
};

int main(){
    std::vector<int> v = {3, 2, 1, 5, 3, 2, 8, 3, 12};
    std::vector<int> w(v.size());
    transformer<int> t;
    std::transform(v.begin(), v.end(), w.begin(), t);

    for(auto& elem : w){
        std::cout << elem << ' ';
    }
}
```

