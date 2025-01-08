# Standard IO

## Problémák a C standard IO-val


A `printf` és `scanf` fő problémája a compile time hibaellenőrzés hiánya. Nincs típusellenőrzés, így gyakran lesznek ezekkel a függvényekkel kapcsolatban problémáink. A `scanf` függvénynél ezen felül nem szabad elfelejteni a címképző operátort(`&`) sem, a `printf` pedig nem képes kiírni a saját típusainkat, valamint ezt megtanítani sem tudjuk neki.

## C++ alternatívák

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