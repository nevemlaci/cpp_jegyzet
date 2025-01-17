# Operator overloading

## Mik az operátorok valójában?

Az operátorok valójában csak speciális függvények. Ez azt jelenti, hogy ugyanúgy bánhatunk velük, habár van némi megkötés, azonban legtöbbször ezek nem fognak az utunkban állni. 

## Operátorok és osztályok

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

## Friend

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

## Copy assignment(értékadó operátor)

A másoló konstruktor testvére a copy assignment(értékadó) operator. A copy constructorhoz hasonlóan `const T&` -ként veszi át a másolandó objektumot és a default is generálódik belőle.
Fontos, hogy a copy assignment operátor nem új objektumot hoz létre így az előzőleg használt erőforrásokat fel kell szabadítani.

```cpp
class tomb{
    T* adat;
    std::size_t size;

    public:
    tomb(const tomb& other);

    tomb& operator=(const tomb& other){
        delete[] adat;
        adat = new T[other.size];
        size = other.size;
        for(std::size_t i = 0; i < other.size; ++i){
            adat[i] = other.adat[i]; 
        }
    }

    ~tomb();
    
    void push_back(const T& elem);
    T& at(std::size_t idx);
    //...
};
```

## Rule of 0/3

<https://en.cppreference.com/w/cpp/language/rule_of_three>

Rule of 3: Ha egy osztálynak szüksége van nem compiler-default destruktorra, másoló konstruktorra vagy copy assignment operátorra akkor majdnem biztosan szüksége van mindháromra.

*advanced*
Rule of 0: Azok az osztályok, amelyeknek nem compiler-default destruktora, copy construktora, copy assignment operátora van, azok valamilyen explicit erőforrás-birtoklást valósítanak meg. (<https://en.wikipedia.org/wiki/Single-responsibility_principle>). Ettől eltérő osztályoknak ne legyen nem compiler-default destruktora, copy constructora vagy copy assignment operátora.

## Néhány kötöttség

Nem változtatható meg:
* precedencia
* asszocivitás

Ezen felül egyes operátoroknak csak kötött számú paramétere lehet.<br>
A logikai(`||` és `&&`) operátorok túltöltése esetén azok elvesztik a short-circuit tulajdonságukat.