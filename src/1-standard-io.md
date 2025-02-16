# Standard IO

## Problémák a C standard IO-val

A `printf` és `scanf` fő problémája a compile time hibaellenőrzés hiánya. Nincs típusellenőrzés, így gyakran lesznek ezekkel a függvényekkel kapcsolatban problémáink. A `scanf` függvénynél ezen felül nem szabad elfelejteni a címképző operátort (`&`) sem, a `printf` pedig nem képes kiírni a saját típusainkat, valamint ezt megtanítani sem tudjuk neki.

## C++ alternatívák
<https://en.cppreference.com/w/cpp/io/cout>

<https://en.cppreference.com/w/cpp/io/cin>

`<iostream>` header

C++ban a standard input és output két fő globális objektum (`std::cin` és `std::cout`) és a C-ből shiftelő operátorokként, (`>>` és `<<`) ismert szimbólumokkal lett megoldva. A standard IO használatához az `iostream` headerre van szükség.

Ha egy változóba szeretnénk beolvasni, majd ezt kiírni:
```cpp
#include <iostream>

int main(){
    int x;
    std::cin >> x;
    std::cout << x;
}

```

A beolvasásokat és kiírásokat láncolhatjuk is:

```cpp
int x;
double d;
char c;

std::cin >> x >> d >> c;
std::cout << "int: " << x << " double: " << d << " char: " << c;
```
Ez a "szintaktika" operátorok túltöltésén (overload) alapul.
Jelenleg annyi említest teszek ezzel kapcsolatban, hogy valójában egy `operator<<` függvényt hívunk meg az `std::cout` (referencia rá) és a "kiírandó dolog" paraméterekkel, ami aztán referenciaként újra visszaadja az `std::cout` -ot, így tudjuk őket láncolni is.
Később azt is megtanuljuk, hogy pontosan hogyan működik az operátorok overload-olása és láncolása, valamint megtanítjuk majd a saját típusaink beolvasását és kiírását is.

### Get
<https://en.cppreference.com/w/cpp/io/basic_istream/get>

```cpp
char k = std::cin.get(); //bekérünk 1 karaktert

char k2;
std::cin.get(k2); //ugyanaz mint az előző, csak máshogy, itt out parameter van return helyett

char k3[6];
std::cin.get(k3, 5); //5 karaktert olvasunk egy 5 méretű tömbbe. Ez a függvény tesz lezáró 0-t

```

## std::getline
<https://en.cppreference.com/w/cpp/string/basic_string/getline>

Az std::getline függvény alapértelmezetten egy egész sort olvas be egy input streamről, viszont saját elválasztót is megadhatunk neki.

```cpp
std::string line;
std::getline(std::cin, line);
std::getline(std::cin, line, ','); // ',' karakterig olvasunk
```

## Ignore
<https://en.cppreference.com/w/cpp/io/basic_istream/ignore>

A bemeneti streameknek van egy `ignore` tagfüggvénye, amellyel eldobhatunk("ignorálhatunk") karaktereket.
```cpp
std::cin.ignore(x); // x karaktert ignorál, vagy amíg eof-t nem kap
std::cin.ignore(std::numeric_limits<std::streamsize>::max()); //ignorál mindent ami a bemeneten van
std::cin.ignore(x, c); //ignorál x karakter, vagy amíg nem kap c-vel azonos karaktert
```

`std::numeric_limits<T>::max()` : adott `T` numerikus típus maximum értékét adja vissza. (pl. `std::numeric_limits<std::size_t>::max()`)

Pl:
```cpp
#include <iostream>
#include <limits>

int main(){
    int a;
    int b;
    std::cin >> a;
    std::cin.ignore(5);
    std::cin >> b;
    std::cout << "a: " << a << " b: " << b << '\n';

    char c1;
    char c2;
    std::cin >> c1;
    //ignorálunk addig amíg ';' -t nem kapunk. Ignorálja a ; -t is!
    std::cin.ignore(std::numeric_limits<std::streamsize>::max(), ';'); 
    std::cin >> c2;
    std::cout << "c1: '" << c1 <<"' c2: '" << c2 << "'\n";
}
```
![](<Screenshot 2025-01-29 115519.png>)

