# Standard IO

## Problémák a C standard IO-val

A `printf` és `scanf` fő problémája a compile time hibaellenőrzés hiánya. Nincs típusellenőrzés, így gyakran lesznek ezekkel a függvényekkel kapcsolatban problémáink. A `scanf` függvénynél ezen felül nem szabad elfelejteni a címképző operátort(`&`) sem, a `printf` pedig nem képes kiírni a saját típusainkat, valamint ezt megtanítani sem tudjuk neki.

## C++ alternatívák
<https://en.cppreference.com/w/cpp/io/cout>

<https://en.cppreference.com/w/cpp/io/cin>

C++ban a standard input és output két fő globális objektum(`std::cin` és `std::cout`) és a C-ből shiftelő operátorokként(`>>` és `<<`) ismert szimbólumokkal lett megoldva. A standard IO használatához az `iostream` headerre van szükség.

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
Ez a "szintaktika" operátorok túltöltésén(overload) alapul.
Jelenleg annyi említest teszek ezzel kapcsolatban, hogy valójában egy `operator<<` függvényt hívunk meg az `std::cout`(referencia rá) és a "kiírandó dolog" paraméterekkel, ami aztán referenciaként újra visszaadja az `std::cout` -ot, így tudjuk őket láncolni is.
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

`std::numeric_limits<T>::max()` : adott `T` típusú numerikus típus maximum értékét adja vissza. (pl. `std::numeric_limits<std::size_t>::max()`)

```cpp
int a;
int b;
std::cin >> a;
std::cin.ignore(5);
std::cin >> b;

char c1;
char c2;

std::cin >> c1;
//ignorálunk addig amíg ';' -t nem kapunk. Ignorálja a ; -t is!
std::cin.ignore(std::numeric_limits<std::streamsize>::max(), ';'); 
std::cin >> c2;
```

*Nem összekeverendő a teljesen más jelentésű `std::ignore`-al.*