*Nem összekeverendő a teljesen más jelentésű `std::ignore`-al.*

## File IO
`<fstream>` header

C++ -ban a file IO *API*-ja (az, amit a programozó lát belőle, Application Programming Interface) megegyezik a standard IO-val.

File olvasásra megnyitásához  és nyilvántartásához az `std::ifstream` (Input Filestream) típust, írásra az `std::ofstream` (Output Filestream) típust használjuk.

```cpp
#include <fstream>

int main(){
    std::ifstream input("input.txt");
    int x;
    input >> x; 
    std::ofstream output("output.txt");
    output << x;
}
```

Az `std::ifstream` és `std::ofstream` típusó objektumok automatikusan (ld. [osztályok](./5-osztályok.md)) bezárják a fileokat, ha scopeon kívül kerülnek, így nem szükséges a fileokat manuálisan bezárni, viszont a lehetőségünk megvan rá. (`.close()`)

## IO manipulátorok
`<ios>` és `<iomanip>` headerek

Az IO műveletek viselkesését ún. manipulátorok segítségével változtathatjuk meg. Ezeket úgy használjuk, mintha ők maguk is input/output lennének. Pl. ha az egészeket mindenképp 7 számjeggyel szeretnénk kiírni, és 0-val kitölteni a maradék helyet.


<https://godbolt.org/z/of6nP3xjn>
```cpp
#include <iomanip>
#include <iostream>

int main(){
    int x = 356;
    std::cout << std::setw(7) << std::setfill('0') << x; 
}
```

A manipulátorok hatóköre változó, vannak olyanok, amelyek csak a következő outputra hatnak, de vannak olyanok is, amelyek hatása "végtelen"(amíg meg nem változtatjuk).

Fontosabb mainpulátorok:
* `std::setw(size)` : megadja, hogy a számok hány karakter szélesek legyene
* `std::setfill(ch)` : a paraméterként kapott karakterrel lesz kitöltve a maradék hely, ha egy kiírt érték nem tölti ki a megadott szélességet
* `std::setprecision(p)` : a lebegőpontos számok tizedesjegyeinek pontosságát (számát) állítja be
* `std::oct`, `std::dec`, `std::hex` : 8-as, 10-es és 16-os számrenszerre állítja az adott streamet
* `std::skipws`, `std::noskipws` : Be/kikapcsolja a leading whitespace átugrását
* `std::boolalpha`, `std::noboolalpha` : Be/kikapcsolja a `bool` értékek alfanumerikus megjelenítését. (be: `true`/`false`, ki: `1`/`0`)

Több IO manipulátor és egyéb kapcsolódó foszlányok itt: <https://en.cppreference.com/w/cpp/io/manip>

Sokszor állítunk el dolgokat egy IO streamen, viszont nem szeretnénk egyesével visszaállítani az eredeti értékeket.
Ekkor van két lehetőségünk. 
Az első, hogy egy "buffer stream" segítségével összeállítunk egy stringet és ezt a stringet írjuk ki. Ehhez használjuk az `std::stringstream` típust: <https://en.cppreference.com/w/cpp/io/basic_stringstream>

<https://godbolt.org/z/59YETh5dn>
```cpp
#include <sstream>
#include <iostream>

int main(){
    std::stringstream buf;
    buf << std::hex << 45678;
    std::cout << buf.str();
}
```

A másik lehetőség az, hogy a stream beállításait (flag, precision, width) elmentjük, majd ezeket visszaállítjuk. Ez elég nagy szenvedés és nem érdemes csinálni, csak ha nagyon muszály.

<https://godbolt.org/z/o1hxqvnzz>
```cpp
#include <sstream>
#include <iostream>
#include <iomanip>

int main(){
    //most őszintén, kinek van ehhez kedve?
    std::ios_base::fmtflags flags = std::cout.flags();
    std::streamsize prec = std::cout.precision();
    std::streamsize width = std::cout.width();
    std::cout << std::hex << 465643 << std::setprecision(12) << std::setw(20) << 454.3256456436;
    std::cout.flags(flags);
    std::cout.precision(prec);
    std::cout.width(width);
    std::cout << '\n';
    std::cout << 54;
}
```